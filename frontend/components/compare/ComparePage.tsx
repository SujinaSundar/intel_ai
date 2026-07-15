"use client";

/**
 * Compare Page.
 *
 * Main page for comparing
 * two NIFTY 50 companies.
 */

import { useState } from "react";

import CompareForm from "./CompareForm";
import CompareResult from "./CompareResult";


export default function ComparePage() {

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

            <CompareForm

                setResult={setResult}

                loading={loading}

                setLoading={setLoading}

            />

            <CompareResult

                result={result}

                loading={loading}

            />

        </div>

    );

}