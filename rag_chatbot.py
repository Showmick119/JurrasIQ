import openai
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load excavation plans (In real implementation, this should be stored in a DB or indexed for retrieval)
excavation_plans = {}  # Dictionary to store plans per site


def generate_chat_response(user_query, site_name):
    """
    Generates a response based on the excavation plan and external knowledge.
    """
    if site_name not in excavation_plans:
        return "No excavation plan found for this site. Please generate a plan first."
    
    excavation_data = json.dumps(excavation_plans[site_name])
    
    prompt = f"""
    You are an excavation assistant chatbot.
    
    The user has asked: "{user_query}"
    
    Here is the structured excavation plan for reference:
    {excavation_data}
    
    If the answer is found in the plan, respond based on that. If not, use your external excavation knowledge to help.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are an excavation planning assistant."},
                      {"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        
        return response["choices"][0]["message"]["content"]
    
    except Exception as e:
        return str(e)


@app.route("/store_plan", methods=["POST"])
def store_excavation_plan():
    """ Stores the excavation plan for later retrieval. """
    data = request.json
    site_name = data.get("site_name")
    excavation_plans[site_name] = data  # Store the plan in memory
    return jsonify({"message": "Excavation plan stored successfully.", "site": site_name})


@app.route("/chat", methods=["POST"])
def chat_with_agent():
    """ Chatbot API endpoint. """
    data = request.json
    user_query = data.get("query")
    site_name = data.get("site_name")
    
    response = generate_chat_response(user_query, site_name)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True, port=5001)