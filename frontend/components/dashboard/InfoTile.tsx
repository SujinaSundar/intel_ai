"use client";

/**
 * Info Tile.
 *
 * Reusable dashboard tile
 * used for statistics,
 * features and summaries.
 */

import { ReactNode } from "react";

interface InfoTileProps {

    icon: ReactNode;

    title: string;

    subtitle: string;

}

export default function InfoTile({

    icon,

    title,

    subtitle

}: InfoTileProps) {

    return (

        <div
            className="
                group
                flex
                h-full
                flex-col
                rounded-2xl
                border
                border-border
                bg-card
                p-6
                shadow-sm
                transition-all
                duration-300
                hover:-translate-y-1
                hover:shadow-lg
            "
        >

            {/* ----------------------------------------- */}
            {/* Icon */}
            {/* ----------------------------------------- */}

            <div
                className="
                    mb-5
                    flex
                    h-12
                    w-12
                    items-center
                    justify-center
                    rounded-xl
                    bg-primary/10
                    text-primary
                    transition-colors
                    duration-300
                    group-hover:bg-primary
                    group-hover:text-primary-foreground
                "
            >

                {icon}

            </div>

            {/* ----------------------------------------- */}
            {/* Title */}
            {/* ----------------------------------------- */}

            <h3 className="text-lg font-semibold tracking-tight text-foreground">

                {title}

            </h3>

            {/* ----------------------------------------- */}
            {/* Subtitle */}
            {/* ----------------------------------------- */}

            <p className="mt-2 flex-1 text-sm leading-6 text-muted-foreground">

                {subtitle}

            </p>

        </div>

    );

}