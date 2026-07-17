"use client";

/**
 * Stat Card.
 *
 * Displays a single
 * financial metric.
 */

import { ReactNode } from "react";

interface StatCardProps {

    label: string;

    value: string | number;

    icon?: ReactNode;

    color?: string;

}

export default function StatCard({

    label,

    value,

    icon,

    color = "text-primary"

}: StatCardProps) {

    return (

        <div className="rounded-2xl border border-border bg-card p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">

            <div className="flex items-center justify-between">

                <span className="text-sm text-muted-foreground">

                    {label}

                </span>

                {

                    icon && (

                        <div className={color}>

                            {icon}

                        </div>

                    )

                }

            </div>

            <div className="mt-4">

                <p className="text-3xl font-bold tracking-tight">

                    {value}

                </p>

            </div>

        </div>

    );

}