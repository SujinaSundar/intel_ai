"use client";

/**
 * Research Tab.
 *
 * Displays research
 * insights for the
 * selected company.
 */

import Markdown from "@/components/common/Markdown";

import {
    Card,
    CardContent,
    CardHeader,
    CardTitle
} from "@/components/ui/card";

import {
    Skeleton
} from "@/components/ui/skeleton";


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

    // ---------------------------------------------------------
    // Loading
    // ---------------------------------------------------------

    if (loading) {

        return (

            <div className="mt-6 space-y-4">

                <Skeleton className="h-6 w-52" />

                <Skeleton className="h-4 w-full" />

                <Skeleton className="h-4 w-full" />

                <Skeleton className="h-4 w-5/6" />

                <Skeleton className="h-4 w-4/6" />

            </div>

        );

    }

    // ---------------------------------------------------------
    // Empty State
    // ---------------------------------------------------------

    if (!research) {

        return (

            <Card className="mt-6">

                <CardContent className="p-6">

                    <p className="text-slate-400">

                        No research available for{" "}

                        <span className="font-semibold">

                            {company}

                        </span>.

                    </p>

                </CardContent>

            </Card>

        );

    }

    // ---------------------------------------------------------
    // UI
    // ---------------------------------------------------------

    return (

        <Card className="mt-6 border-slate-700 bg-slate-900/60 shadow-lg">

            <CardHeader>

                <CardTitle className="text-3xl">

                    Research Summary

                </CardTitle>

                <p className="text-slate-400">

                    AI-generated research for {company}

                </p>

            </CardHeader>

            <CardContent>

                <Markdown

                    content={research}

                />

            </CardContent>

        </Card>

    );

}