"use client";

import { useEffect, useMemo, useState } from "react";

type View = "overview" | "process" | "runs" | "evals" | "governance" | "architecture";
type Language = "en" | "ka";
type Theme = "dark" | "light";

const copy = {
  en: {
    subtitle: "Governed agent harness for internal bank operations",
    synthetic: "SYNTHETIC PORTFOLIO DEMO",
    nav: { overview: "Control tower", process: "Process graph", runs: "Run explorer", evals: "Eval lab", governance: "Governance", architecture: "System map" },
    overviewTitle: "Operational intelligence, under control.",
    overviewIntro: "One governed execution layer for cases, agents, knowledge, approvals and evidence—without replacing authoritative banking systems.",
    processTitle: "Product & Process Change",
    processIntro: "A versioned process package combining deterministic control flow with bounded agent work and human decisions.",
    runsTitle: "Every decision is reconstructable.",
    runsIntro: "Inspect the graph path, agent loop, evidence, policy decision, model cost and human intervention for each case.",
    evalsTitle: "Quality is a release gate.",
    evalsIntro: "Offline regression, in-run quality gates and production signals are evaluated together before a process version can advance.",
    governanceTitle: "Agents operate inside policy.",
    governanceIntro: "Capabilities are explicit, tools are guarded, and consequential actions stop for authenticated human approval.",
    architectureTitle: "Harness, not another chatbot.",
    architectureIntro: "The Banking AI Core coordinates internal operations across channels, workflows, agents, models and bank systems.",
  },
  ka: {
    subtitle: "მართული აგენტური ჰარნესი ბანკის შიდა ოპერაციებისთვის",
    synthetic: "სინთეტიკური პორტფოლიო დემო",
    nav: { overview: "მართვის ცენტრი", process: "პროცესის გრაფი", runs: "გაშვების ანალიზი", evals: "შეფასებების ლაბი", governance: "მმართველობა", architecture: "სისტემის რუკა" },
    overviewTitle: "ოპერაციული ინტელექტი — კონტროლის ქვეშ.",
    overviewIntro: "ერთიანი მართული შესრულების ფენა ქეისებისთვის, აგენტებისთვის, ცოდნისთვის, დამტკიცებებისთვის და მტკიცებულებებისთვის — ძირითადი საბანკო სისტემების ჩანაცვლების გარეშე.",
    processTitle: "პროდუქტისა და პროცესის ცვლილება",
    processIntro: "ვერსირებული პროცესის პაკეტი, რომელიც აერთიანებს დეტერმინისტულ მართვას, შეზღუდულ აგენტურ მუშაობას და ადამიანის გადაწყვეტილებებს.",
    runsTitle: "ყველა გადაწყვეტილება აღდგენადია.",
    runsIntro: "იხილეთ გრაფის გზა, აგენტის ციკლი, მტკიცებულება, პოლიტიკის გადაწყვეტილება, მოდელის ღირებულება და ადამიანის ჩარევა.",
    evalsTitle: "ხარისხი რელიზის სავალდებულო პირობაა.",
    evalsIntro: "ოფლაინ რეგრესია, პროცესშივე ხარისხის კონტროლი და საწარმო სიგნალები ერთად ფასდება.",
    governanceTitle: "აგენტები პოლიტიკის ფარგლებში მოქმედებენ.",
    governanceIntro: "შესაძლებლობები მკაფიოა, ინსტრუმენტები დაცულია, ხოლო მნიშვნელოვანი მოქმედებები ადამიანის დამტკიცებას ელოდება.",
    architectureTitle: "ჰარნესი და არა კიდევ ერთი ჩატბოტი.",
    architectureIntro: "Banking AI Core აერთიანებს არხებს, პროცესებს, აგენტებს, მოდელებს და ბანკის სისტემებს.",
  },
} as const;

