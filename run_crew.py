"""
Entry point for running the multi‑agent pipeline using CrewAI.

This script orchestrates three agents (Imbokodo, Baobab and Athena) to
research a given investment theme, prepare a pre‑IC screen and draft
an investment committee memo. It also demonstrates how to use
auxiliary utilities such as a simple web search, Monte Carlo IRR
simulation and ESG scoring. Outputs are written to the `outputs/`
directory.

To use this script, copy `.env.example` to `.env` and populate it
with your OpenAI API key and (optionally) a SERPAPI key for enhanced
search. Then install dependencies from `requirements.txt` and run

    python run_crew.py

You can adjust the `deal_name`, `sector_query`, `base_case_cashflows`
and `company_profile` variables to suit your analysis.
"""

import os
from dotenv import load_dotenv
from crewai import Task, Crew, Process
from agents import Athena, Baobab, Imbokodo
from tools.search import web_search
from tools.finance import MonteCarloIRR
from tools.esg import score_esg
from tools.writer import render_ic_memo
from rich import print

# Load environment variables (e.g., API keys) from .env
load_dotenv()

# === INPUTS (modify these for each deal) ===
deal_name = "AI Vocational Edtech Expansion"
sector_query = "Sub‑Saharan Africa edtech market size CAGR"
base_case_cashflows = [
    -120_000_000,
    10_000_000,
    25_000_000,
    45_000_000,
    60_000_000,
    80_000_000,
]
company_profile = {
    "has_emissions_plan": True,
    "gender_inclusion_target": True,
    "board_independence": True,
}

# === Agent tasks ===
analyst_task = Task(
    description=(
        f"Research: {sector_query}. Summarize key data points, competitors, and regulatory notes. "
        "Create a short financial summary."
    ),
    agent=Imbokodo,
    expected_output="Markdown brief with bullets and references.",
)

associate_task = Task(
    description=(
        "Turn the analyst brief into a pre-IC screen: investment case, terms, DD list, monitoring metrics."
    ),
    agent=Baobab,
    expected_output="Pre-IC screen with diligence checklist and KPIs.",
)

principal_task = Task(
    description=(
        "Run risk-adjusted analysis, recommend stake and exit scenarios, and draft the IC memo."
    ),
    agent=Athena,
    expected_output="IC-ready memo with scenarios and recommendation.",
)

# Create the crew with a sequential process
crew = Crew(
    agents=[Imbokodo, Baobab, Athena],
    tasks=[analyst_task, associate_task, principal_task],
    process=Process.sequential,
)

# === Non-LLM utilities (demo) ===
search_hits = web_search(sector_query, max_results=6)
irr_result = MonteCarloIRR(base_case_cashflows).run()
esg_score = score_esg(company_profile)

# Compose context for memo rendering
context = {
    "deal_name": deal_name,
    "exec_summary": (
        f"Seeking R120m expansion equity. MC IRR p50: {irr_result['p50']:.2%}. "
        f"ESG (E/S/G): {esg_score.e:.2f}/{esg_score.s:.2f}/{esg_score.g:.2f}."
    ),
    "strategic_fit": "Education sector, SDG 4 & 8 alignment, pan‑African scalability.",
    "market": f"Top search refs: {[h['title'] for h in search_hits]}",
    "financials": "Base case cashflows and margin expansion; sensitivity to CAC & churn.",
    "esg": f"SDG alignment: {esg_score.sdg_alignment}. Governance: independence confirmed.",
    "risks": "Regulatory approvals, platform scalability, CAC volatility.",
    "exits": "Trade sale to global edtech or regional IPO within 5–7 years.",
    "recommendation": "Proceed to full DD. Target 25–30% with board seat and covenants.",
}

# Render the memo using the provided context
memo = render_ic_memo(context)

# Ensure outputs directory exists and write the memo
if not os.path.exists('outputs'):
    os.makedirs('outputs', exist_ok=True)

with open(os.path.join('outputs', 'ic_memo.md'), 'w', encoding='utf-8') as f:
    f.write(memo)

# Kick off the crew (this will run the LLM agents)
result = crew.kickoff()

print("\n[bold green]IC memo written to outputs/ic_memo.md[/bold green]")
print("\n[bold cyan]Crew result (summary):[/bold cyan]", result)