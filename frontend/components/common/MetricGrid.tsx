"use client";

/**
 * Metric Grid.
 *
 * Responsive layout for
 * multiple Stat Cards.
 */

import { ReactNode } from "react";

interface MetricGridProps {

    children: ReactNode;

}

export default function MetricGrid({

    children

}: MetricGridProps) {

    return (

        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">

            {children}

        </div>

    );

}