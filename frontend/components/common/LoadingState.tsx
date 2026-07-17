"use client";

/**
 * Loading State.
 *
 * Shared loading skeleton
 * used across the
 * application.
 */

import {

    Skeleton

} from "@/components/ui/skeleton";


export default function LoadingState() {

    return (

        <div className="space-y-4 py-6">

            <Skeleton className="h-8 w-48 rounded-lg" />

            <Skeleton className="h-4 w-full rounded-lg" />

            <Skeleton className="h-4 w-full rounded-lg" />

            <Skeleton className="h-4 w-5/6 rounded-lg" />

            <Skeleton className="h-4 w-2/3 rounded-lg" />

        </div>

    );

}