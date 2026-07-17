"use client";

/**
 * Chat Message.
 *
 * Displays user and assistant
 * messages with a modern
 * conversational UI.
 */

import Markdown from "@/components/common/Markdown";

import { cn } from "@/lib/utils";
import { Message } from "@/types/chat";

import {

    AlertCircle,

    Bot,

    User

} from "lucide-react";

interface ChatMessageProps {

    message: Message;

}

export default function ChatMessage({

    message

}: ChatMessageProps) {

    const isUser = message.role === "user";

    return (

        <div
            className={cn(
                "mb-8 flex w-full",
                isUser
                    ? "justify-end"
                    : "justify-start"
            )}
        >

            <div
                className={cn(
                    "flex w-full max-w-5xl gap-4",
                    isUser
                        ? "flex-row-reverse"
                        : "flex-row"
                )}
            >

                {/* --------------------------------------- */}
                {/* Avatar */}
                {/* --------------------------------------- */}

                <div
                    className={cn(
                        "flex h-11 w-11 shrink-0 items-center justify-center rounded-full border shadow-sm transition-all",

                        isUser
                            ? "border-primary bg-primary text-primary-foreground"

                            : message.error

                                ? "border-red-500/30 bg-red-500/10 text-red-500"

                                : "border-primary/20 bg-primary/10 text-primary"
                    )}
                >

                    {

                        isUser

                            ? (

                                <User className="h-5 w-5" />

                            )

                            : message.error

                                ? (

                                    <AlertCircle className="h-5 w-5" />

                                )

                                : (

                                    <Bot className="h-5 w-5" />

                                )

                    }

                </div>

                {/* --------------------------------------- */}
                {/* Message */}
                {/* --------------------------------------- */}

                <div
                    className={cn(
                        "max-w-[85%] rounded-2xl border shadow-sm transition-all",

                        isUser

                            ? "border-primary bg-primary text-primary-foreground"

                            : message.error

                                ? "border-red-500/30 bg-red-500/5"

                                : "border-border bg-card"
                    )}
                >

                    {/* Header */}

                    <div
                        className={cn(
                            "flex items-center justify-between border-b px-5 py-3",

                            isUser

                                ? "border-primary-foreground/20"

                                : "border-border"
                        )}
                    >

                        <span
                            className={cn(
                                "text-sm font-semibold",

                                isUser

                                    ? "text-primary-foreground"

                                    : message.error

                                        ? "text-red-500"

                                        : "text-foreground"
                            )}
                        >

                            {

                                isUser

                                    ? "You"

                                    : message.error

                                        ? "System"

                                        : "Intel AI"

                            }

                        </span>

                        {/* Future Timestamp */}

                        <span
                            className={cn(
                                "text-xs",

                                isUser

                                    ? "text-primary-foreground/70"

                                    : "text-muted-foreground"
                            )}
                        >

                            Just now

                        </span>

                    </div>

                    {/* Content */}

                    <div className="px-5 py-4">

                        {

                            isUser

                                ? (

                                    <p className="whitespace-pre-wrap leading-7">

                                        {message.content}

                                    </p>

                                )

                                : (

                                    <Markdown

                                        content={message.content}

                                    />

                                )

                        }

                    </div>

                </div>

            </div>

        </div>

    );

}