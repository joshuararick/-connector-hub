from datetime import datetime
import os

from flask import Flask, jsonify, render_template_string

try:
    import anthropic
except ImportError:  # pragma: no cover - depends on local environment
    anthropic = None


app = Flask(__name__)


PAGE_SHELL = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }} - AI Army</title>
  <style>
    :root {
      --bg: #0b1018;
      --panel: #141c29;
      --panel-2: #192435;
      --line: rgba(255,255,255,.11);
      --text: #eef4ff;
      --muted: #a9b6ca;
      --accent: #5eead4;
      --accent-2: #60a5fa;
      --warn: #fbbf24;
      --bad: #fb7185;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, Segoe UI, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
    }
    a { color: inherit; text-decoration: none; }
    .topbar {
      position: sticky;
      top: 0;
      z-index: 2;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      padding: 16px clamp(18px, 4vw, 56px);
      background: rgba(11,16,24,.92);
      border-bottom: 1px solid var(--line);
      backdrop-filter: blur(12px);
    }
    .brand { font-weight: 900; letter-spacing: .02em; }
    nav { display: flex; gap: 10px; flex-wrap: wrap; color: var(--muted); }
    nav a { padding: 8px 10px; border-radius: 6px; }
    nav a:hover { background: rgba(255,255,255,.07); color: var(--text); }
    main { padding: clamp(24px, 5vw, 64px); }
    .hero {
      display: grid;
      grid-template-columns: minmax(0, 1.2fr) minmax(280px, .8fr);
      gap: 24px;
      align-items: stretch;
      margin-bottom: 28px;
    }
    h1 {
      margin: 0 0 14px;
      font-size: clamp(34px, 6vw, 68px);
      line-height: .98;
      letter-spacing: 0;
    }
    h2 { margin: 0 0 14px; font-size: 24px; }
    h3 { margin: 0 0 8px; font-size: 18px; }
    p { color: var(--muted); line-height: 1.65; }
    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 22px;
    }
    .metric-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }
    .metric {
      background: var(--panel-2);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
    }
    .metric b { display: block; font-size: 30px; }
    .muted { color: var(--muted); }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 14px;
    }
    .agent {
      display: grid;
      gap: 12px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
    }
    .agent header {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: start;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      min-height: 26px;
      padding: 4px 8px;
      border-radius: 999px;
      background: rgba(94,234,212,.12);
      color: var(--accent);
      font-size: 12px;
      font-weight: 800;
      white-space: nowrap;
    }
    .actions { display: flex; gap: 10px; flex-wrap: wrap; }
    button, .button {
      appearance: none;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.08);
      color: var(--text);
      border-radius: 6px;
      padding: 10px 12px;
      font-weight: 800;
      cursor: pointer;
    }
    button.primary, .button.primary {
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      color: #06111f;
      border: 0;
    }
    pre {
      margin: 0;
      padding: 18px;
      overflow: auto;
      white-space: pre-wrap;
      word-break: break-word;
      background: #070b11;
      border: 1px solid var(--line);
      border-radius: 8px;
      color: #dbeafe;
      line-height: 1.55;
    }
    .notice {
      border-left: 4px solid var(--warn);
      background: rgba(251,191,36,.09);
    }
    .error {
      border-left: 4px solid var(--bad);
      background: rgba(251,113,133,.09);
    }
    @media (max-width: 820px) {
      .hero { grid-template-columns: 1fr; }
      .metric-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header class="topbar">
    <a class="brand" href="/">AI Army</a>
    <nav>
      <a href="/">Home</a>
      <a href="/agents">Agents</a>
      <a href="/health">Health</a>
      <a href="/api/agents">JSON API</a>
      <a href="http://127.0.0.1:8087/">Command Center</a>
    </nav>
  </header>
  <main>
    {{ body|safe }}
  </main>
</body>
</html>
"""


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


def page(title, body):
    return render_template_string(PAGE_SHELL, title=title, body=body)


def agent_cards():
    cards = []
    for agent_id, agent in AGENTS.items():
        cards.append(
            f"""
            <article class="agent">
              <header>
                <div>
                  <h3>{agent["name"]}</h3>
                  <p>{agent["mission"]}</p>
                </div>
                <span class="badge">{agent_id}</span>
              </header>
              <div class="actions">
                <a class="button" href="/agents/{agent_id}">Read brief</a>
                <form action="/agents/{agent_id}/deploy" method="post">
                  <button class="primary" type="submit">Deploy</button>
                </form>
              </div>
            </article>
            """
        )
    return "\n".join(cards)


@app.route("/")
def home_page():
    return page(
        "Home",
        f"""
        <section class="hero">
          <div class="panel">
            <h1>AI Army backend, readable for humans.</h1>
            <p>
              This is the local control surface for the backend agents. Use it
              to inspect agents, check service health, and deploy a selected
              agent once a rotated Anthropic key is available in the environment.
            </p>
            <div class="actions">
              <a class="button primary" href="/agents">Open agents</a>
              <a class="button" href="/health">Check health</a>
            </div>
          </div>
          <aside class="panel">
            <h2>Status</h2>
            <div class="metric-grid">
              <div class="metric"><b>{len(AGENTS)}</b><span class="muted">Agents</span></div>
              <div class="metric"><b>{'Yes' if os.environ.get('ANTHROPIC_API_KEY') else 'No'}</b><span class="muted">API key set</span></div>
              <div class="metric"><b>5000</b><span class="muted">Backend port</span></div>
            </div>
          </aside>
        </section>
        <section class="panel notice">
          <h2>Safety note</h2>
          <p>
            Do not paste production secrets into repo files. Set
            <code>ANTHROPIC_API_KEY</code> only in your local shell or a secure
            secret manager.
          </p>
        </section>
        """,
    )


@app.route("/health")
def health_page():
    api_key_set = bool(os.environ.get("ANTHROPIC_API_KEY"))
    return page(
        "Health",
        f"""
        <section class="hero">
          <div class="panel">
            <h1>Backend health</h1>
            <p>The Flask service is online and responding.</p>
          </div>
          <aside class="panel">
            <h2>Runtime</h2>
            <div class="metric-grid">
              <div class="metric"><b>Alive</b><span class="muted">Status</span></div>
              <div class="metric"><b>{len(AGENTS)}</b><span class="muted">Agents</span></div>
              <div class="metric"><b>{'Set' if api_key_set else 'Missing'}</b><span class="muted">Anthropic key</span></div>
            </div>
          </aside>
        </section>
        <section class="panel">
          <h2>Machine endpoint</h2>
          <p>Raw JSON is still available at <a href="/api/health">/api/health</a>.</p>
        </section>
        """,
    )


@app.route("/agents")
def agents_page():
    return page(
        "Agents",
        f"""
        <section class="panel">
          <h1>Agents</h1>
          <p>
            Pick an agent to read its mission and prompt, or deploy it once your
            local Anthropic key is set.
          </p>
        </section>
        <section class="grid" style="margin-top: 18px;">
          {agent_cards()}
        </section>
        """,
    )


@app.route("/agents/<agent_id>")
def agent_detail_page(agent_id):
    if agent_id not in AGENTS:
        return page("Agent not found", '<section class="panel error"><h1>Agent not found</h1><p>That agent ID does not exist.</p></section>'), 404

    agent = AGENTS[agent_id]
    return page(
        agent["name"],
        f"""
        <section class="panel">
          <span class="badge">{agent_id}</span>
          <h1>{agent["name"]}</h1>
          <p>{agent["mission"]}</p>
          <h2>Prompt</h2>
          <pre>{agent["prompt"]}</pre>
          <div class="actions" style="margin-top: 16px;">
            <form action="/agents/{agent_id}/deploy" method="post">
              <button class="primary" type="submit">Deploy {agent["name"]}</button>
            </form>
            <a class="button" href="/agents">Back to agents</a>
          </div>
        </section>
        """,
    )


@app.route("/api/health")
def health_api():
    return jsonify(
        {
            "status": "alive",
            "timestamp": datetime.now().isoformat(),
            "agents": len(AGENTS),
        }
    )


@app.route("/api/agents")
def list_agents_api():
    return jsonify(
        [
            {"id": agent_id, "name": agent["name"], "mission": agent["mission"]}
            for agent_id, agent in AGENTS.items()
        ]
    )


def run_agent(agent_id):
    if agent_id not in AGENTS:
        return None, "Agent not found", 404

    client, error = build_client()
    if error:
        return None, error, 503

    agent = AGENTS[agent_id]
    message = client.messages.create(
        model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
        max_tokens=int(os.environ.get("ANTHROPIC_MAX_TOKENS", "1000")),
        messages=[{"role": "user", "content": agent["prompt"]}],
    )
    return message.content[0].text, None, 200


@app.route("/agents/<agent_id>/deploy", methods=["POST"])
def deploy_page(agent_id):
    result, error, status = run_agent(agent_id)
    if error:
        body = f"""
        <section class="panel error">
          <h1>Could not deploy agent</h1>
          <p>{error}</p>
          <div class="actions">
            <a class="button" href="/agents/{agent_id}">Back to agent</a>
            <a class="button" href="/agents">All agents</a>
          </div>
        </section>
        """
        return page("Deploy failed", body), status

    agent = AGENTS[agent_id]
    return page(
        f"{agent['name']} result",
        f"""
        <section class="panel">
          <span class="badge">{agent_id}</span>
          <h1>{agent["name"]} result</h1>
          <pre>{result}</pre>
          <div class="actions" style="margin-top: 16px;">
            <a class="button" href="/agents/{agent_id}">Back to agent</a>
            <a class="button" href="/agents">All agents</a>
          </div>
        </section>
        """,
    )


@app.route("/api/agents/<agent_id>/deploy", methods=["POST"])
def deploy_api(agent_id):
    result, error, status = run_agent(agent_id)
    if error:
        return jsonify({"error": error}), status

    return jsonify(
        {
            "agent": AGENTS[agent_id]["name"],
            "result": result,
            "timestamp": datetime.now().isoformat(),
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "").lower() in {"1", "true", "yes"}
    print("AI Army backend online")
    print(f"http://localhost:{port}")
    app.run(debug=debug, port=port)
