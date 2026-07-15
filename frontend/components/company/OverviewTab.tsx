"use client";

/**
 * Overview Tab.
 *
 * Displays an overview
 * of the selected company.
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

        return (

            <div className="space-y-6 mt-6">

                <Skeleton className="h-28 rounded-xl" />

                <Skeleton className="h-48 rounded-xl" />

                <Skeleton className="h-48 rounded-xl" />

                <Skeleton className="h-48 rounded-xl" />

            </div>

        );

    }

    // ---------------------------------------------------------
    // UI
    // ---------------------------------------------------------

    return (

        <div className="space-y-6 mt-6">

            {/* ------------------------------------------- */}
            {/* Company Header */}
            {/* ------------------------------------------- */}

            <Card className="border-slate-700 bg-slate-900/60">

                <CardContent className="flex items-center gap-4 p-8">

                    <div className="rounded-xl bg-blue-500/20 p-3">

                        <Building2 className="h-8 w-8 text-blue-400" />

                    </div>

                    <div>

                        <h1 className="text-3xl font-bold">

                            {company}

                        </h1>

                        <p className="text-slate-400">

                            AI-powered company overview

                        </p>

                    </div>

                </CardContent>

            </Card>

            {/* ------------------------------------------- */}
            {/* Financial Summary */}
            {/* ------------------------------------------- */}

            <Card className="border-slate-700 bg-slate-900/60">

                <CardHeader>

                    <CardTitle className="flex items-center gap-2">

                        <TrendingUp className="h-5 w-5" />

                        Financial Summary

                    </CardTitle>

                </CardHeader>

                <CardContent>

                    <Markdown

                        content={finance}

                    />

                </CardContent>

            </Card>

            {/* ------------------------------------------- */}
            {/* Research */}
            {/* ------------------------------------------- */}

            <Card className="border-slate-700 bg-slate-900/60">

                <CardHeader>

                    <CardTitle className="flex items-center gap-2">

                        <Brain className="h-5 w-5" />

                        Research Highlights

                    </CardTitle>

                </CardHeader>

                <CardContent>

                    <Markdown

                        content={research}

                    />

                </CardContent>

            </Card>

            {/* ------------------------------------------- */}
            {/* News */}
            {/* ------------------------------------------- */}

            <Card className="border-slate-700 bg-slate-900/60">

                <CardHeader>

                    <CardTitle className="flex items-center gap-2">

                        <Newspaper className="h-5 w-5" />

                        Latest News

                    </CardTitle>

                </CardHeader>

                <CardContent>

                    <Markdown

                        content={news}

                    />

                </CardContent>

            </Card>

        </div>

    );

}