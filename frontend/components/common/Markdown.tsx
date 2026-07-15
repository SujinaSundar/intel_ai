"use client";

/**
 * Markdown Renderer.
 *
 * Shared markdown component
 * used throughout the
 * application.
 */

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface MarkdownProps {

    content: string;

}

export default function Markdown({

    content

}: MarkdownProps) {

    return (

        <div className="space-y-4 text-base leading-8 text-slate-200">

            <ReactMarkdown

                remarkPlugins={[remarkGfm]}

                components={{

                    h1: ({ children }) => (

                        <h1 className="mb-6 mt-2 text-3xl font-bold tracking-tight text-white">

                            {children}

                        </h1>

                    ),

                    h2: ({ children }) => (

                        <h2 className="mb-4 mt-8 border-b border-slate-700 pb-2 text-2xl font-semibold text-white">

                            {children}

                        </h2>

                    ),

                    h3: ({ children }) => (

                        <h3 className="mb-3 mt-6 text-xl font-semibold text-white">

                            {children}

                        </h3>

                    ),

                    p: ({ children }) => (

                        <p className="mb-4 leading-8 text-slate-300">

                            {children}

                        </p>

                    ),

                    ul: ({ children }) => (

                        <ul className="mb-5 list-disc space-y-2 pl-6 text-slate-300">

                            {children}

                        </ul>

                    ),

                    ol: ({ children }) => (

                        <ol className="mb-5 list-decimal space-y-2 pl-6 text-slate-300">

                            {children}

                        </ol>

                    ),

                    li: ({ children }) => (

                        <li className="leading-7">

                            {children}

                        </li>

                    ),

                    strong: ({ children }) => (

                        <strong className="font-semibold text-white">

                            {children}

                        </strong>

                    ),

                    blockquote: ({ children }) => (

                        <blockquote className="my-6 border-l-4 border-blue-500 pl-4 italic text-slate-400">

                            {children}

                        </blockquote>

                    ),

                    code: ({ className, children }) => {

                        const isBlock = className?.startsWith("language-");

                        if (isBlock) {

                            return (

                                <code className={className}>

                                    {children}

                                </code>

                            );

                        }

                        return (

                            <code className="rounded bg-slate-800 px-1.5 py-1 text-sm text-cyan-300">

                                {children}

                            </code>

                        );

                    },

                    pre: ({ children }) => (

                        <pre className="my-6 overflow-x-auto rounded-xl bg-slate-950 p-4 text-sm text-slate-200">

                            {children}

                        </pre>

                    ),

                    hr: () => (

                        <hr className="my-8 border-slate-700" />

                    ),

                    table: ({ children }) => (

                        <div className="my-6 overflow-x-auto">

                            <table className="min-w-full border border-slate-700">

                                {children}

                            </table>

                        </div>

                    ),

                    thead: ({ children }) => (

                        <thead className="bg-slate-800">

                            {children}

                        </thead>

                    ),

                    tbody: ({ children }) => (

                        <tbody>

                            {children}

                        </tbody>

                    ),

                    tr: ({ children }) => (

                        <tr className="border-b border-slate-700">

                            {children}

                        </tr>

                    ),

                    th: ({ children }) => (

                        <th className="px-4 py-3 text-left font-semibold text-white">

                            {children}

                        </th>

                    ),

                    td: ({ children }) => (

                        <td className="px-4 py-3 text-slate-300">

                            {children}

                        </td>

                    ),

                    a: ({ href, children }) => (

                        <a

                            href={href}

                            target="_blank"

                            rel="noopener noreferrer"

                            className="text-blue-400 underline hover:text-blue-300"

                        >

                            {children}

                        </a>

                    )

                }}

            >

                {content}

            </ReactMarkdown>

        </div>

    );

}