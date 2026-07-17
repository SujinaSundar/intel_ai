"use client";

/**
 * Chat Input.
 *
 * Modern AI chat input
 * for asking questions.
 */

import { useState, KeyboardEvent } from "react";

import {

    Send,

    Loader2

} from "lucide-react";

import {

    Button

} from "@/components/ui/button";

import {

    Textarea

} from "@/components/ui/textarea";

interface ChatInputProps {

    onSend: (

        message: string

    ) => void;

    disabled?: boolean;

}

export default function ChatInput({

    onSend,

    disabled = false

}: ChatInputProps) {

    // ---------------------------------------------------------
    // State
    // ---------------------------------------------------------

    const [

        message,

        setMessage

    ] = useState("");

    // ---------------------------------------------------------
    // Send
    // ---------------------------------------------------------

    function sendMessage() {

        const text = message.trim();

        if (!text) {

            return;

        }

        onSend(text);

        setMessage("");

    }

    // ---------------------------------------------------------
    // Enter Key
    // ---------------------------------------------------------

    function handleKeyDown(

        event: KeyboardEvent<HTMLTextAreaElement>

    ) {

        if (

            event.key === "Enter" &&

            !event.shiftKey

        ) {

            event.preventDefault();

            sendMessage();

        }

    }

    // ---------------------------------------------------------
    // UI
    // ---------------------------------------------------------

    return (

        <div className="mt-6 border-t border-border pt-6">

            <div className="rounded-2xl border border-border bg-card shadow-sm">

                <div className="flex items-end gap-4 p-4">

                    {/* ------------------------------------- */}
                    {/* Text Area */}
                    {/* ------------------------------------- */}

                    <Textarea

                        value={message}

                        onChange={(event) =>

                            setMessage(

                                event.target.value

                            )

                        }

                        onKeyDown={handleKeyDown}

                        placeholder="Ask anything about NIFTY 50 companies..."

                        disabled={disabled}

                        className="
                            min-h-[64px]
                            resize-none
                            border-0
                            bg-transparent
                            p-0
                            text-base
                            shadow-none
                            focus-visible:ring-0
                            focus-visible:ring-offset-0
                        "

                    />

                    {/* ------------------------------------- */}
                    {/* Send Button */}
                    {/* ------------------------------------- */}

                    <Button

                        size="icon"

                        className="h-11 w-11 rounded-xl"

                        disabled={

                            disabled ||

                            !message.trim()

                        }

                        onClick={sendMessage}

                    >

                        {

                            disabled

                                ? (

                                    <Loader2 className="h-5 w-5 animate-spin" />

                                )

                                : (

                                    <Send className="h-5 w-5" />

                                )

                        }

                    </Button>

                </div>

                {/* ------------------------------------- */}
                {/* Footer */}
                {/* ------------------------------------- */}

                <div className="flex items-center justify-between border-t border-border px-4 py-2 text-xs text-muted-foreground">

                    <span>

                        Press <strong>Enter</strong> to send

                    </span>

                    <span>

                        <strong>Shift + Enter</strong> for a new line

                    </span>

                </div>

            </div>

        </div>

    );

}