"use client";

/**
 * Research Tab.
 *
 * Displays AI-generated
 * research insights.
 */

import Markdown from "@/components/common/Markdown";
import SectionCard from "@/components/common/SectionCard";
import EmptyState from "@/components/common/EmptyState";
import LoadingState from "@/components/common/LoadingState";

interface ResearchTabProps {

    company: string;

    loading: boolean;

    research: string;

}

export default function ResearchTab({

    company,

    loading,

    research

}: ResearchTabProps) {

    if (loading) {

        return <LoadingState />;

    }

    if (!research) {

        return (

            <EmptyState

                title="Research"

                description={`No research available for ${company}.`}

            />

        );

    }

    return (

        <SectionCard

            title="Research"

            description={`AI-generated research summary for ${company}`}

        >

            <Markdown content={research} />

        </SectionCard>

    );

}