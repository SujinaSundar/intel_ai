/**
 * Company Service.
 *
 * Fetches company data
 * through the Agent Service.
 */

import { askQuestion } from "./agent.service";

export async function getCompanyData(
    company: string
) {

    const [

        finance,

        research,

        news

    ] = await Promise.all([

        askQuestion(

            `Provide the latest financial summary of ${company}.`,[]

        ),

        askQuestion(

            `Give me a research summary of ${company}.`,[]

        ),

        askQuestion(

            `Summarize the latest news about ${company}.`,[]

        )

    ]);

    return {

        finance,

        research,

        news

    };

}