"use client";

/**
 * Insight Banner.
 *
 * Shared AI insight banner
 * displayed throughout
 * the application.
 */

import {

    Brain,

    Sparkles

} from "lucide-react";

interface InsightBannerProps {

    title: string;

    description: string;

}

export default function InsightBanner({

    title,

    description

}: InsightBannerProps) {

    return (

        <div
            className="
                relative
                overflow-hidden
                rounded-2xl
                border
                border-primary/20
                bg-primary/5
                p-6
                shadow-sm
            "
        >

            {/* ----------------------------------------- */}
            {/* Decorative Background */}
            {/* ----------------------------------------- */}

            <div className="absolute right-0 top-0 opacity-10">

                <Sparkles className="h-32 w-32 text-primary" />

            </div>

            {/* ----------------------------------------- */}
            {/* Content */}
            {/* ----------------------------------------- */}

            <div className="relative flex items-start gap-5">

                {/* Icon */}

                <div
                    className="
                        flex
                        h-14
                        w-14
                        shrink-0
                        items-center
                        justify-center
                        rounded-2xl
                        bg-primary/10
                        text-primary
                    "
                >

                    <Brain className="h-7 w-7" />

                </div>

                {/* Text */}

                <div className="space-y-2">

                    <h3 className="text-xl font-semibold tracking-tight text-foreground">

                        {title}

                    </h3>

                    <p className="max-w-4xl leading-7 text-muted-foreground">

                        {description}

                    </p>

                </div>

            </div>

        </div>

    );

}