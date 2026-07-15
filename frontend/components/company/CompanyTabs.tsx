"use client";

/**
 * Company Tabs.
 *
 * Displays company
 * information using
 * tab navigation.
 */

import {
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger
} from "@/components/ui/tabs";

import OverviewTab from "./OverviewTab";
import FinanceTab from "./FinanceTab";
import ResearchTab from "./ResearchTab";
import NewsTab from "./NewsTab";


interface CompanyTabsProps {

    company: string;

    loading: boolean;

    finance: string;

    research: string;

    news: string;

}


export default function CompanyTabs({

    company,

    loading,

    finance,

    research,

    news

}: CompanyTabsProps) {

    return (

        <Tabs

            defaultValue="overview"

            className="w-full"

        >

            {/* ------------------------------------------------ */}
            {/* Tab Header */}
            {/* ------------------------------------------------ */}

            <TabsList
                className="inline-flex"
            >

                <TabsTrigger value="overview">

                    Overview

                </TabsTrigger>

                <TabsTrigger value="finance">

                    Finance

                </TabsTrigger>

                <TabsTrigger value="research">

                    Research

                </TabsTrigger>

                <TabsTrigger value="news">

                    News

                </TabsTrigger>

            </TabsList>

            {/* ------------------------------------------------ */}
            {/* Overview */}
            {/* ------------------------------------------------ */}

            <TabsContent value="overview">

                <OverviewTab

                    company={company}

                    loading={loading}

                    finance={finance}

                    research={research}

                    news={news}

                />

            </TabsContent>

            {/* ------------------------------------------------ */}
            {/* Finance */}
            {/* ------------------------------------------------ */}

            <TabsContent value="finance">

                <FinanceTab

                    company={company}

                    loading={loading}

                    finance={finance}

                />

            </TabsContent>

            {/* ------------------------------------------------ */}
            {/* Research */}
            {/* ------------------------------------------------ */}

            <TabsContent value="research">

                <ResearchTab

                    company={company}

                    loading={loading}

                    research={research}

                />

            </TabsContent>

            {/* ------------------------------------------------ */}
            {/* News */}
            {/* ------------------------------------------------ */}

            <TabsContent value="news">

                <NewsTab

                    company={company}

                    loading={loading}

                    news={news}

                />

            </TabsContent>

        </Tabs>

    );

}