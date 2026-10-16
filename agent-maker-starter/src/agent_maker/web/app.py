#!/usr/bin/env python3
"""Josh's AI Army — Web Command Center"""
from __future__ import annotations

import json
import sys
import threading
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent_maker.core.orchestrator import Orchestrator
from agent_maker.core.llm_planner import LLMPlanner
from agent_maker.tools.basic import default_registry
from agent_maker.tools.brain_tools import get_brain_tools
from agent_maker.tools.registry import Tool

BRAIN_FILE = Path("C:/Users/joshu/Brain of Ai/brain-server/data.json")

def get_brain():
    try:
        if BRAIN_FILE.exists():
            return json.loads(BRAIN_FILE.read_text())
    except: pass
    return {}

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Josh's AI Army</title>
<style>
:root {
  --bg: #0a0a0f;
  --surface: #13131a;
  --surface2: #1c1c28;
  --border: #2a2a3d;
  --accent: #7c3aed;
  --accent2: #a855f7;
  --green: #10b981;
  --yellow: #f59e0b;
  --red: #ef4444;
  --blue: #3b82f6;
  --text: #f0f0f8;
  --muted: #6b7280;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; min-height: 100vh; }
.header { background: var(--surface); border-bottom: 1px solid var(--border); padding: 16px 24px; display: flex; align-items: center; gap: 16px; }
.logo { width: 36px; height: 36px; background: linear-gradient(135deg, var(--accent), var(--accent2)); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
.header h1 { font-size: 20px; font-weight: 700; }
.header p { font-size: 12px; color: var(--muted); margin-top: 2px; }
.layout { display: grid; grid-template-columns: 300px 1fr; gap: 0; height: calc(100vh - 69px); }
.sidebar { background: var(--surface); border-right: 1px solid var(--border); overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 20px; }
.main { overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 20px; }

.brain-card { background: var(--surface2); border: 1px solid var(--border); border-radius: 12px; padding: 16px; }
.brain-card h3 { font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); margin-bottom: 12px; }
.brain-item { display: flex; align-items: flex-start; gap: 8px; margin-bottom: 8px; }
.brain-dot { width: 6px; height: 6px; border-radius: 50%; margin-top: 6px; flex-shrink: 0; }
.brain-text { font-size: 12px; color: #ccc; line-height: 1.5; }
.tag { display: inline-block; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 99px; margin: 2px; }

.goal-box { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 24px; }
.goal-box h2 { font-size: 16px; font-weight: 600; margin-bottom: 16px; }
.goal-input { width: 100%; background: var(--bg); border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; color: var(--text); font-size: 15px; font-family: inherit; resize: none; outline: none; line-height: 1.5; }
.goal-input:focus { border-color: var(--accent); }
.btn-row { display: flex; gap: 10px; margin-top: 12px; }
.btn { padding: 10px 20px; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; border: none; transition: opacity .15s; }
.btn:active { opacity: .8; }
.btn-primary { background: var(--accent); color: white; }
.btn-secondary { background: var(--surface2); color: var(--text); border: 1px solid var(--border); }
.btn-green { background: var(--green); color: white; }

.quick-goals { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.quick-btn { background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; padding: 7px 12px; font-size: 12px; font-weight: 500; cursor: pointer; color: var(--text); transition: border-color .15s; }
.quick-btn:hover { border-color: var(--accent); }

.runs-section h2 { font-size: 16px; font-weight: 600; margin-bottom: 16px; }
.run-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 12px; }
.run-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.run-goal { font-size: 15px; font-weight: 500; }
.status-badge { font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 99px; }
.status-done { background: rgba(16,185,129,.15); color: var(--green); }
.status-running { background: rgba(245,158,11,.15); color: var(--yellow); }
.status-pending { background: rgba(107,114,128,.15); color: var(--muted); }

.steps { display: flex; flex-direction: column; gap: 8px; }
.step { display: flex; gap: 12px; align-items: flex-start; padding: 10px 12px; background: var(--surface2); border-radius: 8px; border-left: 3px solid transparent; }
.step.done { border-left-color: var(--green); }
.step.running { border-left-color: var(--yellow); }
.step.pending { border-left-color: var(--border); }
.step-id { font-size: 10px; font-weight: 700; color: var(--muted); min-width: 52px; padding-top: 2px; }
.step-content { flex: 1; }
.step-goal { font-size: 13px; font-weight: 500; margin-bottom: 4px; }
.step-result { font-size: 12px; color: #aaa; line-height: 1.5; }
.step-meta { display: flex; gap: 8px; margin-top: 4px; }
.risk-low { color: var(--green); }
.risk-medium { color: var(--yellow); }
.risk-high { color: var(--red); }
.tool-name { font-size: 10px; font-weight: 700; background: rgba(124,58,237,.2); color: var(--accent2); padding: 1px 6px; border-radius: 4px; }

.empty-state { text-align: center; padding: 48px; color: var(--muted); }
.empty-state .icon { font-size: 48px; margin-bottom: 12px; }
.empty-state p { font-size: 14px; }

.spinner { display: inline-block; width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-top-color: white; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
</head>
<body>
<div class="header">
  <div class="logo">🧠</div>
  <div>
    <h1>Josh's AI Army</h1>
    <p>Autonomous agent command center — Father · Husband · Creator</p>
  </div>
</div>

<div class="layout">
  <div class="sidebar">
    <div class="brain-card">
      <h3>🧠 Brain Context</h3>
      <div id="brain-content"><div style="color:#6b7280;font-size:12px">Loading...</div></div>
    </div>
    <div class="brain-card">
      <h3>⚡ AI Stack</h3>
      <div class="brain-item"><div class="brain-dot" style="background:#10b981"></div><div class="brain-text"><strong>Brain MCP</strong> — localhost:3336</div></div>
      <div class="brain-item"><div class="brain-dot" style="background:#3b82f6"></div><div class="brain-text"><strong>GPT-4o</strong> — localhost:3337</div></div>
      <div class="brain-item"><div class="brain-dot" style="background:#8b5cf6"></div><div class="brain-text"><strong>Gemini</strong> — localhost:3339</div></div>
      <div class="brain-item"><div class="brain-dot" style="background:#f59e0b"></div><div class="brain-text"><strong>Grok</strong> — localhost:3340</div></div>
    </div>
  </div>

  <div class="main">
    <div class="goal-box">
      <h2>What do you want to accomplish?</h2>
      <textarea class="goal-input" id="goal" rows="3" placeholder="e.g. Research the best way to grow my creator business and write a 30-day action plan..."></textarea>
      <div class="quick-goals">
        <button class="quick-btn" onclick="setGoal('Plan my week based on my brain context and goals')">📅 Plan my week</button>
        <button class="quick-btn" onclick="setGoal('Research ways to build a sustainable creator business and summarize top 5 strategies')">💡 Creator research</button>
        <button class="quick-btn" onclick="setGoal('Analyze my brain priorities and suggest what to focus on today')">🎯 Focus for today</button>
        <button class="quick-btn" onclick="setGoal('Create a financial plan to build a 6-month emergency fund')">💰 Finance plan</button>
        <button class="quick-btn" onclick="setGoal('Write a morning routine that helps me show up for my family and business')">🌅 Morning routine</button>
        <button class="quick-btn" onclick="setGoal('Research and summarize the latest in AI agents for small businesses')">🤖 AI research</button>
      </div>
      <div class="btn-row">
        <button class="btn btn-primary" onclick="runAgent()" id="run-btn">▶ Run Agent</button>
        <button class="btn btn-secondary" onclick="clearRuns()">Clear</button>
      </div>
    </div>

    <div class="runs-section">
      <h2>Agent Runs</h2>
      <div id="runs-container">
        <div class="empty-state">
          <div class="icon">🤖</div>
          <p>Enter a goal above and let the agent work</p>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
var runs = [];

function setGoal(text) {
  document.getElementById('goal').value = text;
  document.getElementById('goal').focus();
}

function runAgent() {
  var goal = document.getElementById('goal').value.trim();
  if (!goal) return;
  var btn = document.getElementById('run-btn');
  btn.innerHTML = '<span class="spinner"></span> Running...';
  btn.disabled = true;
  
  fetch('/run', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({goal: goal})
  })
  .then(r => r.json())
  .then(data => {
    runs.unshift(data);
    renderRuns();
    btn.innerHTML = '▶ Run Agent';
    btn.disabled = false;
  })
  .catch(e => {
    btn.innerHTML = '▶ Run Agent';
    btn.disabled = false;
    alert('Error: ' + e.message);
  });
}

function clearRuns() {
  runs = [];
  renderRuns();
}

function renderRuns() {
  var container = document.getElementById('runs-container');
  if (!runs.length) {
    container.innerHTML = '<div class="empty-state"><div class="icon">🤖</div><p>Enter a goal above and let the agent work</p></div>';
    return;
  }
  container.innerHTML = runs.map(run => {
    var statusClass = run.status === 'done' ? 'status-done' : run.status === 'running' ? 'status-running' : 'status-pending';
    var steps = (run.plan || []).map(step => {
      var riskClass = 'risk-' + (step.risk || 'low');
      return '<div class="step ' + (step.status || 'done') + '">' +
        '<div class="step-id">' + step.id + '</div>' +
        '<div class="step-content">' +
          '<div class="step-goal">' + (step.goal || '') + '</div>' +
          (step.result ? '<div class="step-result">' + step.result.substring(0,200) + (step.result.length > 200 ? '...' : '') + '</div>' : '') +
          '<div class="step-meta"><span class="tool-name">' + (step.tool || 'note') + '</span><span class="' + riskClass + '" style="font-size:10px;font-weight:700">' + (step.risk || 'low') + ' risk</span></div>' +
        '</div>' +
      '</div>';
    }).join('');
    return '<div class="run-card">' +
      '<div class="run-header"><div class="run-goal">' + run.goal + '</div><span class="status-badge ' + statusClass + '">' + (run.status || 'done') + '</span></div>' +
      '<div class="steps">' + steps + '</div>' +
    '</div>';
  }).join('');
}

function loadBrain() {
  fetch('/brain')
    .then(r => r.json())
    .then(data => {
      var html = '';
      if (data.identity) {
        html += '<div class="brain-item"><div class="brain-dot" style="background:#7c3aed"></div><div class="brain-text"><strong>' + data.identity.name + '</strong> — ' + (data.identity.roles || []).join(', ') + '</div></div>';
      }
      if (data.weekly_theme) {
        html += '<div class="brain-item"><div class="brain-dot" style="background:#3b82f6"></div><div class="brain-text">Theme: ' + data.weekly_theme + '</div></div>';
      }
      if (data.focus && data.focus.text) {
        html += '<div class="brain-item"><div class="brain-dot" style="background:#10b981"></div><div class="brain-text">Focus: ' + data.focus.text + '</div></div>';
      }
      Object.entries(data.life_areas || {}).forEach(([area, goal]) => {
        if (goal) html += '<div class="brain-item"><div class="brain-dot" style="background:#6b7280"></div><div class="brain-text"><strong>' + area + ':</strong> ' + goal.substring(0, 60) + '</div></div>';
      });
      document.getElementById('brain-content').innerHTML = html || '<div style="color:#6b7280;font-size:12px">No brain data</div>';
    }).catch(() => {});
}

loadBrain();
setInterval(loadBrain, 30000);

document.getElementById('goal').addEventListener('keydown', function(e) {
  if (e.key === 'Enter' && e.ctrlKey) runAgent();
});
</script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    
    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
    
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())
        elif parsed.path == "/brain":
            self.send_json(get_brain())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == "/run":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            goal = body.get("goal", "")
            try:
                registry = default_registry()
                from agent_maker.tools.brain_tools import get_brain_tools
                for t in get_brain_tools():
                    registry.register(t)
                
                planner = LLMPlanner()
                orch = Orchestrator(planner=planner, registry=registry)
                result = orch.run_goal(goal, auto_approve=True)
                self.send_json(result.model_dump())
            except Exception as e:
                self.send_json({"goal": goal, "status": "failed", "error": str(e), "plan": []})
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=7777):
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"AI Army Command Center running at http://localhost:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
