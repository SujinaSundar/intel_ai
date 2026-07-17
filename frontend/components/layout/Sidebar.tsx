"use client";

/**
 * Sidebar.
 *
 * Main navigation for the
 * Intel AI Trading Research
 * Platform.
 */

import Link from "next/link";
import { usePathname } from "next/navigation";

import {

    BarChart3,

    Bot,

    Building2,

    ChevronRight,

    Info,

    Landmark,

    Sparkles

} from "lucide-react";

import { cn } from "@/lib/utils";

const menuItems = [

    {

        title: "AI Assistant",

        href: "/",

        icon: Bot

    },

    {

        title: "Company Explorer",

        href: "/company",

        icon: Building2

    },

    {

        title: "Compare Companies",

        href: "/compare",

        icon: BarChart3

    },

    {

        title: "Sector Analysis",

        href: "/sector",

        icon: Landmark

    },

    {

        title: "About",

        href: "/about",

        icon: Info

    }

];

export default function Sidebar() {

    const pathname = usePathname();

    return (

        <aside
            className="
                sticky
                top-0
                flex
                h-screen
                w-72
                shrink-0
                flex-col
                border-r
                border-border
                bg-sidebar
            "
        >

            {/* ------------------------------------------ */}
            {/* Brand */}
            {/* ------------------------------------------ */}

            <div className="border-b border-border p-6">

                <div className="flex items-center gap-4">

                    <div
                        className="
                            flex
                            h-12
                            w-12
                            items-center
                            justify-center
                            rounded-2xl
                            bg-primary
                            text-primary-foreground
                            shadow-sm
                        "
                    >

                        <Sparkles className="h-6 w-6" />

                    </div>

                    <div>

                        <h1 className="text-xl font-bold tracking-tight">

                            Intel AI

                        </h1>

                        <p className="text-sm text-muted-foreground">

                            Trading Research Platform

                        </p>

                    </div>

                </div>

            </div>

            {/* ------------------------------------------ */}
            {/* Navigation */}
            {/* ------------------------------------------ */}

            <nav className="flex-1 space-y-2 p-4">

                {

                    menuItems.map((item) => {

                        const Icon = item.icon;

                        const active = pathname === item.href;

                        return (

                            <Link

                                key={item.href}

                                href={item.href}

                                className={cn(

                                    "group flex items-center justify-between rounded-xl px-4 py-3 transition-all duration-200",

                                    active

                                        ? "bg-primary text-primary-foreground shadow-sm"

                                        : "text-muted-foreground hover:bg-accent hover:text-foreground"

                                )}

                            >

                                <div className="flex items-center gap-3">

                                    <Icon
                                        className={cn(

                                            "h-5 w-5 transition-transform duration-200",

                                            !active &&

                                                "group-hover:scale-110"

                                        )}
                                    />

                                    <span className="font-medium">

                                        {item.title}

                                    </span>

                                </div>

                                {

                                    active && (

                                        <ChevronRight className="h-4 w-4" />

                                    )

                                }

                            </Link>

                        );

                    })

                }

            </nav>

            {/* ------------------------------------------ */}
            {/* Footer */}
            {/* ------------------------------------------ */}

            <div className="border-t border-border p-5">

                <div
                    className="
                        rounded-2xl
                        border
                        border-border
                        bg-card
                        p-4
                        shadow-sm
                    "
                >

                    <div className="flex items-center gap-2">

                        <span className="relative flex h-3 w-3">

                            <span
                                className="
                                    absolute
                                    inline-flex
                                    h-full
                                    w-full
                                    animate-ping
                                    rounded-full
                                    bg-green-500
                                    opacity-50
                                "
                            />

                            <span
                                className="
                                    relative
                                    inline-flex
                                    h-3
                                    w-3
                                    rounded-full
                                    bg-green-500
                                "
                            />

                        </span>

                        <span className="font-semibold">

                            System Online

                        </span>

                    </div>

                    <p className="mt-3 text-sm leading-6 text-muted-foreground">

                        LangGraph • Hybrid GraphRAG • Groq LLM

                    </p>

                </div>

            </div>

        </aside>

    );

}