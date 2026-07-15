"use client";

/**
 * Sector Page.
 *
 * Main container for
 * Sector Analysis.
 */

import { useState } from "react";

import SectorSelector from "./SectorSelector";
import SectorResult from "./SectorResult";


export default function SectorPage() {

    const [

        result,

        setResult

    ] = useState("");

    const [

        loading,

        setLoading

    ] = useState(false);

    return (

        <div className="space-y-8">

            <SectorSelector

                loading={loading}

                setLoading={setLoading}

                setResult={setResult}

            />

            <SectorResult

                loading={loading}

                result={result}

            />

        </div>

    );

}