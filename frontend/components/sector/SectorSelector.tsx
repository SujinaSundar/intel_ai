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

import { Button } from "@/components/ui/button";

import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue
} from "@/components/ui/select";

import { askQuestion } from "@/services/agent.service";

import { SECTORS } from "@/constants/sectors";


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

    const [

        sector,

        setSector

    ] = useState("");

    // ---------------------------------------------------------
    // Analyze Sector
    // ---------------------------------------------------------

    const analyzeSector = async () => {

        if (!sector) {

            return;

        }

        setLoading(true);

        try {

            const response = await askQuestion(

                `Analyze the ${sector} sector.`

            );

            setResult(

                response

            );

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

    };

    // ---------------------------------------------------------
    // UI
    // ---------------------------------------------------------

    return (

        <div className="space-y-6">

            <div>

                <h1 className="text-4xl font-bold">

                    🏦 Sector Analysis

                </h1>

                <p className="mt-2 text-slate-400">

                    Explore AI-generated insights for NIFTY 50 sectors.

                </p>

            </div>

            <div className="max-w-md">

                <Select

                    value={sector}

                    onValueChange={setSector}

                >

                    <SelectTrigger>

                        <SelectValue

                            placeholder="Select a sector"

                        />

                    </SelectTrigger>

                    <SelectContent>

                        {

                            SECTORS.map(

                                (

                                    item

                                ) => (

                                    <SelectItem

                                        key={item}

                                        value={item}

                                    >

                                        {item}

                                    </SelectItem>

                                )

                            )

                        }

                    </SelectContent>

                </Select>

            </div>

            <Button

                onClick={analyzeSector}

                disabled={

                    loading ||

                    !sector

                }

            >

                {

                    loading

                        ? "Analyzing..."

                        : "Analyze Sector"

                }

            </Button>

        </div>

    );

}