"use client";

/**
 * Compare Form.
 *
 * Select two companies
 * and compare them using
 * the AI Trading Research
 * Platform.
 */

import {
    ArrowLeftRight,
    Building2,
    Sparkles
} from "lucide-react";

import {
    Button
} from "@/components/ui/button";

import {
    Card,
    CardContent
} from "@/components/ui/card";

import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue
} from "@/components/ui/select";

import {
    COMPANIES
} from "@/constants/companies";

import {
    askQuestion
} from "@/services/agent.service";

interface CompareFormProps {

    companyOne: string;

    companyTwo: string;

    setCompanyOne: (
        value: string
    ) => void;

    setCompanyTwo: (
        value: string
    ) => void;

    loading: boolean;

    setLoading: (
        loading: boolean
    ) => void;

    setResult: (
        result: string
    ) => void;

}

export default function CompareForm({

    companyOne,

    companyTwo,

    setCompanyOne,

    setCompanyTwo,

    loading,

    setLoading,

    setResult

}: CompareFormProps) {

    // ---------------------------------------------------------
    // Compare Companies
    // ---------------------------------------------------------

    async function compareCompanies() {

        if (

            !companyOne ||

            !companyTwo

        ) {

            return;

        }

        setLoading(true);

        try {

            const response = await askQuestion(
    `Compare ${companyOne} and ${companyTwo}.`,
    []
);
            setResult(response);

        }

        catch (error) {

            console.error(error);

        }

        finally {

            setLoading(false);

        }

    }

    // ---------------------------------------------------------
    // UI
    // ---------------------------------------------------------

    return (

        <Card className="border-border shadow-sm">

            <CardContent className="space-y-8 p-8">

                <div className="text-center">

                    <h2 className="text-2xl font-bold">

                        Select Companies

                    </h2>

                    <p className="mt-2 text-muted-foreground">

                        Compare financial performance, business research
                        and latest news for any two NIFTY 50 companies.

                    </p>

                </div>

                <div className="grid items-center gap-8 lg:grid-cols-[1fr_auto_1fr]">

                    {/* Company A */}

                    <div>

                        <label className="mb-3 flex items-center gap-2 text-sm font-medium">

                            <Building2 className="h-4 w-4 text-primary" />

                            Company A

                        </label>

                        <Select

                            value={companyOne}

                           onValueChange={(value) => {
    if (value !== null) {
        setCompanyOne(value);
    }
}}

                        >

                            <SelectTrigger className="h-12 rounded-xl">

                                <SelectValue

                                    placeholder="Select first company"

                                />

                            </SelectTrigger>

                            <SelectContent>

                                {

                                    COMPANIES.map(

                                        company => (

                                            <SelectItem

                                                key={company.value}

                                                value={company.value}

                                            >

                                                {company.label}

                                            </SelectItem>

                                        )

                                    )

                                }

                            </SelectContent>

                        </Select>

                    </div>

                    {/* VS */}

                    <div className="flex justify-center">

                        <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-lg">

                            <ArrowLeftRight className="h-7 w-7" />

                        </div>

                    </div>

                    {/* Company B */}

                    <div>

                        <label className="mb-3 flex items-center gap-2 text-sm font-medium">

                            <Building2 className="h-4 w-4 text-primary" />

                            Company B

                        </label>

                        <Select

                            value={companyTwo}

                            onValueChange={(value) => {
    if (value !== null) {
        setCompanyTwo(value);
    }
}}

                        >

                            <SelectTrigger className="h-12 rounded-xl">

                                <SelectValue

                                    placeholder="Select second company"

                                />

                            </SelectTrigger>

                            <SelectContent>

                                {

                                    COMPANIES.map(

                                        company => (

                                            <SelectItem

                                                key={company.value}

                                                value={company.value}

                                            >

                                                {company.label}

                                            </SelectItem>

                                        )

                                    )

                                }

                            </SelectContent>

                        </Select>

                    </div>

                </div>

                <div className="flex justify-center">

                    <Button

                        size="lg"

                        className="rounded-xl px-10"

                        disabled={

                            loading ||

                            !companyOne ||

                            !companyTwo

                        }

                        onClick={compareCompanies}

                    >

                        <Sparkles className="mr-2 h-5 w-5" />

                        {

                            loading

                                ? "Generating AI Comparison..."

                                : "Compare Companies"

                        }

                    </Button>

                </div>

            </CardContent>

        </Card>

    );

}
