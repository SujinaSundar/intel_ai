"use client";

/**
 * Section Card.
 *
 * Shared card component
 * used throughout the
 * application.
 */

import { ReactNode } from "react";

import {

    Card,

    CardContent,

    CardHeader,

    CardTitle

} from "@/components/ui/card";

interface SectionCardProps {

    title: string;

    description?: string;

    icon?: ReactNode;

    children: ReactNode;

}

export default function SectionCard({

    title,

    description,

    icon,

    children

}: SectionCardProps) {

    return (

        <Card className="overflow-hidden rounded-2xl border-border bg-card shadow-sm transition-all duration-300 hover:shadow-lg">

            {/* ----------------------------------------- */}
            {/* Header */}
            {/* ----------------------------------------- */}

            <CardHeader className="border-b border-border bg-muted/30 p-6">

                <div className="flex items-center gap-3">

                    {

                        icon && (

                            <div className="text-primary">

                                {icon}

                            </div>

                        )

                    }

                    <CardTitle className="text-2xl font-semibold tracking-tight">

                        {title}

                    </CardTitle>

                </div>

                {

                    description && (

                        <p className="pt-1 text-sm leading-6 text-muted-foreground">

                            {description}

                        </p>

                    )

                }

            </CardHeader>

            {/* ----------------------------------------- */}
            {/* Content */}
            {/* ----------------------------------------- */}

            <CardContent className="p-8">

                {children}

            </CardContent>

        </Card>

    );

}