from crewai import Agent

from backend.config import get_llm
from backend.tools.inventory_tool import check_inventory_stock
from backend.tools.rag_tool import search_company_docs
from backend.tools.sales_tool import generate_quotation


def build_agents():
    llm = get_llm()

    inventory_agent = Agent(
        role="Inventory Specialist",
        goal="Provide accurate, up-to-date stock and pricing information from the business database.",
        backstory=(
            "You are the warehouse and inventory expert. You always check the live "
            "inventory database before answering and never guess stock numbers."
        ),
        tools=[check_inventory_stock],
        llm=llm,
        allow_delegation=False,
        verbose=True,
    )

    sales_agent = Agent(
        role="Sales Specialist",
        goal=(
            "Call the Generate Sales Quotation tool and return its output EXACTLY "
            "as-is — every line, every number. Never rephrase or add extra text."
        ),
        backstory=(
            "You are a sales executive. Your only job is to call your quotation tool "
            "with the correct product name, quantity, and discount, then return the "
            "tool output verbatim. You never invent payment terms or extra clauses."
        ),
        tools=[generate_quotation],
        llm=llm,
        allow_delegation=False,
        verbose=True,
    )

    support_agent = Agent(
        role="Customer Support Specialist",
        goal="Answer customer questions about company policies using official documentation only.",
        backstory=(
            "You are a customer support representative who always grounds answers in "
            "the company's official policy documents rather than assumptions."
        ),
        tools=[search_company_docs],
        llm=llm,
        allow_delegation=False,
        verbose=True,
    )

    return [inventory_agent, sales_agent, support_agent]
