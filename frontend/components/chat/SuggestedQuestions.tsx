"use client";

/**
 * Suggested Questions.
 *
 * Displays AI prompt cards
 * to help users get started.
 */

import {

    ArrowRight,

    BarChart3,

    Landmark,

    Newspaper,

    Sparkles,

    TrendingUp

} from "lucide-react";

interface Props {

    onSelect: (

        question: string

    ) => void;

}

const questions = [

    {

        title: "Should I invest in Infosys?",

        subtitle: "AI-powered investment research and financial analysis.",

        icon: TrendingUp,

        question: "Should I invest in Infosys?"

    },

    {

        title: "Compare Infosys and TCS",

        subtitle: "Compare financial performance, news and business strategy.",

        icon: BarChart3,

        question: "Compare Infosys and TCS"

    },

    {

        title: "Latest news about Reliance",

        subtitle: "Summarize recent company news and market sentiment.",

        icon: Newspaper,

        question: "Latest news about Reliance"

    },

    {

        title: "Analyze the IT Sector",

        subtitle: "Explore market trends and AI-generated sector insights.",

        icon: Landmark,

        question: "Analyze the IT sector"

    }

];

export default function SuggestedQuestions({

    onSelect

}: Props) {

    return (

        <section className="mb-10">

            {/* ----------------------------------------- */}
            {/* Header */}
            {/* ----------------------------------------- */}

            <div className="mb-6 flex items-center gap-3">

                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/10 text-primary">

                    <Sparkles className="h-6 w-6" />

                </div>

                <div>

                    <h2 className="text-xl font-semibold tracking-tight">

                        Get Started with AI

                    </h2>

                    <p className="text-sm text-muted-foreground">

                        Choose a question below or ask your own.

                    </p>

                </div>

            </div>

            {/* ----------------------------------------- */}
            {/* Cards */}
            {/* ----------------------------------------- */}

            <div className="grid gap-5 md:grid-cols-2">

                {

                    questions.map((item) => {

                        const Icon = item.icon;

                        return (

                            <button

                                key={item.title}

                                type="button"

                                onClick={() => onSelect(item.question)}

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
                                    text-left
                                    shadow-sm
                                    transition-all
                                    duration-300
                                    hover:-translate-y-1
                                    hover:border-primary/40
                                    hover:shadow-lg
                                "

                            >

                                {/* Top */}

                                <div className="flex items-center justify-between">

                                    <div
                                        className="
                                            flex
                                            h-12
                                            w-12
                                            items-center
                                            justify-center
                                            rounded-xl
                                            bg-primary/10
                                            text-primary
                                            transition-all
                                            duration-300
                                            group-hover:bg-primary
                                            group-hover:text-primary-foreground
                                        "
                                    >

                                        <Icon className="h-5 w-5" />

                                    </div>

                                    <ArrowRight
                                        className="
                                            h-5
                                            w-5
                                            text-muted-foreground
                                            transition-transform
                                            duration-300
                                            group-hover:translate-x-1
                                        "
                                    />

                                </div>

                                {/* Content */}

                                <div className="mt-6 flex-1">

                                    <h3 className="text-lg font-semibold">

                                        {item.title}

                                    </h3>

                                    <p className="mt-2 text-sm leading-6 text-muted-foreground">

                                        {item.subtitle}

                                    </p>

                                </div>

                                {/* Footer */}

                                <div className="mt-6 text-sm font-medium text-primary">

                                    Ask AI →

                                </div>

                            </button>

                        );

                    })

                }

            </div>

        </section>

    );

}