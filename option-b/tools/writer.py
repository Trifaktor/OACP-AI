"""
Utility functions for generating human‑readable artefacts.

Currently includes `render_ic_memo`, which takes a context dictionary
and returns a Markdown string formatted as an investment committee
memorandum. This can easily be extended to render other document
formats (e.g., PDF, Word) using python‑docx or reportlab.
"""

from datetime import date
from typing import Dict


def render_ic_memo(context: Dict[str, object]) -> str:
    """Render an IC memo as a Markdown string.

    Args:
        context: Dictionary containing keys such as deal_name,
            exec_summary, strategic_fit, market, financials, esg,
            risks, exits and recommendation.

    Returns:
        A formatted Markdown string representing the memo.
    """
    return f"""
# Investment Committee Memo
**Deal:** {context['deal_name']}
**Date:** {date.today().isoformat()}
**Prepared by:** Imbokodo (Analyst), Baobab (Associate), Athena (Principal)

## 1. Executive Summary
{context['exec_summary']}

## 2. Strategic Fit
{context['strategic_fit']}

## 3. Market Overview
{context['market']}

## 4. Business & Financials
{context['financials']}

## 5. ESG & Impact
{context['esg']}

## 6. Risks & Mitigants
{context['risks']}

## 7. Exit Scenarios
{context['exits']}

## 8. Recommendation
{context['recommendation']}
"""