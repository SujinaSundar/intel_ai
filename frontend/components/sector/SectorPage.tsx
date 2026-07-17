"use client";

/**
 * Sector Page.
 *
 * AI-powered sector analysis
 * for NIFTY 50 sectors.
 */

import { useState } from "react";

import { Landmark } from "lucide-react";

import PageHeader from "@/components/common/PageHeader";
import InsightBanner from "@/components/dashboard/InsightBanner";

import SectorSelector from "./SectorSelector";
import SectorResult from "./SectorResult";

export default function SectorPage() {

    // ---------------------------------------------------------
    // State
    // ---------------------------------------------------------

    const [

        result,

        setResult

    ] = useState("");

    const [

        loading,

        setLoading

    ] = useState(false);

    // ---------------------------------------------------------
    // UI
    // ---------------------------------------------------------

    return (

        <div className="mx-auto max-w-7xl space-y-8">

            {/* --------------------------------------------- */}
            {/* Page Header */}
            {/* --------------------------------------------- */}

            <PageHeader

                title="Sector Analysis"

                description="Analyze NIFTY 50 sectors using AI-powered financial, research and news intelligence."

                icon={

                    <Landmark className="h-8 w-8 text-primary" />

                }

            />

            {/* --------------------------------------------- */}
            {/* AI Insight */}
            {/* --------------------------------------------- */}

            <InsightBanner

                title="AI-Powered Sector Intelligence"

                description="Sector Analysis combines Finance, Research and News agents to provide a comprehensive overview of companies within a selected sector."

            />

            {/* --------------------------------------------- */}
            {/* Sector Selector */}
            {/* --------------------------------------------- */}

            <SectorSelector

                loading={loading}

                setLoading={setLoading}

                setResult={setResult}

            />

            {/* --------------------------------------------- */}
            {/* Result */}
            {/* --------------------------------------------- */}

            <SectorResult

                loading={loading}

                result={result}

            />

        </div>

    );

}