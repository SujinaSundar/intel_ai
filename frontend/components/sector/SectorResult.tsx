"use client";

/**
 * Sector Result.
 *
 * Displays the AI-generated
 * sector analysis.
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

    if (!result) {

        return (

            <Card className="mt-6">

                <CardContent className="p-6">

                    <p className="text-slate-400">

                        Select a sector and click

                        <span className="font-semibold">

                            {" "}Analyze Sector

                        </span>

                        {" "}to generate an AI-powered analysis.

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

                    Sector Analysis

                </CardTitle>

                <p className="text-slate-400">

                    AI-generated insights for the selected sector.

                </p>

            </CardHeader>

            <CardContent>

                <Markdown

                    content={result}

                />

            </CardContent>

        </Card>

    );

}