const graphNodes = [
  { id: "intake", title: "Intake & preserve", kind: "system", status: "done" },
  { id: "classify", title: "Classify change", kind: "agent", status: "done" },
  { id: "validate", title: "Validate evidence", kind: "control", status: "done" },
  { id: "retrieve", title: "Retrieve source", kind: "knowledge", status: "done" },
  { id: "impact", title: "Parallel impact", kind: "agent", status: "active" },
  { id: "evaluate", title: "Quality gate", kind: "eval", status: "next" },
  { id: "approve", title: "Human approval", kind: "human", status: "next" },
  { id: "commit", title: "Controlled action", kind: "system", status: "next" },
];

const trace = [
  { time: "09:42:01", title: "Case registered", detail: "Original request preserved · checksum 8f2…a91", type: "system", cost: "—" },
  { time: "09:42:03", title: "Change classified", detail: "CHANGE_TO_EXISTING / PROCESS · confidence 0.96", type: "agent", cost: "$0.004" },
  { time: "09:42:04", title: "Evidence policy passed", detail: "Risk, Legal and InfoSec references present", type: "policy", cost: "—" },
  { time: "09:42:06", title: "Source retrieved", detail: "OPS-PROC-014 · v3.2 · semantic score 0.91", type: "knowledge", cost: "$0.001" },
  { time: "09:42:12", title: "Impact agents completed", detail: "Risk · Operations · Technology · 3/3 returned", type: "agent", cost: "$0.012" },
  { time: "09:42:13", title: "Citation eval failed", detail: "Technology finding #2 lacked an authoritative source", type: "eval", cost: "—" },
  { time: "09:42:16", title: "Bounded retry succeeded", detail: "Iteration 2/3 · evidence coverage now 100%", type: "agent", cost: "$0.003" },
  { time: "09:42:18", title: "Product Support approval requested", detail: "Execution paused at durable checkpoint", type: "human", cost: "—" },
];

const evalRows = [
  ["Classification accuracy", "98.0%", "≥ 95%", "pass"],
  ["Required evidence coverage", "100%", "100%", "pass"],
  ["Citation validity", "96.4%", "≥ 95%", "pass"],
  ["Policy-compliant routing", "100%", "100%", "pass"],
  ["Human override rate", "8.2%", "≤ 15%", "pass"],
  ["P95 case preparation", "4m 18s", "≤ 5m", "pass"],
  ["Cost per prepared case", "$0.19", "≤ $0.25", "pass"],
];

function Mark({ kind }: { kind: string }) { return <span className={`mark mark-${kind}`} aria-hidden="true" />; }
function StatusPill({ children, tone = "neutral" }: { children: React.ReactNode; tone?: string }) { return <span className={`status-pill status-${tone}`}>{children}</span>; }

