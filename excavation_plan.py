import openai
import json
import os
import smtplib
import random
import requests
from email.mime.text import MIMEText

# Load API Keys from Render Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ZOOM_CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")
ZOOM_ACCOUNT_ID = os.getenv("ZOOM_ACCOUNT_ID")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def validate_json(response_text):
    """ Ensures OpenAI response is valid JSON """
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format received from OpenAI"}

def generate_excavation_plan(site_name, site_area, fossil_yield, depth_required, team_size, user_location):
    """
    Generates a comprehensive excavation plan using OpenAI API.
    """
    openai.api_key = OPENAI_API_KEY

    prompt = f"""
    You are an expert in archaeological excavation planning. Given an excavation site, generate a detailed structured plan covering:
    
    1. **Excavation Overview**: Details about the site, expected challenges, and best excavation techniques.
    2. **Excavation Duration**: Estimated time required for excavation based on site depth, fossil yield, and manpower.
    3. **Manpower & Resources**: Number of workers needed, roles, equipment required, and estimated labor costs.
    4. **Step-by-Step Excavation Plan**: Chronological breakdown of excavation phases, safety measures, and best practices.
    5. **Travel & Logistics**: Optimal travel route from {user_location} to {site_name}, recommended transport mode (train, bus, flight, car), estimated ticket costs, and logistics.
    6. **Accommodation & Food**: Best lodging options near the site, per-night hotel costs, food expenses per person.
    7. **Final Budget Breakdown**: Summarized cost of excavation, labor, travel, lodging, and other expenses.
    8. **Actionable Steps**: Interactive buttons for booking tickets, renting equipment, hiring workers, and accessing safety protocols.
    
    Site Details:
    - Site Name: {site_name}
    - Location: {user_location} to {site_name}
    - Site Area: {site_area} sq km
    - Expected Fossil Yield: {fossil_yield}
    - Depth Required: {depth_required} meters
    - Team Size: {team_size} people
    
    💡 Output the result strictly in structured JSON format suitable for frontend display.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are a structured excavation planning assistant."},
                      {"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=800
        )
        
        structured_data = validate_json(response["choices"][0]["message"]["content"])
        send_excavation_email(site_name, structured_data)
        return structured_data
    
    except Exception as e:
        return {"error": str(e)}

def get_zoom_access_token():
    """Fetch an OAuth access token for Zoom API."""
    url = "https://zoom.us/oauth/token"
    headers = {
        "Authorization": "Basic " + requests.auth._basic_auth_str(ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "account_credentials", "account_id": ZOOM_ACCOUNT_ID}

    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()

    if "access_token" in response_data:
        return response_data["access_token"]
    else:
        raise Exception(f"Failed to get Zoom token: {response_data}")

def create_zoom_meeting(site_name):
    """Creates a Zoom meeting and returns the meeting link."""
    try:
        access_token = get_zoom_access_token()
        url = "https://api.zoom.us/v2/users/me/meetings"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "topic": f"Excavation Planning - {site_name}",
            "type": 2,  # Scheduled meeting
            "duration": 60,
            "timezone": "UTC",
            "agenda": f"Discussion on excavation plan for {site_name}",
            "settings": {"host_video": True, "participant_video": True},
        }

        response = requests.post(url, headers=headers, json=payload)
        meeting_data = response.json()

        if "join_url" in meeting_data:
            return meeting_data["join_url"]
        else:
            raise Exception(f"Failed to create Zoom meeting: {meeting_data}")
    except Exception as e:
        return f"Error creating Zoom meeting: {str(e)}"

def send_excavation_email(site_name, plan_details):
    """ Sends an email to the excavation team with trip details """
    recipients = [
        {"name": "Showmick Das", "email": "showmickdas75@gmail.com"},
        {"name": "Aadi Raj Dewan", "email": "aadird13@gmail.com"},
        {"name": "Ujaan Rakshit", "email": "ujaanrakshit@gmail.com"}
    ]
    
    meeting_time = random.choice(["10:00 AM", "2:00 PM", "5:00 PM"])
    meeting_date = "March 10, 2025"
    zoom_link = create_zoom_meeting(site_name)

    subject = f"Excavation Trip to {site_name} - Important Details"
    body = f"""
    Dear Team,
    
    You have an upcoming excavation trip to {site_name}.
    
    **Excavation Overview:**
    {plan_details.get('excavation_overview', 'Details will be shared soon.')}

    **Meeting Details:**
    - Date: {meeting_date}
    - Time: {meeting_time}
    - Topic: Excavation planning for {site_name}
    - Zoom Link: {zoom_link}
    
    Please be available for the meeting. 
    
    Best,
    JurassIQ AI Assistant
    """

    for recipient in recipients:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient["email"]
        
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(SENDER_EMAIL, EMAIL_PASSWORD)
                server.sendmail(SENDER_EMAIL, recipient["email"], msg.as_string())
                print(f"Email sent to {recipient['name']} ({recipient['email']})")
        except Exception as e:
            print(f"Error sending email to {recipient['name']}: {str(e)}")

# Example Usage
if __name__ == "__main__":
    site_details = {
        "site_name": "Gobi Desert Fossil Site",
        "site_area": 5,
        "fossil_yield": "Medium (30-50 fossils)",
        "depth_required": 2.5,
        "team_size": 8,
        "user_location": "New York, USA"
    }

    plan = generate_excavation_plan(**site_details)
    print(json.dumps(plan, indent=4))