"use client";

/**
 * About Page.
 *
 * Displays the architecture,
 * technology stack and
 * project features.
 */

import {

    Brain,

    Database,

    Network,

    Server,

    Layers3,

    Cpu

} from "lucide-react";

import {

    Card,

    CardContent,

    CardHeader,

    CardTitle

} from "@/components/ui/card";

export default function AboutPage() {

    return (

        <div className="space-y-8">

            {/* ------------------------------------------- */}
            {/* Hero */}
            {/* ------------------------------------------- */}

            <div>

                <h1 className="text-4xl font-bold">

                    🚀 Intel AI Trading Research Platform

                </h1>

                <p className="mt-3 text-lg text-slate-400">

                    An Agentic AI platform for intelligent
                    stock research, company comparison and
                    sector analysis using LangGraph,
                    Hybrid GraphRAG and Microservices.

                </p>

            </div>

            {/* ------------------------------------------- */}
            {/* Architecture */}
            {/* ------------------------------------------- */}

            <Card>

                <CardHeader>

                    <CardTitle className="flex items-center gap-2">

                        <Network size={22} />

                        Architecture

                    </CardTitle>

                </CardHeader>

                <CardContent>

                    <pre className="overflow-x-auto rounded-lg bg-slate-950 p-6 text-sm">

{`User
   │
   ▼
Next.js Frontend
   │
   ▼
Agent Service
   │
   ▼
LangGraph Supervisor
   │
   ├── Finance Agent
   ├── News Agent
   ├── Research Agent
   ├── Comparison Agent
   └── Sector Agent
   │
   ▼
Finance Service
News Service
Research Service
   │
   ▼
PostgreSQL
Neo4j
ChromaDB`}

                    </pre>

                </CardContent>

            </Card>

            {/* ------------------------------------------- */}
            {/* Technology Stack */}
            {/* ------------------------------------------- */}

            <Card>

                <CardHeader>

                    <CardTitle className="flex items-center gap-2">

                        <Cpu size={22} />

                        Technology Stack

                    </CardTitle>

                </CardHeader>

                <CardContent>

                    <div className="grid gap-4 md:grid-cols-2">

                        <div>

                            <h3 className="font-semibold">

                                Frontend

                            </h3>

                            <ul className="mt-2 list-disc pl-5 text-slate-300">

                                <li>Next.js 16</li>

                                <li>React</li>

                                <li>TypeScript</li>

                                <li>Tailwind CSS</li>

                                <li>shadcn/ui</li>

                            </ul>

                        </div>

                        <div>

                            <h3 className="font-semibold">

                                Backend

                            </h3>

                            <ul className="mt-2 list-disc pl-5 text-slate-300">

                                <li>FastAPI</li>

                                <li>LangGraph</li>

                                <li>LlamaIndex</li>

                                <li>Groq LLM</li>

                                <li>REST APIs</li>

                            </ul>

                        </div>

                        <div>

                            <h3 className="font-semibold">

                                Databases

                            </h3>

                            <ul className="mt-2 list-disc pl-5 text-slate-300">

                                <li>PostgreSQL</li>

                                <li>Neo4j</li>

                                <li>ChromaDB</li>

                            </ul>

                        </div>

                        <div>

                            <h3 className="font-semibold">

                                Deployment

                            </h3>

                            <ul className="mt-2 list-disc pl-5 text-slate-300">

                                <li>Docker</li>

                                <li>Docker Compose</li>

                                <li>Microservices</li>

                            </ul>

                        </div>

                    </div>

                </CardContent>

            </Card>

            {/* ------------------------------------------- */}
            {/* Features */}
            {/* ------------------------------------------- */}

            <Card>

                <CardHeader>

                    <CardTitle className="flex items-center gap-2">

                        <Layers3 size={22} />

                        Platform Features

                    </CardTitle>

                </CardHeader>

                <CardContent>

                    <div className="grid gap-3 md:grid-cols-2">

                        <div>✅ AI Research Copilot</div>

                        <div>✅ Company Explorer</div>

                        <div>✅ Compare Companies</div>

                        <div>✅ Sector Analysis</div>

                        <div>✅ Hybrid GraphRAG</div>

                        <div>✅ LangGraph Workflow</div>

                        <div>✅ MCP Architecture</div>

                        <div>✅ Multi-Agent System</div>

                    </div>

                </CardContent>

            </Card>

        </div>

    );

}