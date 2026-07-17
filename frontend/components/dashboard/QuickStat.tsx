"use client";

/**
 * Quick Stat.
 *
 * Small dashboard card
 * displaying a metric.
 */

import { ReactNode } from "react";

interface QuickStatProps {

    title: string;

    value: string;

    icon: ReactNode;

}

export default function QuickStat({

    title,

    value,

    icon

}: QuickStatProps) {

    return (

        <div className="rounded-2xl border border-border bg-card p-5 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">

            <div className="flex items-center justify-between">

                <span className="text-sm text-muted-foreground">

                    {title}

                </span>

                <div className="text-primary">

                    {icon}

                </div>

            </div>

            <h2 className="mt-4 text-3xl font-bold">

                {value}

            </h2>

        </div>

    );

}