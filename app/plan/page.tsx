"use client"

import { useSearchParams } from 'next/navigation'
import { useEffect, useState, Suspense } from 'react'
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { AlertCircle, Clock, FileText, MapPin, Microscope, Calendar } from "lucide-react"
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

function PlanContent() {
  const searchParams = useSearchParams()
  const [plan, setPlan] = useState<string>('')
  const [error, setError] = useState<string>('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const siteData = searchParams.get('site')
    if (!siteData) {
      setError('No site data provided')
      setLoading(false)
      return
    }

    const fetchPlan = async () => {
      try {
        const response = await fetch('/api/excavation/plan', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: siteData
        })

        const data = await response.json()
        if (data.error) throw new Error(data.error)
        setPlan(data.plan)
      } catch (error) {
        setError(error instanceof Error ? error.message : 'Failed to load plan')
      } finally {
        setLoading(false)
      }
    }

    fetchPlan()
  }, [searchParams])

  if (error) {
    return (
      <div className="container mx-auto py-8">
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      </div>
    )
  }

  const site = searchParams.get('site') ? JSON.parse(decodeURIComponent(searchParams.get('site')!)) : null

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-background/80">
      <div className="container mx-auto py-8 space-y-8 px-4">
        {/* Enhanced Header Section */}
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-primary to-primary/70">
            Excavation Plan
          </h1>
          <p className="text-xl text-muted-foreground mb-8">
            Comprehensive Analysis & Strategic Operations Document
          </p>
          
          {site && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-8">
              <Card className="bg-card/50 backdrop-blur-sm border-primary/10">
                <CardHeader className="space-y-1">
                  <div className="flex items-center gap-2 text-primary">
                    <Microscope className="h-5 w-5" />
                    <h3 className="font-semibold">Fossil Type</h3>
                  </div>
                  <p className="text-sm text-muted-foreground">{site.fossilType}</p>
                </CardHeader>
              </Card>
              
              <Card className="bg-card/50 backdrop-blur-sm border-primary/10">
                <CardHeader className="space-y-1">
                  <div className="flex items-center gap-2 text-primary">
                    <Calendar className="h-5 w-5" />
                    <h3 className="font-semibold">Age Range</h3>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {site.age_start} - {site.age_end} Mya
                  </p>
                </CardHeader>
              </Card>
              
              <Card className="bg-card/50 backdrop-blur-sm border-primary/10">
                <CardHeader className="space-y-1">
                  <div className="flex items-center gap-2 text-primary">
                    <MapPin className="h-5 w-5" />
                    <h3 className="font-semibold">Location</h3>
                  </div>
                  <p className="text-sm text-muted-foreground">{site.locationName}</p>
                </CardHeader>
              </Card>
              
              <Card className="bg-card/50 backdrop-blur-sm border-primary/10">
                <CardHeader className="space-y-1">
                  <div className="flex items-center gap-2 text-primary">
                    <FileText className="h-5 w-5" />
                    <h3 className="font-semibold">Environment</h3>
                  </div>
                  <p className="text-sm text-muted-foreground">{site.environment}</p>
                </CardHeader>
              </Card>
            </div>
          )}
        </div>

        {/* Main Content with Enhanced Styling */}
        <Card className="overflow-hidden max-w-5xl mx-auto bg-card/50 backdrop-blur-sm border-primary/10">
          <CardContent className="p-8">
            {loading ? (
              <div className="space-y-6">
                {[...Array(8)].map((_, i) => (
                  <div key={i} className="space-y-3">
                    <Skeleton className="h-8 w-[40%]" />
                    <div className="space-y-2">
                      <Skeleton className="h-4 w-full" />
                      <Skeleton className="h-4 w-[95%]" />
                      <Skeleton className="h-4 w-[90%]" />
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <article className="prose prose-slate dark:prose-invert prose-headings:text-primary max-w-none">
                <ReactMarkdown 
                  remarkPlugins={[remarkGfm]}
                  components={{
                    h1: ({node, ...props}) => (
                      <h1 className="text-3xl font-bold border-b border-primary/20 pb-4 mb-6" {...props} />
                    ),
                    h2: ({node, ...props}) => (
                      <h2 className="text-2xl font-semibold mt-8 mb-4 text-primary/90" {...props} />
                    ),
                    h3: ({node, ...props}) => (
                      <h3 className="text-xl font-medium mt-6 mb-3 text-primary/80" {...props} />
                    ),
                    ul: ({node, ...props}) => (
                      <ul className="my-4 list-disc pl-6 marker:text-primary/60" {...props} />
                    ),
                    ol: ({node, ...props}) => (
                      <ol className="my-4 list-decimal pl-6 marker:text-primary/60" {...props} />
                    ),
                    li: ({node, ...props}) => (
                      <li className="mt-2" {...props} />
                    ),
                    p: ({node, ...props}) => (
                      <p className="my-4 leading-relaxed" {...props} />
                    ),
                    blockquote: ({node, ...props}) => (
                      <blockquote className="border-l-4 border-primary/20 pl-4 italic my-6 text-muted-foreground" {...props} />
                    ),
                    table: ({node, ...props}) => (
                      <div className="overflow-x-auto my-6">
                        <table className="min-w-full border border-primary/20" {...props} />
                      </div>
                    ),
                    th: ({node, ...props}) => (
                      <th className="bg-primary/5 border border-primary/20 px-4 py-2 text-left" {...props} />
                    ),
                    td: ({node, ...props}) => (
                      <td className="border border-primary/20 px-4 py-2" {...props} />
                    ),
                  }}
                >
                  {plan}
                </ReactMarkdown>
              </article>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function PlanLoading() {
  return (
    <div className="container mx-auto py-8 space-y-8 px-4">
      <div className="text-center max-w-3xl mx-auto">
        <Skeleton className="h-12 w-64 mx-auto" />
        <Skeleton className="h-6 w-96 mx-auto mt-4" />
        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          {[...Array(3)].map((_, i) => (
            <Card key={i} className="bg-muted/5">
              <CardContent className="p-4">
                <Skeleton className="h-12 w-full" />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
      <Card className="overflow-hidden max-w-5xl mx-auto">
        <CardContent className="p-8">
          <div className="space-y-6">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="space-y-3">
                <Skeleton className="h-8 w-[40%]" />
                <div className="space-y-2">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-[95%]" />
                  <Skeleton className="h-4 w-[90%]" />
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default function PlanPage() {
  return (
    <Suspense fallback={<PlanLoading />}>
      <PlanContent />
    </Suspense>
  )
} 