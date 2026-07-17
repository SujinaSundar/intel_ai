"use client";

/**
 * Overview Tab.
 *
 * Displays an AI-powered
 * overview of the selected
 * company.
 */

import Markdown from "@/components/common/Markdown";
import SectionCard from "@/components/common/SectionCard";
import LoadingState from "@/components/common/LoadingState";

import {
    Card,
    CardContent
} from "@/components/ui/card";

import {
    Building2,
    Newspaper,
    TrendingUp,
    Brain
} from "lucide-react";

interface OverviewTabProps {

    company: string;

    loading: boolean;

    finance: string;

    research: string;

    news: string;

}

export default function OverviewTab({

    company,

    loading,

    finance,

    research,

    news

}: OverviewTabProps) {

    // ---------------------------------------------------------
    // Loading
    // ---------------------------------------------------------

    if (loading) {

        return <LoadingState />;

    }

    // ---------------------------------------------------------
    // UI
    // ---------------------------------------------------------

    return (

        <div className="mt-6 space-y-8">

            {/* ------------------------------------------------ */}
            {/* Hero */}
            {/* ------------------------------------------------ */}

            <Card className="overflow-hidden border-border bg-card shadow-md">

                <CardContent className="flex items-center gap-5 p-8">

                    <div className="rounded-2xl bg-primary/10 p-4">

                        <Building2 className="h-10 w-10 text-primary" />

                    </div>

                    <div>

                        <h1 className="text-4xl font-bold tracking-tight">

                            {company}

                        </h1>

                        <p className="mt-2 text-muted-foreground">

                            AI-powered company overview combining financial performance,

                            business research and latest news.

                        </p>

                    </div>

                </CardContent>

            </Card>

            {/* ------------------------------------------------ */}
            {/* Financial Summary */}
            {/* ------------------------------------------------ */}

            <SectionCard

                title="📈 Financial Summary"

                description="Latest stock performance and financial overview."

            >

                <Markdown

                    content={finance}

                />

            </SectionCard>

            {/* ------------------------------------------------ */}
            {/* Research */}
            {/* ------------------------------------------------ */}

            <SectionCard

                title="🧠 AI Research Highlights"

                description="Business overview, products, partnerships and strategic insights."

            >

                <Markdown

                    content={research}

                />

            </SectionCard>

            {/* ------------------------------------------------ */}
            {/* News */}
            {/* ------------------------------------------------ */}

            <SectionCard

                title="📰 Latest News"

                description="Recent news and AI-generated news summary."

            >

                <Markdown

                    content={news}

                />

            </SectionCard>

        </div>

    );

}