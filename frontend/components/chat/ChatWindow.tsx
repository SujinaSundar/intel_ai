"use client";

/**
 * Chat Window.
 *
 * Main AI chat interface
 * for the Intel AI Trading
 * Research Platform.
 */

import {

    useEffect,

    useRef,

    useState

} from "react";

import {

    Brain,

    BarChart3,

    Building2,

    Landmark,

    Newspaper

} from "lucide-react";

import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";
import SuggestedQuestions from "./SuggestedQuestions";
import TypingIndicator from "./TypingIndicator";

import { askQuestion } from "@/services/agent.service";
import { Message } from "@/types/chat";

export default function ChatWindow() {

    // ---------------------------------------------------------
    // State
    // ---------------------------------------------------------

    const [

        messages,

        setMessages

    ] = useState<Message[]>([]);

    const [

        loading,

        setLoading

    ] = useState(false);

    // ---------------------------------------------------------
    // Auto Scroll
    // ---------------------------------------------------------

    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {

        messagesEndRef.current?.scrollIntoView({

            behavior: "smooth"

        });

    }, [

        messages,

        loading

    ]);

    // ---------------------------------------------------------
    // Send Question
    // ---------------------------------------------------------

    const handleSend = async (

        question: string

    ) => {

        const userMessage: Message = {

            id: crypto.randomUUID(),

            role: "user",

            content: question,

            createdAt: new Date()

        };

        // Build conversation history before updating state
        const history = [

            ...messages,

            userMessage,

        ].map(

            message => ({

                role: message.role,

                content: message.content,

            })

        );

        setMessages(

            previous => [

                ...previous,

                userMessage

            ]

        );

        setLoading(true);

        try {

            const answer = await askQuestion(

                question,

                history,

            );

            setMessages(

                previous => [

                    ...previous,

                    {

                        id: crypto.randomUUID(),

                        role: "assistant",

                        content: answer,

                        createdAt: new Date()

                    }

                ]

            );

        }

        catch {

            setMessages(

                previous => [

                    ...previous,

                    {

                        id: crypto.randomUUID(),

                        role: "assistant",

                        content:

                            "Unable to connect to the Agent Service.",

                        createdAt: new Date(),

                        error: true

                    }

                ]

            );

        }

        finally {

            setLoading(false);

        }

    };

    // ---------------------------------------------------------
    // UI
    // ---------------------------------------------------------

    return (

        <div className="mx-auto flex h-[calc(100vh-160px)] max-w-6xl flex-col">

            {/* -------------------------------------------------- */}
            {/* Welcome */}
            {/* -------------------------------------------------- */}

            {

                messages.length === 0 && (

                    <div className="mb-10 text-center">

                        <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-3xl bg-primary/10">

                            <Brain className="h-10 w-10 text-primary" />

                        </div>

                        <h1 className="text-5xl font-bold tracking-tight">

                            Intel AI

                        </h1>

                        <p className="mt-3 text-xl text-muted-foreground">

                            Multi-Agent Trading Research Platform

                        </p>

                        <p className="mx-auto mt-6 max-w-3xl text-base leading-8 text-muted-foreground">

                            Ask questions about NIFTY 50 companies,

                            compare businesses, explore sectors,

                            analyze financial data and generate

                            AI-powered investment research.

                        </p>

                        {/* -------------------------------------- */}
                        {/* Capabilities */}
                        {/* -------------------------------------- */}

                        <div className="mx-auto mt-10 grid max-w-5xl gap-4 md:grid-cols-2 xl:grid-cols-4">

                            <div className="rounded-2xl border border-border bg-card p-5 text-left shadow-sm">

                                <BarChart3 className="mb-3 h-6 w-6 text-primary" />

                                <h3 className="font-semibold">

                                    Financial Analysis

                                </h3>

                                <p className="mt-2 text-sm text-muted-foreground">

                                    Analyze prices, trends and market performance.

                                </p>

                            </div>

                            <div className="rounded-2xl border border-border bg-card p-5 text-left shadow-sm">

                                <Building2 className="mb-3 h-6 w-6 text-primary" />

                                <h3 className="font-semibold">

                                    Company Research

                                </h3>

                                <p className="mt-2 text-sm text-muted-foreground">

                                    Explore company fundamentals and business insights.

                                </p>

                            </div>

                            <div className="rounded-2xl border border-border bg-card p-5 text-left shadow-sm">

                                <Newspaper className="mb-3 h-6 w-6 text-primary" />

                                <h3 className="font-semibold">

                                    News Intelligence

                                </h3>

                                <p className="mt-2 text-sm text-muted-foreground">

                                    Stay updated with AI-powered news summaries.

                                </p>

                            </div>

                            <div className="rounded-2xl border border-border bg-card p-5 text-left shadow-sm">

                                <Landmark className="mb-3 h-6 w-6 text-primary" />

                                <h3 className="font-semibold">

                                    Sector Analysis

                                </h3>

                                <p className="mt-2 text-sm text-muted-foreground">

                                    Discover market trends across NIFTY sectors.

                                </p>

                            </div>

                        </div>

                    </div>

                )

            }

            {/* -------------------------------------------------- */}
            {/* Suggested Questions */}
            {/* -------------------------------------------------- */}

            {

                messages.length === 0 && (

                    <SuggestedQuestions

                        onSelect={handleSend}

                    />

                )

            }

            {/* -------------------------------------------------- */}
            {/* Messages */}
            {/* -------------------------------------------------- */}

            <div className="flex-1 overflow-y-auto py-6 pr-2">

                {

                    messages.map(

                        message => (

                            <ChatMessage

                                key={message.id}

                                message={message}

                            />

                        )

                    )

                }

                {

                    loading && (

                        <TypingIndicator />

                    )

                }

                {/* Auto Scroll */}

                <div ref={messagesEndRef} />

            </div>

            {/* -------------------------------------------------- */}
            {/* Input */}
            {/* -------------------------------------------------- */}

            <div className="sticky bottom-0 border-t border-border bg-background/95 py-5 backdrop-blur">

                <ChatInput

                    onSend={handleSend}

                    disabled={loading}

                />

            </div>

        </div>

    );

}