"use client";

/**
 * Compare Form.
 *
 * Allows the user to select
 * two companies and compare
 * them using the AI Agent.
 */

import { useState } from "react";

import {
    Button
} from "@/components/ui/button";

import CompanySelector from "@/components/company/CompanySelector";

import {
    COMPANIES
} from "@/constants/companies";

import {
    askQuestion
} from "@/services/agent.service";


interface CompareFormProps {

    loading: boolean;

    setLoading: (

        loading: boolean

    ) => void;

    setResult: (

        result: string

    ) => void;

}


export default function CompareForm({

    loading,

    setLoading,

    setResult

}: CompareFormProps) {

    const [

        companyOne,

        setCompanyOne

    ] = useState("");

    const [

        companyTwo,

        setCompanyTwo

    ] = useState("");

    // ---------------------------------------------------------
    // Compare Companies
    // ---------------------------------------------------------

    const compareCompanies = async () => {

        if (

            !companyOne ||

            !companyTwo

        ) {

            return;

        }

        setLoading(true);

        try {

            const response = await askQuestion(

                `Compare ${companyOne} and ${companyTwo}.`

            );

            setResult(

                response

            );

        }

        catch (error) {

            console.error(

                error

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

        <div className="space-y-6">

            <div>

                <h1 className="text-4xl font-bold">

                    📊 Compare Companies

                </h1>

                <p className="mt-2 text-slate-400">

                    Compare two NIFTY 50 companies using
                    our AI Research Platform.

                </p>

            </div>

            <div className="grid gap-6 md:grid-cols-2">

                <CompanySelector

                    companies={COMPANIES}

                    value={companyOne}

                    onChange={setCompanyOne}

                />

                <CompanySelector

                    companies={COMPANIES}

                    value={companyTwo}

                    onChange={setCompanyTwo}

                />

            </div>

            <Button

                onClick={compareCompanies}

                disabled={

                    loading ||

                    !companyOne ||

                    !companyTwo

                }

            >

                {

                    loading

                        ? "Comparing..."

                        : "Compare"

                }

            </Button>

        </div>

    );

}