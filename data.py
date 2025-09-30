from datetime import date

# Scenario multipliers (simple but illustrative)
SCENARIOS = {
    "baseline":    {"rev": 1.00, "margin": 1.00, "csat": 1.00, "capex": 1.00, "headcount": 1.00},
    "aggressive":  {"rev": 1.15, "margin": 0.95, "csat": 0.98, "capex": 1.30, "headcount": 1.12},
    "conservative":{"rev": 0.92, "margin": 1.05, "csat": 1.02, "capex": 0.80, "headcount": 0.96},
}

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# Mock “ERP pulls”
BASE_SERIES = {
    "revenue": [2.1,2.3,2.5,2.4,2.7,2.9,3.0,3.2,3.1,3.3,3.5,3.8],  # $M
    "op_margin_pct": [18,17,19,18,20,21,22,21,20,22,23,24],       # %
    "csat": [78,79,80,79,81,82,83,84,83,85,86,87],                # %
}
# Allocations (sum to 100)
BASE_ALLOC = {
    "capital": {"R&D": 30, "Sales": 20, "Ops": 25, "IT": 15, "G&A": 10},
    "headcount": {"R&D": 35, "Sales": 25, "Ops": 20, "IT": 10, "G&A": 10},
}

INITIATIVES = [
    {"name":"Expand into APAC","owner":"VP Growth","status":"On Track","kpi":"Revenue Growth"},
    {"name":"Self-Service Portal","owner":"VP CX","status":"At Risk","kpi":"CSAT"},
    {"name":"Working Capital Program","owner":"CFO","status":"On Track","kpi":"Cash Conversion Cycle"},
    {"name":"Cloud Cost Optimization","owner":"CIO","status":"Off Track","kpi":"Operating Margin"},
]

OBJECTIVES = [
    {"objective":"Accelerate profitable growth",
     "kpis":[{"name":"Revenue Growth","target":"+18% YoY"},{"name":"Operating Margin","target":">=22%"}]},
    {"objective":"Delight customers",
     "kpis":[{"name":"CSAT","target":">=85%"},{"name":"NPS","target":">=45"}]},
    {"objective":"Efficient capital & people allocation",
     "kpis":[{"name":"ROIC","target":">=12%"},{"name":"Cash Conversion Cycle","target":"<40 days"}]},
]

def _apply_scenario(series, factor):
    return [round(v*factor, 2) for v in series]

def get_kpis_for_scenario(scenario: str):
    m = SCENARIOS[scenario]
    rev = _apply_scenario(BASE_SERIES["revenue"], m["rev"])
    margin = [round(p*m["margin"], 1) for p in BASE_SERIES["op_margin_pct"]]
    csat = [round(p*m["csat"], 0) for p in BASE_SERIES["csat"]]

    capital_alloc = {k: round(v*m["capex"], 1) for k,v in BASE_ALLOC["capital"].items()}
    headcount_alloc = {k: round(v*m["headcount"], 1) for k,v in BASE_ALLOC["headcount"].items()}

    return {
        "as_of": date.today().isoformat(),
        "months": MONTHS,
        "revenue_m": rev,
        "op_margin_pct": margin,
        "csat": csat,
        "capital_alloc": capital_alloc,
        "headcount_alloc": headcount_alloc,
        "initiatives": INITIATIVES
    }

def get_strategy_model():
    return {
        "objectives": OBJECTIVES,
        "initiatives": INITIATIVES
    }
