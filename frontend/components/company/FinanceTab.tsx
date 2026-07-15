"use client";

/**
 * Finance Tab.
 *
 * Displays the latest
 * financial information
 * for a company.
 */

import Markdown from "@/components/common/Markdown";
import { Skeleton } from "@/components/ui/skeleton";

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

    if (!finance) {

        return (

            <div className="mt-6 rounded-lg border p-6">

                <p className="text-slate-400">

                    No financial information available for{" "}

                    <span className="font-semibold">

                        {company}

                    </span>.

                </p>

            </div>

        );

    }

    // ---------------------------------------------------------
    // UI
    // ---------------------------------------------------------

    return (

        <div className="mt-6 rounded-lg border bg-card p-6">

            <div className="mb-6">

                <h2 className="text-2xl font-semibold">

                    Financial Summary

                </h2>

                <p className="text-sm text-slate-400">

                    Latest financial information for {company}

                </p>

            </div>

            <Markdown

                content={finance}

            />

        </div>

    );

}