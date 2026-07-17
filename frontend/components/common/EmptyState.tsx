"use client";

/**
 * Empty State.
 *
 * Shared empty state
 * component used across
 * the application.
 */

import {

    SearchX

} from "lucide-react";

import SectionCard from "./SectionCard";


interface EmptyStateProps {

    title: string;

    description: string;

}


export default function EmptyState({

    title,

    description

}: EmptyStateProps) {

    return (

        <SectionCard

            title={title}

        >

            <div className="flex flex-col items-center justify-center py-10 text-center">

                <div className="mb-4 rounded-full bg-muted p-4">

                    <SearchX className="h-8 w-8 text-muted-foreground" />

                </div>

                <p className="text-lg font-medium">

                    {description}

                </p>

            </div>

        </SectionCard>

    );

}