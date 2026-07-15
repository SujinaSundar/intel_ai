"use client";

/**
 * Company Explorer.
 *
 * Main container for
 * Company Explorer.
 */

import { useEffect, useState } from "react";

import CompanySelector from "./CompanySelector";
import CompanyTabs from "./CompanyTabs";

import {
    COMPANIES
} from "@/constants/companies";

import {
    getCompanyData
} from "@/services/company.service";


export default function CompanyExplorer() {

    const [company, setCompany] = useState("");

    const [loading, setLoading] = useState(false);

    const [companyData, setCompanyData] = useState({

        finance: "",

        research: "",

        news: ""

    });

    // ---------------------------------------------------------
    // Load Company Information
    // ---------------------------------------------------------

    useEffect(() => {

        if (!company) {

            return;

        }

        loadCompany();

    }, [company]);

    // ---------------------------------------------------------
    // Fetch Company Data
    // ---------------------------------------------------------

    const loadCompany = async () => {

        setLoading(true);

        try {

            const response = await getCompanyData(

                company

            );
            console.log("Company Data:", response);

            setCompanyData(

                response

            );

        }

        catch (error) {

            console.error(

                "Unable to load company.",

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

        <div className="space-y-8">

            <CompanySelector

                companies={COMPANIES}

                value={company}

                onChange={setCompany}

            />

            {

                company && (

                    <CompanyTabs

                        company={company}

                        loading={loading}

                        finance={companyData.finance}

                        research={companyData.research}

                        news={companyData.news}

                    />

                )

            }

        </div>

    );

}