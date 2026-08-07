"use client";

/**
 * Sector Selector.
 *
 * Allows the user to select
 * a NIFTY 50 sector and
 * generate an AI-powered
 * sector analysis.
 */

import { useState } from "react";

import {

    Landmark,

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

    askQuestion

} from "@/services/agent.service";

import {

    SECTORS

} from "@/constants/sectors";

interface SectorSelectorProps {

    loading: boolean;

    setLoading: (

        loading: boolean

    ) => void;

    setResult: (

        result: string

    ) => void;

}

export default function SectorSelector({

    loading,

    setLoading,

    setResult

}: SectorSelectorProps) {

    // ---------------------------------------------------------
    // State
    // ---------------------------------------------------------

    const [

        sector,

        setSector

    ] = useState("");

    // ---------------------------------------------------------
    // Analyze Sector
    // ---------------------------------------------------------

    async function analyzeSector() {

        if (!sector) {

            return;

        }

        setLoading(true);

        try {

            const response = await askQuestion(
    `Analyze the ${sector} sector.`,
    []
);

            setResult(response);

        }

        catch (error) {

            console.error(

                "Unable to analyze sector.",

                error

            );

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

                {/* --------------------------------------------- */}
                {/* Header */}
                {/* --------------------------------------------- */}

                <div className="text-center">

                    <h2 className="text-2xl font-bold">

                        Select Sector

                    </h2>

                    <p className="mt-2 text-muted-foreground">

                        Choose a NIFTY 50 sector to generate AI-powered
                        financial, research and news insights.

                    </p>

                </div>

                {/* --------------------------------------------- */}
                {/* Selector */}
                {/* --------------------------------------------- */}

                <div className="mx-auto max-w-lg">

                    <label className="mb-3 flex items-center gap-2 text-sm font-medium">

                        <Landmark className="h-4 w-4 text-primary" />

                        Sector

                    </label>

                    <Select

                       value={sector}

onValueChange={(value, _details) => {
    setSector(value ?? "");
}}


                    >

                        <SelectTrigger className="h-12 rounded-xl">

                            <SelectValue

                                placeholder="Select a NIFTY 50 sector"

                            />

                        </SelectTrigger>

                        <SelectContent>

                            {

                                SECTORS.map(

                                    (sector) => (

                                        <SelectItem

                                            key={sector}

                                            value={sector}

                                        >

                                            {sector}

                                        </SelectItem>

                                    )

                                )

                            }

                        </SelectContent>

                    </Select>

                </div>

                {/* --------------------------------------------- */}
                {/* Button */}
                {/* --------------------------------------------- */}

                <div className="flex justify-center">

                    <Button

                        size="lg"

                        className="rounded-xl px-10"

                        disabled={

                            loading ||

                            !sector

                        }

                        onClick={analyzeSector}

                    >

                        <Sparkles className="mr-2 h-5 w-5" />

                        {

                            loading

                                ? "Generating AI Analysis..."

                                : "Analyze Sector"

                        }

                    </Button>

                </div>

            </CardContent>

        </Card>

    );

}
