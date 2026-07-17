"use client";

/**
 * Markdown Renderer.
 *
 * Shared markdown component
 * used across the application.
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

        <div className="max-w-none text-base leading-7 text-foreground">

            <ReactMarkdown

                remarkPlugins={[remarkGfm]}

                components={{

                    // -------------------------------------------------
                    // Heading 1
                    // -------------------------------------------------

                    h1: ({ children }) => (

                        <h1 className="mb-4 mt-1 text-3xl font-bold tracking-tight text-foreground">

                            {children}

                        </h1>

                    ),

                    // -------------------------------------------------
                    // Heading 2
                    // -------------------------------------------------

                    h2: ({ children }) => (

                        <h2 className="mb-3 mt-6 border-b border-border pb-2 text-2xl font-semibold text-foreground">

                            {children}

                        </h2>

                    ),

                    // -------------------------------------------------
                    // Heading 3
                    // -------------------------------------------------

                    h3: ({ children }) => (

                        <h3 className="mb-2 mt-5 text-xl font-semibold text-foreground">

                            {children}

                        </h3>

                    ),

                    // -------------------------------------------------
                    // Paragraph
                    // -------------------------------------------------

                    p: ({ children }) => (

                        <p className="mb-3 leading-7 text-muted-foreground">

                            {children}

                        </p>

                    ),

                    // -------------------------------------------------
                    // Unordered List
                    // -------------------------------------------------

                    ul: ({ children }) => (

                        <ul className="mb-4 list-disc space-y-1 pl-6 text-muted-foreground">

                            {children}

                        </ul>

                    ),

                    // -------------------------------------------------
                    // Ordered List
                    // -------------------------------------------------

                    ol: ({ children }) => (

                        <ol className="mb-4 list-decimal space-y-1 pl-6 text-muted-foreground">

                            {children}

                        </ol>

                    ),

                    // -------------------------------------------------
                    // List Item
                    // -------------------------------------------------

                    li: ({ children }) => (

                        <li className="leading-7">

                            {children}

                        </li>

                    ),

                    // -------------------------------------------------
                    // Strong
                    // -------------------------------------------------

                    strong: ({ children }) => (

                        <strong className="font-semibold text-foreground">

                            {children}

                        </strong>

                    ),

                    // -------------------------------------------------
                    // Inline Code
                    // -------------------------------------------------

                    code: ({ children }) => (

                        <code className="rounded-md bg-muted px-1.5 py-0.5 font-mono text-sm text-primary">

                            {children}

                        </code>

                    ),

                    // -------------------------------------------------
                    // Block Quote
                    // -------------------------------------------------

                    blockquote: ({ children }) => (

                        <blockquote className="my-4 border-l-4 border-primary pl-4 italic text-muted-foreground">

                            {children}

                        </blockquote>

                    ),

                    // -------------------------------------------------
                    // Horizontal Rule
                    // -------------------------------------------------

                    hr: () => (

                        <hr className="my-4 border-border" />

                    ),

                    // -------------------------------------------------
                    // Table
                    // -------------------------------------------------

                    table: ({ children }) => (

                        <div className="my-4 overflow-x-auto">

                            <table className="w-full border-collapse">

                                {children}

                            </table>

                        </div>

                    ),

                    thead: ({ children }) => (

                        <thead className="border-b border-border bg-muted/40">

                            {children}

                        </thead>

                    ),

                    tbody: ({ children }) => (

                        <tbody>

                            {children}

                        </tbody>

                    ),

                    tr: ({ children }) => (

                        <tr className="border-b border-border">

                            {children}

                        </tr>

                    ),

                    th: ({ children }) => (

                        <th className="px-4 py-2 text-left font-semibold text-foreground">

                            {children}

                        </th>

                    ),

                    td: ({ children }) => (

                        <td className="px-4 py-2 text-muted-foreground">

                            {children}

                        </td>

                    )

                }}

            >

                {content}

            </ReactMarkdown>

        </div>

    );

}