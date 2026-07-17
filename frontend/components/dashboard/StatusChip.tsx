"use client";

interface StatusChipProps {

    text: string;

}

export default function StatusChip({

    text

}: StatusChipProps) {

    return (

        <span className="inline-flex items-center rounded-full bg-green-500/15 px-3 py-1 text-sm font-medium text-green-400">

            ● {text}

        </span>

    );

}