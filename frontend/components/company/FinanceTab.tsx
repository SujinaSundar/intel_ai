"use client";

/**
 * Finance Tab.
 *
 * Displays the latest
 * financial information
 * for a company.
 */

import Markdown from "@/components/common/Markdown";
import SectionCard from "@/components/common/SectionCard";
import EmptyState from "@/components/common/EmptyState";
import LoadingState from "@/components/common/LoadingState";


interface FinanceTabProps {

    company: string;

    loading: boolean;

    finance: string;

}


export default function FinanceTab({

    company,

    loading,

    finance

}: FinanceTabProps) {

    // ---------------------------------------------------------
    // Loading
    // ---------------------------------------------------------

    if (loading) {

        return <LoadingState />;

    }

    // ---------------------------------------------------------
    // Empty State
    // ---------------------------------------------------------

    if (!finance) {

        return (

            <EmptyState

                title="Financial Summary"

                description={`No financial information available for ${company}.`}

            />

        );

    }

    // ---------------------------------------------------------
    // UI
    // ---------------------------------------------------------

    return (

        <SectionCard

            title="Financial Summary"

            description={`Latest financial information for ${company}`}

        >

            <Markdown

                content={finance}

            />

        </SectionCard>

    );

}