export default function Home() {
  const [view, setView] = useState<View>("overview");
  const [language, setLanguage] = useState<Language>("en");
  const [theme, setTheme] = useState<Theme>("dark");
  const [approval, setApproval] = useState<"pending" | "approved" | "rejected">("pending");
  const [selectedNode, setSelectedNode] = useState("impact");
  const t = copy[language];

  useEffect(() => { document.documentElement.dataset.theme = theme; }, [theme]);
  const title = useMemo(() => ({
    overview: [t.overviewTitle, t.overviewIntro], process: [t.processTitle, t.processIntro], runs: [t.runsTitle, t.runsIntro],
    evals: [t.evalsTitle, t.evalsIntro], governance: [t.governanceTitle, t.governanceIntro], architecture: [t.architectureTitle, t.architectureIntro],
  }[view]), [t, view]);

  return <main className="app-shell">
    <aside className="sidebar">
      <div className="brand-block"><div className="brand-mark">BA</div><div><strong>Banking AI Core</strong><span>AGENTIC HARNESS / 0.1</span></div></div>
      <nav aria-label="Primary navigation">{(Object.keys(t.nav) as View[]).map((item, index) => <button key={item} className={view === item ? "nav-item active" : "nav-item"} onClick={() => setView(item)}><span>0{index + 1}</span>{t.nav[item]}</button>)}</nav>
      <div className="sidebar-foot"><div className="runtime-line"><span className="pulse" />Harness runtime healthy</div><div className="sidebar-metric"><span>MODEL ROUTE</span><strong>OLLAMA / LOCAL</strong></div><div className="sidebar-metric"><span>ACTIVE POLICY</span><strong>BANK-INTERNAL / V4</strong></div></div>
    </aside>
    <section className="workspace">
      <header className="topbar"><div className="breadcrumb">CORE / {view.toUpperCase()} <StatusPill tone="demo">{t.synthetic}</StatusPill></div><div className="controls"><button onClick={() => setLanguage(language === "en" ? "ka" : "en")} aria-label="Change language">{language === "en" ? "KA" : "EN"}</button><button onClick={() => setTheme(theme === "dark" ? "light" : "dark")} aria-label="Change theme">{theme === "dark" ? "LIGHT" : "DARK"}</button><div className="avatar">MJ</div></div></header>
      <div className="content"><div className="view-heading"><div><span className="kicker">BANKING AI CORE / {view}</span><h1>{title[0]}</h1><p>{title[1]}</p></div><div className="release-card"><span>ACTIVE RELEASE</span><strong>product-change@0.1.0</strong><small>Approved for simulation</small></div></div>
        {view === "overview" && <Overview setView={setView} />}{view === "process" && <ProcessGraph selectedNode={selectedNode} setSelectedNode={setSelectedNode} />}{view === "runs" && <RunExplorer approval={approval} setApproval={setApproval} />}{view === "evals" && <EvalLab />}{view === "governance" && <Governance />}{view === "architecture" && <Architecture />}
      </div>
    </section>
  </main>;
}

function Overview({ setView }: { setView: (view: View) => void }) {
  const metrics = [["Active cases", "24", "+6 this week"], ["Awaiting humans", "7", "3 high priority"], ["Eval pass rate", "96.4%", "+2.1 pts"], ["Cost / case", "$0.19", "−14%"]];
  return <><div className="metric-grid">{metrics.map(([label, value, note]) => <article className="metric-card" key={label}><span>{label}</span><strong>{value}</strong><small>{note}</small></article>)}</div>
    <div className="overview-grid"><article className="panel system-panel"><div className="panel-head"><div><span className="kicker">LIVE HARNESS MAP</span><h2>From intake to evidence</h2></div><button className="text-button" onClick={() => setView("architecture")}>EXPLORE SYSTEM →</button></div><div className="harness-map">{["Channels", "Process router", "LangGraph runtime", "Policy & approvals", "Bank adapters"].map((label, index) => <div className="harness-node" key={label}><span>0{index + 1}</span><strong>{label}</strong><small>{["Workbench · API", "Intent · package", "Cases · agents", "HITL · controls", "Systems of record"][index]}</small></div>)}</div><div className="foundation-row"><span>KNOWLEDGE FABRIC</span><span>MODEL GATEWAY</span><span>EVIDENCE LEDGER</span><span>OBSERVABILITY + EVALS</span></div></article>
      <article className="panel queue-panel"><div className="panel-head"><div><span className="kicker">MY WORK</span><h2>Approval queue</h2></div><span className="count-badge">07</span></div>{["Product onboarding procedure", "Digital archive retention", "SME pricing exception"].map((name, index) => <button className="queue-row" key={name} onClick={() => setView("runs")}><span className={`priority p${index}`}>P{index + 1}</span><div><strong>{name}</strong><small>CASE-2026-0{142 + index} · Product Support</small></div><span>→</span></button>)}</article></div>
    <div className="lower-grid"><article className="panel"><div className="panel-head"><div><span className="kicker">PROCESS PORTFOLIO</span><h2>Operational packages</h2></div></div><div className="process-list"><button onClick={() => setView("process")}><Mark kind="active"/><span><strong>Product & Process Change</strong><small>8 graph nodes · 3 agents · 7 evals</small></span><StatusPill tone="live">LIVE</StatusPill></button><button><Mark kind="prototype"/><span><strong>Procurement Request</strong><small>Existing validated vertical slice</small></span><StatusPill tone="prototype">PROTOTYPE</StatusPill></button><button><Mark kind="planned"/><span><strong>Audit Evidence Preparation</strong><small>Process package specification</small></span><StatusPill>PLANNED</StatusPill></button></div></article>
      <article className="panel signal-panel"><span className="kicker">QUALITY SIGNAL / 7 DAYS</span><div className="signal-value">96.4<small>%</small></div><div className="spark-bars">{[44,62,55,78,70,88,94,86,98,92,100,96].map((height, i) => <i key={i} style={{height: `${height}%`}} />)}</div><p>1,248 evaluated agent steps · 14 human overrides · 0 policy breaches</p></article></div></>;
}

