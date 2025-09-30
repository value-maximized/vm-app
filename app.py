from flask import Flask, render_template, request, url_for
from data import get_kpis_for_scenario, get_strategy_model, SCENARIOS

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template("dashboard.html", **_ctx("baseline"))

    @app.route("/dashboard")
    def dashboard():
        scenario = request.args.get("scenario", "baseline").lower()
        if scenario not in SCENARIOS:
            scenario = "baseline"
        return render_template("dashboard.html", **_ctx(scenario))

    @app.route("/strategy")
    def strategy():
        model = get_strategy_model()
        return render_template("strategy.html", model=model, scenarios=list(SCENARIOS.keys()))

    def _ctx(scenario: str):
        kpis = get_kpis_for_scenario(scenario)
        return {
            "scenario": scenario,
            "scenarios": list(SCENARIOS.keys()),
            "kpis": kpis
        }

    return app

app = create_app()
