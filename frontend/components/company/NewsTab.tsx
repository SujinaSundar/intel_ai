"use client";

/**
 * News Tab.
 *
 * Displays the latest
 * company news.
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


interface NewsTabProps {

    company: string;

    loading: boolean;

    news: string;

}


export default function NewsTab({

    company,

    loading,

    news

}: NewsTabProps) {

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

    if (!news) {

        return (

            <Card className="mt-6">

                <CardContent className="p-6">

                    <p className="text-slate-400">

                        No recent news available for{" "}

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

                    Latest News

                </CardTitle>

                <p className="text-slate-400">

                    Recent developments related to {company}

                </p>

            </CardHeader>

            <CardContent>

                <Markdown

                    content={news}

                />

            </CardContent>

        </Card>

    );

}