function ProcessGraph({ selectedNode, setSelectedNode }: { selectedNode: string; setSelectedNode: (id: string) => void }) {
  const current = graphNodes.find((node) => node.id === selectedNode) ?? graphNodes[0];
  return <div className="process-layout"><article className="panel graph-panel"><div className="panel-head"><div><span className="kicker">EXECUTABLE PROCESS GRAPH / V0.1.0</span><h2>Change-to-existing path</h2></div><div className="legend"><span><Mark kind="agent"/>Agent</span><span><Mark kind="human"/>Human</span><span><Mark kind="system"/>System</span></div></div><div className="graph-canvas">{graphNodes.map((node, index) => <div className="graph-item" key={node.id}><button className={`graph-node kind-${node.kind} node-${node.status} ${selectedNode === node.id ? "selected" : ""}`} onClick={() => setSelectedNode(node.id)}><span>0{index + 1}</span><strong>{node.title}</strong><small>{node.kind.toUpperCase()}</small></button>{index < graphNodes.length - 1 && <div className="connector"><i /></div>}</div>)}</div><div className="graph-branch"><span>WHEN EVAL FAILS</span><div>Quality gate <b>→</b> bounded retrieval retry <b>→</b> max 3 iterations <b>→</b> human escalation</div></div></article>
    <aside className="inspector panel"><span className="kicker">NODE INSPECTOR</span><h2>{current.title}</h2><StatusPill tone={current.kind}>{current.kind.toUpperCase()}</StatusPill><dl><div><dt>Owner</dt><dd>{current.kind === "human" ? "Product Support" : current.kind === "agent" ? "Impact Analysis Agent" : "Harness Runtime"}</dd></div><div><dt>Timeout</dt><dd>{current.kind === "agent" ? "60 seconds" : "Policy controlled"}</dd></div><div><dt>Retry</dt><dd>{current.kind === "agent" ? "3 bounded attempts" : "No autonomous retry"}</dd></div><div><dt>Evidence</dt><dd>Required and logged</dd></div></dl><div className="inspector-section"><span>INPUT CONTRACT</span><code>case_id · source_version · evidence_refs · policy_context</code></div><div className="inspector-section"><span>OUTPUT CONTRACT</span><code>finding[] · citations[] · confidence · obligations[]</code></div><div className="guardrail"><strong>CONTROL PRINCIPLE</strong><p>Probabilistic components prepare and propose. Deterministic services authorize, persist and commit.</p></div></aside>
    <article className="panel loop-panel"><div className="panel-head"><div><span className="kicker">BOUNDED AGENT LOOP</span><h2>Inside “Parallel impact”</h2></div><StatusPill tone="live">ITERATION 2 / 3</StatusPill></div><div className="loop-track">{["Plan", "Retrieve", "Analyze", "Cite", "Evaluate", "Stop / retry"].map((x,i)=><div key={x} className={i===4?"loop-active":""}><span>0{i+1}</span><strong>{x}</strong></div>)}</div></article></div>;
}

