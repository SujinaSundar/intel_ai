"use client";

/**
 * Compare Result.
 *
 * Displays the AI-generated
 * comparison between two
 * companies.
 */

import Markdown from "@/components/common/Markdown";
import SectionCard from "@/components/common/SectionCard";
import EmptyState from "@/components/common/EmptyState";
import LoadingState from "@/components/common/LoadingState";

import InsightBanner from "@/components/dashboard/InsightBanner";
import InfoTile from "@/components/dashboard/InfoTile";

import {

    BarChart3,

    Brain,

    Newspaper,

    Trophy

} from "lucide-react";

interface CompareResultProps {

    companyOne: string;

    companyTwo: string;

    loading: boolean;

    result: string;

}

export default function CompareResult({

    companyOne,

    companyTwo,

    loading,

    result

}: CompareResultProps) {

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

                title="Ready to Compare"

                description="Choose two companies to generate an AI-powered comparison across finance, research and news."

            />

        );

    }

    // ---------------------------------------------------------
    // UI
    // ---------------------------------------------------------

    return (

        <div className="space-y-8">

            <InsightBanner

                title="Comparison Complete"

                description={`AI-generated comparison between ${companyOne} and ${companyTwo} using Finance, Research and News agents.`}

            />

            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

                <InfoTile

                    icon={<BarChart3 className="h-6 w-6" />}

                    title="Finance"

                    subtitle="Stock performance comparison"

                />

                <InfoTile

                    icon={<Brain className="h-6 w-6" />}

                    title="Research"

                    subtitle="Business strategy & products"

                />

                <InfoTile

                    icon={<Newspaper className="h-6 w-6" />}

                    title="News"

                    subtitle="Latest updates & sentiment"

                />

                <InfoTile

                    icon={<Trophy className="h-6 w-6" />}

                    title="AI Verdict"

                    subtitle="Overall comparison summary"

                />

            </div>

            <SectionCard

                title="Detailed AI Comparison"

                description={`Comprehensive comparison report for ${companyOne} and ${companyTwo}.`}

            >

                <Markdown

                    content={result}

                />

            </SectionCard>

        </div>

    );

}