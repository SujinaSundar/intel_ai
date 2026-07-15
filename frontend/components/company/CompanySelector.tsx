"use client";

/**
 * Company Selector.
 *
 * Dropdown component for
 * selecting a company.
 */

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

        <div className="space-y-2">

            <label
                className="text-sm font-medium text-slate-300"
            >
                Company
            </label>

            <Select

                value={value}

                onValueChange={onChange}

            >

                <SelectTrigger
                    className="w-[320px]"
                >

                    <SelectValue
                        placeholder="Select a company"
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

        </div>

    );

}