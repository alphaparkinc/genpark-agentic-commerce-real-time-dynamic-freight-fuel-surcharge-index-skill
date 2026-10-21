# -*- coding: utf-8 -*-
"""Dynamic Freight Fuel Surcharge Indexer for GenPark Agentic Commerce."""
import json
from typing import Dict, Any

class FreightFuelSurchargeIndexer:
    @staticmethod
    def calculate_baseline_fsc_percentage(current_doe_diesel_price_per_gal: float, baseline_diesel_peg: float = 1.25, fsc_step_cents: float = 0.05, fsc_step_pct: float = 0.5) -> Dict[str, Any]:
        excess_cost = max(0.0, current_doe_diesel_price_per_gal - baseline_diesel_peg)
        steps = excess_cost / fsc_step_cents
        fsc_pct = round(steps * fsc_step_pct, 2)
        return {"current_diesel_price": current_doe_diesel_price_per_gal, "baseline_peg": baseline_diesel_peg, "contract_fsc_rate_pct": fsc_pct}

    @staticmethod
    def audit_carrier_invoice_fsc_overcharge(billed_fsc_usd: float, linehaul_charge_usd: float, expected_fsc_pct: float) -> Dict[str, Any]:
        legit_fsc = round(linehaul_charge_usd * (expected_fsc_pct / 100.0), 2)
        overcharge = round(max(0.0, billed_fsc_usd - legit_fsc), 2)
        return {"billed_fsc_usd": billed_fsc_usd, "contract_legitimate_fsc_usd": legit_fsc, "overcharge_usd": overcharge, "verdict": "OVERCHARGE_DETECTED" if overcharge > 5.0 else "INVOICE_VALID"}