function RunExplorer({ approval, setApproval }: { approval: string; setApproval: (value: "pending" | "approved" | "rejected") => void }) {
  return <div className="run-layout"><article className="panel run-summary"><div><span className="kicker">CASE-2026-0142</span><h2>Digital archive retention process</h2><p>Change to an existing internal operations procedure.</p></div><div className="run-facts"><span>STATUS<strong>{approval === "pending" ? "Awaiting approval" : approval}</strong></span><span>GRAPH<strong>product-change@0.1.0</strong></span><span>TRACE<strong>tr_81bf29e4</strong></span><span>COST<strong>$0.020</strong></span></div></article>
    <article className="panel timeline-panel"><div className="panel-head"><div><span className="kicker">DURABLE EVENT STREAM</span><h2>Run trace</h2></div><StatusPill tone="live">REPLAYABLE</StatusPill></div><div className="timeline">{trace.map((item, index) => <div className="trace-row" key={item.time}><time>{item.time}</time><div className={`trace-dot trace-${item.type}`} /><div><strong>{item.title}</strong><p>{item.detail}</p></div><span>{item.cost}</span>{index < trace.length - 1 && <i />}</div>)}</div></article>
    <aside className="panel approval-panel"><span className="kicker">HUMAN CONTROL GATE</span><h2>Product Support review</h2>{approval === "pending" ? <><p>The agent package passed automated evals. Confirm that the evidence and proposed document are suitable for controlled review.</p><div className="approval-score"><span>Evidence coverage<strong>100%</strong></span><span>Policy checks<strong>8 / 8</strong></span><span>Open assumptions<strong>1</strong></span></div><label>Decision note<textarea defaultValue="Evidence references verified. Release to departmental review." /></label><div className="approval-actions"><button className="reject" onClick={() => setApproval("rejected")}>REJECT</button><button className="approve" onClick={() => setApproval("approved")}>APPROVE & RESUME</button></div></> : <div className={`decision-result ${approval}`}><span>{approval === "approved" ? "✓" : "×"}</span><strong>Case {approval}</strong><p>The decision was recorded as an immutable evidence event. The demo can be reset safely.</p><button onClick={() => setApproval("pending")}>RESET DEMO</button></div>}</aside></div>;
}

function EvalLab() { return <div className="eval-layout"><div className="score-grid"><article><span>RELEASE SCORE</span><strong>96.4</strong><small>PASS / 90 REQUIRED</small></article><article><span>GOLDEN CASES</span><strong>50</strong><small>49 PASS · 1 REVIEW</small></article><article><span>POLICY BREACHES</span><strong>0</strong><small>LAST 1,248 STEPS</small></article><article><span>REGRESSION</span><strong>+2.1</strong><small>VS VERSION 0.0.3</small></article></div><article className="panel eval-table"><div className="panel-head"><div><span className="kicker">RELEASE GATE / PRODUCT-CHANGE@0.1.0</span><h2>Evaluation suite</h2></div><button className="run-evals">RUN 50 CASES</button></div><div className="table-head"><span>METRIC</span><span>RESULT</span><span>THRESHOLD</span><span>GATE</span></div>{evalRows.map(([metric,result,threshold,status])=><div className="table-row" key={metric}><strong>{metric}</strong><span>{result}</span><span>{threshold}</span><StatusPill tone={status}>{status.toUpperCase()}</StatusPill></div>)}</article><article className="panel eval-method"><div><span className="kicker">THREE-LAYER EVALUATION</span><h2>Test before, during and after release.</h2></div>{[["01","OFFLINE","Golden cases · adversarial inputs · regression"],["02","IN-RUN","Evidence · citations · policy · confidence"],["03","PRODUCTION","Overrides · failures · latency · cost · drift"]].map(x=><div key={x[0]}><span>{x[0]}</span><strong>{x[1]}</strong><p>{x[2]}</p></div>)}</article></div>; }

