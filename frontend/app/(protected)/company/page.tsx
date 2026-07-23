"use client";

/**
 * Company Explorer Page.
 */

import CompanyExplorer from "@/components/company/CompanyExplorer";


export default function CompanyPage() {

    return (

        <div className="mx-auto max-w-6xl">

            <div className="mb-8">

                <h1 className="text-4xl font-bold">

                    🏢 Company Explorer

                </h1>

                <p className="mt-2 text-slate-400">

                    Explore financial information,
                    research insights and latest
                    news for NIFTY 50 companies.

                </p>

            </div>

            <CompanyExplorer />

        </div>

    );

}