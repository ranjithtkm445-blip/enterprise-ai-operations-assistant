from crewai.tools import tool

from backend.rag.vector_store import search


@tool("Search Company Policies")
def search_company_docs(query: str) -> str:
    """Search internal company policy documents (warranty, refund, shipping) for
    information relevant to the query. Use this for any customer support or policy question."""
    docs = search(query)
    if not docs:
        return "No relevant company policy information found for this query."
    return "\n\n---\n\n".join(docs)
