"""
Financial utilities for the OACP multi-agent workflow.

Currently includes a Monte Carlo IRR simulator which applies
stochastic shocks to a base cashflow schedule and returns the
distribution of simulated IRRs as well as key percentiles. This is
intended for demonstration and can be replaced with more robust
modelling as needed.
"""

import numpy as np
from typing import Dict, List


class MonteCarloIRR:
    """Monte Carlo simulation for internal rate of return (IRR).

    Args:
        cashflows: Sequence of cashflows (negative for outflows, positive for inflows).
        sims: Number of Monte Carlo simulations to run.
        vol: Standard deviation of the multiplicative shock applied to each cashflow.
        seed: Random seed for reproducibility.

    Methods:
        run() -> dict: Executes the simulation and returns a dictionary with
            p50, p75, p25 and the raw array of IRRs.
    """

    def __init__(self, cashflows: List[float], sims: int = 5000, vol: float = 0.15, seed: int = 42):
        self.cashflows = np.array(cashflows, dtype=float)
        self.sims = sims
        self.vol = vol
        self.rng = np.random.default_rng(seed)

    def run(self) -> Dict[str, object]:
        years = np.arange(len(self.cashflows))
        flows = self.cashflows.copy()
        irrs: List[float] = []
        for _ in range(self.sims):
            # Apply normally distributed shocks to each cashflow
            shocks = self.rng.normal(0, self.vol, size=len(flows))
            shocked = flows * (1 + shocks)
            try:
                irr = np.irr(shocked)  # use numpy_financial if available
            except Exception:
                irr = np.nan
            irrs.append(irr)
        arr = np.array(irrs)
        # Compute percentiles if there are any finite values
        p50 = float(np.nanpercentile(arr, 50) if np.isfinite(arr).any() else float('nan'))
        p75 = float(np.nanpercentile(arr, 75) if np.isfinite(arr).any() else float('nan'))
        p25 = float(np.nanpercentile(arr, 25) if np.isfinite(arr).any() else float('nan'))
        return {
            "p50": p50,
            "p75": p75,
            "p25": p25,
            "raw": arr.tolist(),
        }