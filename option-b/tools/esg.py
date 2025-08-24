"""
Naive ESG scoring utilities.

This module contains a simple dataclass for representing an ESG score
and a rudimentary scoring function that assigns heuristic scores based
on a small number of company attributes. In a real deployment, this
logic should be replaced with a thorough policy aligned with your
fund’s ESG/SDG framework.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ESGScore:
    e: float
    s: float
    g: float
    sdg_alignment: List[int]


def score_esg(company_profile: Dict[str, bool]) -> ESGScore:
    """Compute a naive ESG score based on a company profile.

    Args:
        company_profile: Dictionary indicating presence of ESG features such as
            has_emissions_plan, gender_inclusion_target and board_independence.

    Returns:
        An ESGScore object containing E, S, G metrics and a list of
        aligned SDG numbers.
    """
    e = 0.6 if company_profile.get("has_emissions_plan") else 0.4
    s = 0.7 if company_profile.get("gender_inclusion_target") else 0.5
    g = 0.8 if company_profile.get("board_independence") else 0.5
    sdgs: List[int] = [4, 8] + ([5] if company_profile.get("gender_inclusion_target") else [])
    return ESGScore(e=e, s=s, g=g, sdg_alignment=sdgs)