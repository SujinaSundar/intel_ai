"use client";

/**
 * Compare Page.
 *
 * Main page for comparing
 * two NIFTY 50 companies.
 */

import { useState } from "react";

import { Scale } from "lucide-react";

import PageHeader from "@/components/common/PageHeader";
import InsightBanner from "@/components/dashboard/InsightBanner";

import CompareForm from "./CompareForm";
import CompareResult from "./CompareResult";

export default function ComparePage() {

    const [

        companyOne,

        setCompanyOne

    ] = useState("");

    const [

        companyTwo,

        setCompanyTwo

    ] = useState("");

    const [

        result,

        setResult

    ] = useState("");

    const [

        loading,

        setLoading

    ] = useState(false);

    return (

        <div className="mx-auto max-w-7xl space-y-8">

            <PageHeader

                title="Compare Companies"

                description="Compare financial performance, AI research, business insights and latest news for any two NIFTY 50 companies."

                icon={

                    <Scale className="h-8 w-8 text-primary" />

                }

            />

            <InsightBanner

                title="AI-Powered Company Comparison"

                description="The comparison combines Finance, Research and News agents to generate a comprehensive comparison."

            />

            <CompareForm

                companyOne={companyOne}

                companyTwo={companyTwo}

                setCompanyOne={setCompanyOne}

                setCompanyTwo={setCompanyTwo}

                setResult={setResult}

                loading={loading}

                setLoading={setLoading}

            />

            <CompareResult

                companyOne={companyOne}

                companyTwo={companyTwo}

                result={result}

                loading={loading}

            />

        </div>

    );

}