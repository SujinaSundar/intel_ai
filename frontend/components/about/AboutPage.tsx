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

    Cpu,

    Database,

    Layers3,

    Network,

    Server,

    Boxes,

    Sparkles

} from "lucide-react";

import PageHeader from "@/components/common/PageHeader";
import InsightBanner from "@/components/dashboard/InsightBanner";
import InfoTile from "@/components/dashboard/InfoTile";

import {

    Card,

    CardContent,

    CardHeader,

    CardTitle

} from "@/components/ui/card";

export default function AboutPage() {

    return (

        <div className="mx-auto max-w-7xl space-y-8">

            {/* ------------------------------------------------ */}
            {/* Page Header */}
            {/* ------------------------------------------------ */}

            <PageHeader

                title="Intel AI Trading Research Platform"

                description="A production-style multi-agent AI platform for intelligent stock research, company comparison and sector analysis."

                icon={

                    <Brain className="h-8 w-8 text-primary" />

                }

            />

            {/* ------------------------------------------------ */}
            {/* Insight */}
            {/* ------------------------------------------------ */}

            <InsightBanner

                title="Production-Style AI Architecture"

                description="Built using LangGraph, Hybrid GraphRAG, FastAPI microservices and modern frontend technologies to deliver AI-powered trading research."

            />

            {/* ------------------------------------------------ */}
            {/* Project Statistics */}
            {/* ------------------------------------------------ */}

            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

                <InfoTile

                    icon={<Brain className="h-6 w-6" />}

                    title="5 AI Agents"

                    subtitle="Finance, News, Research, Comparison & Sector"

                />

                <InfoTile

                    icon={<Server className="h-6 w-6" />}

                    title="3 Services"

                    subtitle="Finance, News & Research"

                />

                <InfoTile

                    icon={<Database className="h-6 w-6" />}

                    title="3 Databases"

                    subtitle="PostgreSQL, Neo4j & ChromaDB"

                />

                <InfoTile

                    icon={<Sparkles className="h-6 w-6" />}

                    title="AI Powered"

                    subtitle="LangGraph + Hybrid GraphRAG"

                />

            </div>

            {/* ------------------------------------------------ */}
            {/* Architecture */}
            {/* ------------------------------------------------ */}

            <Card className="border-border shadow-sm">

                <CardHeader>

                    <CardTitle className="flex items-center gap-2">

                        <Network className="h-5 w-5 text-primary" />

                        System Architecture

                    </CardTitle>

                </CardHeader>

                <CardContent>

<pre className="overflow-x-auto rounded-xl bg-muted p-6 text-sm leading-7">

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

            {/* ------------------------------------------------ */}
            {/* Technology Stack */}
            {/* ------------------------------------------------ */}

            <Card className="border-border shadow-sm">

                <CardHeader>

                    <CardTitle className="flex items-center gap-2">

                        <Cpu className="h-5 w-5 text-primary" />

                        Technology Stack

                    </CardTitle>

                </CardHeader>

                <CardContent>

                    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

                        <InfoTile

                            icon={<Boxes className="h-6 w-6" />}

                            title="Frontend"

                            subtitle="Next.js • React • TypeScript • Tailwind CSS"

                        />

                        <InfoTile

                            icon={<Server className="h-6 w-6" />}

                            title="Backend"

                            subtitle="FastAPI • LangGraph • Groq • LlamaIndex"

                        />

                        <InfoTile

                            icon={<Database className="h-6 w-6" />}

                            title="Databases"

                            subtitle="PostgreSQL • Neo4j • ChromaDB"

                        />

                        <InfoTile

                            icon={<Sparkles className="h-6 w-6" />}

                            title="Deployment"

                            subtitle="Docker • Docker Compose • Microservices"

                        />

                    </div>

                </CardContent>

            </Card>

            {/* ------------------------------------------------ */}
            {/* Platform Features */}
            {/* ------------------------------------------------ */}

            <Card className="border-border shadow-sm">

                <CardHeader>

                    <CardTitle className="flex items-center gap-2">

                        <Layers3 className="h-5 w-5 text-primary" />

                        Platform Features

                    </CardTitle>

                </CardHeader>

                <CardContent>

                    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">

                        <InfoTile

                            icon={<Brain className="h-5 w-5" />}

                            title="AI Research"

                            subtitle="Research Copilot"

                        />

                        <InfoTile

                            icon={<Database className="h-5 w-5" />}

                            title="Company Explorer"

                            subtitle="Company Insights"

                        />

                        <InfoTile

                            icon={<Network className="h-5 w-5" />}

                            title="Compare"

                            subtitle="AI Company Comparison"

                        />

                        <InfoTile

                            icon={<Cpu className="h-5 w-5" />}

                            title="Sector Analysis"

                            subtitle="Industry Intelligence"

                        />

                        <InfoTile

                            icon={<Sparkles className="h-5 w-5" />}

                            title="Hybrid GraphRAG"

                            subtitle="Knowledge + Vector Search"

                        />

                        <InfoTile

                            icon={<Server className="h-5 w-5" />}

                            title="LangGraph"

                            subtitle="Agent Orchestration"

                        />

                        <InfoTile

                            icon={<Boxes className="h-5 w-5" />}

                            title="MCP"

                            subtitle="Model Context Protocol"

                        />

                        <InfoTile

                            icon={<Layers3 className="h-5 w-5" />}

                            title="Multi-Agent"

                            subtitle="Production Architecture"

                        />

                    </div>

                </CardContent>

            </Card>

        </div>

    );

}