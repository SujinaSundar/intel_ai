"use client";

/**
 * Feature Cards.
 *
 * Displays the core features
 * of the Intel AI Trading
 * Research Platform.
 */

import Link from "next/link";

import {
    Building2,
    BarChart3,
    Landmark,
    ArrowRight
} from "lucide-react";

const features = [

    {
        title: "Company Explorer",
        description:
            "Explore financial data, research insights and latest news for NIFTY 50 companies.",
        icon: Building2,
        href: "/company"
    },

    {
        title: "Compare Companies",
        description:
            "Compare two companies using financial metrics, research and AI-generated insights.",
        icon: BarChart3,
        href: "/compare"
    },

    {
        title: "Sector Analysis",
        description:
            "Analyze sectors such as IT, Banking, FMCG and Energy using AI.",
        icon: Landmark,
        href: "/sector"
    }

];

export default function FeatureCards() {

    return (

        <div className="mt-12 grid gap-6 md:grid-cols-3">

            {

                features.map((feature) => {

                    const Icon = feature.icon;

                    return (

                        <Link

                            key={feature.title}

                            href={feature.href}

                            className="group rounded-2xl border border-border bg-card p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-primary hover:shadow-xl"

                        >

                            <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">

                                <Icon className="h-6 w-6 text-primary" />

                            </div>

                            <h3 className="text-xl font-semibold">

                                {feature.title}

                            </h3>

                            <p className="mt-3 leading-7 text-muted-foreground">

                                {feature.description}

                            </p>

                            <div className="mt-6 flex items-center gap-2 font-medium text-primary">

                                Explore

                                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />

                            </div>

                        </Link>

                    );

                })

            }

        </div>

    );

}