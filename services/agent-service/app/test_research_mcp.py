from pprint import pprint

from app.mcp.research_mcp import ResearchMCP

mcp = ResearchMCP()

print("\nAnswer")
pprint(
    mcp.answer_question(
        "What products does Infosys offer?"
    )
)

print("\nSearch")
pprint(
    mcp.search_reports(
        "What products does Infosys offer?"
    )
)

print("\nMetadata")
pprint(
    mcp.get_report_metadata(
        "Infosys"
    )
)

print("\nReports")
pprint(
    mcp.list_available_reports(
        "Infosys"
    )
)

print("\nSummary")
pprint(
    mcp.summarize_reports(
        "Infosys"
    )
)

print("\nLatest")
pprint(
    mcp.get_latest_report(
        "Infosys"
    )
)

print("\nCount")
pprint(
    mcp.get_report_count(
        "Infosys"
    )
)