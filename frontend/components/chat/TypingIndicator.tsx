"use client";

/**
 * Typing Indicator.
 *
 * Displays the AI typing
 * animation while waiting
 * for a response.
 */

import {

    Bot

} from "lucide-react";

export default function TypingIndicator() {

    return (

        <div className="mb-8 flex justify-start">

            <div className="flex max-w-5xl gap-4">

                {/* --------------------------------------- */}
                {/* Avatar */}
                {/* --------------------------------------- */}

                <div
                    className="
                        flex
                        h-11
                        w-11
                        shrink-0
                        items-center
                        justify-center
                        rounded-full
                        border
                        border-primary/20
                        bg-primary/10
                        text-primary
                        shadow-sm
                    "
                >

                    <Bot className="h-5 w-5" />

                </div>

                {/* --------------------------------------- */}
                {/* Bubble */}
                {/* --------------------------------------- */}

                <div
                    className="
                        rounded-2xl
                        border
                        border-border
                        bg-card
                        shadow-sm
                    "
                >

                    {/* Header */}

                    <div className="flex items-center justify-between border-b border-border px-5 py-3">

                        <span className="text-sm font-semibold text-foreground">

                            Intel AI

                        </span>

                        <span className="text-xs text-muted-foreground">

                            Thinking...

                        </span>

                    </div>

                    {/* Content */}

                    <div className="flex items-center gap-3 px-5 py-4">

                        <span
                            className="
                                h-2.5
                                w-2.5
                                animate-bounce
                                rounded-full
                                bg-primary
                            "
                        />

                        <span
                            className="
                                h-2.5
                                w-2.5
                                animate-bounce
                                rounded-full
                                bg-primary
                            "
                            style={{

                                animationDelay: "0.15s"

                            }}
                        />

                        <span
                            className="
                                h-2.5
                                w-2.5
                                animate-bounce
                                rounded-full
                                bg-primary
                            "
                            style={{

                                animationDelay: "0.30s"

                            }}
                        />

                        <span className="ml-2 text-sm text-muted-foreground">

                            Generating AI response...

                        </span>

                    </div>

                </div>

            </div>

        </div>

    );

}