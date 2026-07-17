"use client";

/**
 * Page Header.
 *
 * Shared page header used
 * throughout the application.
 */

import { ReactNode } from "react";

interface PageHeaderProps {

    title: string;

    description: string;

    icon?: ReactNode;

}

export default function PageHeader({

    title,

    description,

    icon

}: PageHeaderProps) {

    return (

        <header className="mb-10">

            <div className="flex flex-col gap-5 sm:flex-row sm:items-center">

                {/* ----------------------------------------- */}
                {/* Icon */}
                {/* ----------------------------------------- */}

                {

                    icon && (

                        <div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-border bg-primary/10 shadow-sm">

                            {icon}

                        </div>

                    )

                }

                {/* ----------------------------------------- */}
                {/* Title */}
                {/* ----------------------------------------- */}

                <div className="space-y-2">

                    <h1 className="text-4xl font-bold tracking-tight text-foreground">

                        {title}

                    </h1>

                    <p className="max-w-3xl text-base leading-7 text-muted-foreground">

                        {description}

                    </p>

                </div>

            </div>

        </header>

    );

}