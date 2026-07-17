"use client";

/**
 * Company Selector.
 *
 * Modern company selector
 * used in the Company
 * Explorer page.
 */

import { Building2, CheckCircle2 } from "lucide-react";

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
    CompanyOption
} from "@/types/company";

interface CompanySelectorProps {

    companies: CompanyOption[];

    value: string;

    onChange: (
        value: string
    ) => void;

}

export default function CompanySelector({

    companies,

    value,

    onChange

}: CompanySelectorProps) {

    return (

        <Card className="mb-8 border-border bg-card shadow-sm">

            <CardContent className="p-6">

                {/* ------------------------------------------ */}
                {/* Header */}
                {/* ------------------------------------------ */}

                <div className="mb-6 flex items-start gap-4">

                    <div className="rounded-xl bg-primary/10 p-3">

                        <Building2 className="h-6 w-6 text-primary" />

                    </div>

                    <div>

                        <h2 className="text-xl font-semibold">

                            Select Company

                        </h2>

                        <p className="mt-1 text-sm leading-6 text-muted-foreground">

                            Explore financial performance, AI research,
                            company news and business insights for any
                            NIFTY 50 company.

                        </p>

                    </div>

                </div>

                {/* ------------------------------------------ */}
                {/* Company Selector */}
                {/* ------------------------------------------ */}

                <div>

                    <label className="mb-2 block text-sm font-medium text-muted-foreground">

                        Company

                    </label>

                    <Select

                        value={value}

                        onValueChange={onChange}

                    >

                        <SelectTrigger className="h-12 w-full rounded-xl transition-all focus:ring-2 focus:ring-primary">

                            <SelectValue

                                placeholder="Select a NIFTY 50 company"

                            />

                        </SelectTrigger>

                        <SelectContent>

                            {

                                companies.map(

                                    (company) => (

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

                    {

                        value && (

                            <div className="mt-4 flex items-center gap-2 rounded-lg border border-green-500/20 bg-green-500/10 px-4 py-3">

                                <CheckCircle2 className="h-5 w-5 text-green-500" />

                                <p className="text-sm">

                                    Showing AI insights for{" "}

                                    <span className="font-semibold text-foreground">

                                        {companies.find(

                                            company => company.value === value

                                        )?.label ?? value}

                                    </span>

                                </p>

                            </div>

                        )

                    }

                </div>

            </CardContent>

        </Card>

    );

}