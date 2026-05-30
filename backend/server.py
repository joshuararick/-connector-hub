from datetime import datetime
import os

from flask import Flask, jsonify

try:
    import anthropic
except ImportError:  # pragma: no cover - depends on local environment
    anthropic = None


app = Flask(__name__)


AGENTS = {
    "pathfinder": {
        "name": "PATHFINDER",
        "mission": "Find cloud and network engineering opportunities",
        "prompt": (
            "You are PATHFINDER, a job search agent for a senior "
            "cloud/network engineer. Find 5 current opportunities matching "
            "AWS, Azure, Cisco, Fortinet, healthcare IT, and HIPAA. Format as "
            "a tactical briefing with specific next actions."
        ),
    },
    "sentinel": {
        "name": "SENTINEL",
        "mission": "Review cash flow and runway planning",
        "prompt": (
            "You are SENTINEL, a financial operations agent. Create a "
            "cash-flow review protocol for a job-search transition. Flag "
            "runway risks, recurring obligations, and this week's highest "
            "leverage actions without assuming private account balances."
        ),
    },
    "lifeline": {
        "name": "LIFELINE",
        "mission": "Track health insurance deadlines",
        "prompt": (
            "You are LIFELINE, a benefits planning agent. Explain COBRA vs ACA "
            "options for someone who recently lost employer coverage. Include "
            "deadlines, documents to gather, cost comparison steps, and what "
            "to do this week."
        ),
    },
    "surgeon": {
        "name": "SURGEON",
        "mission": "Audit subscriptions and recurring spend",
        "prompt": (
            "You are SURGEON, a subscription audit agent. Generate a complete "
            "recurring-charge audit protocol: where to search, how to cancel, "
            "what to negotiate, and how to prevent forgotten renewals."
        ),
    },
    "deduction": {
        "name": "DEDUCTION",
        "mission": "Prepare tax-planning questions",
        "prompt": (
            "You are DEDUCTION, a tax preparation planning agent. List "
            "questions and records to bring to a qualified tax professional "
            "during a job-search year. Avoid giving legal or tax guarantees."
        ),
    },
    "hustler": {
        "name": "HUSTLER",
        "mission": "Find realistic short-term income options",
        "prompt": (
            "You are HUSTLER, a side-income agent for a senior cloud/network "
            "engineer. Suggest realistic freelance or contract work that can "
            "start this week, including platforms, rates to research, and a "
            "48-hour action plan."
        ),
    },
    "closer": {
        "name": "CLOSER",
        "mission": "Prepare offer negotiation scripts",
        "prompt": (
            "You are CLOSER, an offer negotiation agent for a cloud/network "
            "engineer. Provide negotiation scripts, compensation research "
            "steps, and ways to negotiate beyond base salary."
        ),
    },
    "anchor": {
        "name": "ANCHOR",
        "mission": "Create a daily momentum briefing",
        "prompt": (
            "You are ANCHOR, a momentum agent. Give an honest daily briefing "
            "for someone rebuilding after a job loss: what matters today, what "
            "to ignore, and the single highest-value action."
        ),
    },
    "prophet": {
        "name": "PROPHET",
        "mission": "Identify risks and blind spots",
        "prompt": (
            "You are PROPHET, a pattern detection agent. Identify likely risks "
            "during a career transition, including financial, operational, "
            "healthcare, and focus risks. Be direct and practical."
        ),
    },
}


def build_client():
    if anthropic is None:
        return None, "The anthropic package is not installed."

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None, "ANTHROPIC_API_KEY is not set."

    return anthropic.Anthropic(api_key=api_key), None


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "alive",
            "timestamp": datetime.now().isoformat(),
            "agents": len(AGENTS),
        }
    )


@app.route("/agents")
def list_agents():
    return jsonify(
        [
            {"id": agent_id, "name": agent["name"], "mission": agent["mission"]}
            for agent_id, agent in AGENTS.items()
        ]
    )


@app.route("/agents/<agent_id>/deploy", methods=["POST"])
def deploy(agent_id):
    if agent_id not in AGENTS:
        return jsonify({"error": "Agent not found"}), 404

    client, error = build_client()
    if error:
        return jsonify({"error": error}), 503

    agent = AGENTS[agent_id]
    message = client.messages.create(
        model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
        max_tokens=int(os.environ.get("ANTHROPIC_MAX_TOKENS", "1000")),
        messages=[{"role": "user", "content": agent["prompt"]}],
    )

    return jsonify(
        {
            "agent": agent["name"],
            "result": message.content[0].text,
            "timestamp": datetime.now().isoformat(),
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "").lower() in {"1", "true", "yes"}
    print("AI Army backend online")
    print(f"http://localhost:{port}")
    app.run(debug=debug, port=port)
