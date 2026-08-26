# The Banking OS Manifesto

## Why banking needs an operating layer

Banks do not lack systems. They have many: core banking platforms, payment engines, customer channels, workflow tools, document stores, data platforms, risk services and regulatory controls. Each is valuable, but the seams between them are where change becomes slow, knowledge fragments and operational risk accumulates.

A new product, policy or process often crosses several systems and departments. The bank must reconcile different data models, approval paths, vendor constraints and release cycles. Point-to-point integrations solve one request at a time, then become another dependency to maintain. AI added as isolated assistants can increase fragmentation instead of reducing it.

The answer is not another system of record. It is a **Banking OS**: a governed coordination layer above existing systems that makes capabilities composable, decisions traceable and change safer.

This repository implements one bounded part of that vision: an agentic execution harness for product and process change. It is evidence of the direction, not a claim that the complete Banking OS already exists.

## What a Banking OS is

A Banking OS is the bank-owned control and interoperability layer through which people, deterministic services, AI agents and existing platforms cooperate.

It provides common contracts for:

- cases, tasks, state and long-running processes;
- policy decisions, obligations and human authority;
- knowledge retrieval with source and version lineage;
- model and agent execution within explicit boundaries;
- guarded access to business capabilities;
- events, evaluations, traces and audit evidence.

It does not replace the core ledger, payment rails, CRM, data warehouse or other authoritative platforms. Those systems retain ownership of records and transactions. The Banking OS coordinates work across them and controls how intelligent automation participates.

## The manifesto

### 1. Change should be assembled, not rebuilt

Banking processes should be composed from versioned capabilities, policies, agents, human tasks and adapters. A new workflow should reuse trusted building blocks rather than create another isolated application or integration chain.

### 2. The bank should own the control plane

Vendors, models and frameworks will change. The bank must retain ownership of process definitions, policy boundaries, canonical contracts, evidence and routing decisions. Technology providers plug into the operating layer; they do not become the operating layer.

### 3. Agentic does not mean autonomous

Agents are valuable where work requires interpretation, retrieval, synthesis and planning. They should operate within bounded loops, typed contracts, approved tools and measurable quality gates. Authority remains deterministic or human wherever an action is consequential.

### 4. Interoperability is an architectural requirement

Every capability should be reachable through stable, well-defined interfaces. Open protocols and canonical schemas should isolate processes from vendor-specific APIs. Adapters absorb platform differences so that business workflows do not.

### 5. Models are replaceable resources

No process should depend on one model provider's identity or prompt format. Models should be selected by policy according to task, data classification, quality, cost, latency, residency and availability. A model can be upgraded, routed locally or replaced without redesigning the process.

### 6. Governance belongs in the execution path

Governance is not a review document attached after delivery. Identity, authorization, segregation of duties, data obligations, evaluation thresholds, approvals and evidence capture must shape every consequential transition as it happens.

### 7. Evidence is a first-class output

A completed task is insufficient. The platform must preserve what was requested, which sources and versions were used, which policies applied, which model and tools participated, what evaluations passed, who approved the outcome and what authoritative system committed the action.

### 8. Resilience includes intelligent degradation

Bank operations cannot depend on a single model, agent or external service. Processes need timeouts, idempotency, retries, circuit breakers, checkpoint recovery and alternative routes. When intelligence is unavailable or uncertain, the system should fail closed, reduce automation or hand work to a person without losing case state.

### 9. Evolution must be continuous and reversible

Processes, prompts, policies, models and adapters should be independently versioned and evaluated. Releases should support simulation, shadow execution, canaries and rollback. The platform learns from evidence without silently changing the rules governing live work.

### 10. Human expertise remains part of the architecture

The Banking OS should amplify institutional knowledge, not obscure accountability. It routes the right evidence and recommendations to the right decision-maker, preserves explicit authority and makes escalation a designed outcome rather than a failure.

## The flexibility this creates

With these foundations, the bank can change one layer without destabilizing the others:

| Change | What remains stable |
|---|---|
| Replace or add an LLM | Process contract, policy and evidence model |
| Move a workload between local and cloud inference | Agent behavior contract and consuming workflow |
| Replace a workflow or core-system vendor | Canonical capability interface and process intent |
| Add a regulatory obligation | Shared policy enforcement and affected process packages |
| Introduce a new channel | Case, identity, process and capability services |
| Improve an agent | Human authority, deterministic gates and rollback path |

Flexibility here does not mean fewer controls. It means changing faster because controls and interfaces are reusable, visible and testable.

## A practical adoption path

The Banking OS should grow through bounded, measurable vertical slices:

1. Select an internal process with clear ownership, evidence and approval boundaries.
2. Preserve the current case and decision model before introducing AI.
3. Expose only the minimum guarded capabilities required by the process.
4. Add bounded agents where interpretation or synthesis creates demonstrable value.
5. Evaluate quality, control effectiveness, latency, cost and human outcomes.
6. Promote reusable contracts into shared platform capabilities.
7. Expand only when operational evidence supports the next scope.

The product and process change workflow in this repository follows that approach. It demonstrates orchestration, bounded parallel agents, evaluation gates, checkpointed human approval and evidence capture while deliberately stopping short of real banking-system mutation.

## The promise

A Banking OS gives a bank a stable way to evolve in an unstable technology landscape. It makes intelligent automation adoptable without making the institution dependent on a single model, vendor or monolithic transformation. It turns governance into executable infrastructure, integration into reusable capability and change into a controlled, observable discipline.

The goal is not autonomy at any cost. The goal is a bank that can adapt continuously while remaining accountable, resilient and in control.