function Governance() {
  const policies = [["Data classification","INTERNAL","External model egress blocked"],["Tool execution","APPROVAL","Writes require one-time human authorization"],["Model budget","ENFORCED","$0.25 maximum per prepared case"],["Evidence","REQUIRED","Every material claim must cite a source"]];
  const tools = [["search_bank_memory","READ","Chroma / approved corpus"],["get_process_source","READ","Document registry"],["create_review_task","WRITE","Case service · approval"],["notify_reviewers","WRITE","Channel gateway · approval"]];
  return <div className="governance-layout"><article className="panel policy-panel"><div className="panel-head"><div><span className="kicker">ACTIVE POLICY PROFILE</span><h2>bank-internal / v4</h2></div><StatusPill tone="live">ENFORCED</StatusPill></div>{policies.map(([name,status,detail])=><div className="policy-row" key={name}><Mark kind="policy"/><div><strong>{name}</strong><p>{detail}</p></div><span>{status}</span></div>)}</article><article className="panel tool-panel"><div className="panel-head"><div><span className="kicker">CAPABILITY REGISTRY</span><h2>Guarded tools</h2></div><span className="count-badge">04</span></div>{tools.map(([name,mode,provider])=><div className="tool-row" key={name}><code>{name}</code><StatusPill tone={mode === "WRITE" ? "human" : "neutral"}>{mode}</StatusPill><span>{provider}</span></div>)}</article><article className="panel responsibility-panel"><span className="kicker">AUTHORITY BOUNDARY</span><div className="authority-grid">{[["MODEL","Propose","Interpret, classify, retrieve, draft and recommend."],["LANGGRAPH","Coordinate","Route state through controlled nodes and pause points."],["POLICY","Authorize","Enforce identity, data, capability and obligation rules."],["BANK SYSTEM","Commit","Persist authoritative records through controlled adapters."]].map(x=><div key={x[0]}><span>{x[0]}</span><strong>{x[1]}</strong><p>{x[2]}</p></div>)}</div></article></div>;
}

function Architecture() {
  const layers = [["01","EXPERIENCE PLANE","Operational workbench · APIs · approved channels","Employees create cases and act on human tasks."],["02","CONTROL PLANE","Router · process registry · policy · approvals","Deterministic services select and govern execution."],["03","AGENT RUNTIME","LangGraph · bounded agents · sandboxes","Stateful graphs coordinate agentic and deterministic work."],["04","INTELLIGENCE PLANE","Ollama · Bedrock route · Chroma · Bank Memory","Models and knowledge are selected by policy and data class."],["05","INTEGRATION PLANE","MCP · APIs · enterprise adapters","Guarded capabilities connect to systems of record."],["06","EVIDENCE PLANE","Events · traces · evals · cost ledger","Every material decision remains attributable and replayable."]];
  return <div className="architecture-layout"><article className="panel architecture-stack">{layers.map(([num,name,tech,detail],index)=><div className="architecture-layer" key={num}><span>{num}</span><div><strong>{name}</strong><small>{tech}</small></div><p>{detail}</p><i style={{width:`${100-index*7}%`}} /></div>)}</article><aside className="panel boundary-panel"><span className="kicker">EXPLICIT NON-GOALS</span><h2>The harness does not become the bank.</h2><ul><li>Does not execute payments or financial transactions</li><li>Does not make autonomous credit decisions</li><li>Does not replace core banking or the data warehouse</li><li>Does not bypass departmental or Board authority</li><li>Does not treat an LLM transcript as an audit ledger</li></ul><div className="architecture-note"><strong>PORTFOLIO BOUNDARY</strong><p>The web interface uses synthetic cases. The repository contains an executable LangGraph vertical slice; enterprise adapters remain explicit interfaces.</p></div></aside></div>;
}
