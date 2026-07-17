"use client";

/**
 * News Tab.
 *
 * Displays the latest
 * company news.
 */

import Markdown from "@/components/common/Markdown";
import SectionCard from "@/components/common/SectionCard";
import EmptyState from "@/components/common/EmptyState";
import LoadingState from "@/components/common/LoadingState";

interface NewsTabProps {

    company: string;

    loading: boolean;

    news: string;

}

export default function NewsTab({

    company,

    loading,

    news

}: NewsTabProps) {

    if (loading) {

        return <LoadingState />;

    }

    if (!news) {

        return (

            <EmptyState

                title="Latest News"

                description={`No recent news available for ${company}.`}

            />

        );

    }

    return (

        <SectionCard

            title="Latest News"

            description={`Recent developments related to ${company}`}

        >

            <Markdown content={news} />

        </SectionCard>

    );

}