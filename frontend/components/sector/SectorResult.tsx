"use client";

/**
 * Sector Result.
 *
 * Displays the AI-generated
 * sector analysis.
 */

import Markdown from "@/components/common/Markdown";
import SectionCard from "@/components/common/SectionCard";
import EmptyState from "@/components/common/EmptyState";
import LoadingState from "@/components/common/LoadingState";

import InsightBanner from "@/components/dashboard/InsightBanner";
import InfoTile from "@/components/dashboard/InfoTile";

import {

    Landmark,

    Building2,

    TrendingUp,

    Brain

} from "lucide-react";

interface SectorResultProps {

    loading: boolean;

    result: string;

}

export default function SectorResult({

    loading,

    result

}: SectorResultProps) {

    // ---------------------------------------------------------
    // Loading
    // ---------------------------------------------------------

    if (loading) {

        return <LoadingState />;

    }

    // ---------------------------------------------------------
    // Empty State
    // ---------------------------------------------------------

    if (!result) {

        return (

            <EmptyState

                title="Ready for Sector Analysis"

                description="Select a NIFTY 50 sector and click 'Analyze Sector' to generate AI-powered insights."

            />

        );

    }

    // ---------------------------------------------------------
    // UI
    // ---------------------------------------------------------

    return (

        <div className="space-y-8">

            {/* --------------------------------------------- */}
            {/* AI Insight */}
            {/* --------------------------------------------- */}

            <InsightBanner

                title="Sector Analysis Complete"

                description="Intel AI analyzed the selected sector using Finance, Research and News agents to generate a comprehensive report."

            />

            {/* --------------------------------------------- */}
            {/* Analysis Overview */}
            {/* --------------------------------------------- */}

            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

                <InfoTile

                    icon={

                        <Landmark className="h-6 w-6" />

                    }

                    title="Sector Overview"

                    subtitle="Industry summary and outlook"

                />

                <InfoTile

                    icon={

                        <Building2 className="h-6 w-6" />

                    }

                    title="Companies"

                    subtitle="Leading NIFTY 50 companies"

                />

                <InfoTile

                    icon={

                        <TrendingUp className="h-6 w-6" />

                    }

                    title="Market Performance"

                    subtitle="Financial trends and activity"

                />

                <InfoTile

                    icon={

                        <Brain className="h-6 w-6" />

                    }

                    title="AI Insights"

                    subtitle="Research and sentiment analysis"

                />

            </div>

            {/* --------------------------------------------- */}
            {/* Detailed Analysis */}
            {/* --------------------------------------------- */}

            <SectionCard

                title="Detailed Sector Analysis"

                description="Comprehensive AI-generated analysis of the selected NIFTY 50 sector."

            >

                <Markdown

                    content={result}

                />

            </SectionCard>

        </div>

    );

}