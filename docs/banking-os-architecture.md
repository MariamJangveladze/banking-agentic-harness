# Banking OS Architecture

## Target-state view

The Banking OS is a bank-owned coordination layer between approved experiences and authoritative enterprise systems. It separates business processes from specific channels, models, agent frameworks and system vendors while keeping policy, human authority and evidence in the execution path.

![Banking OS target-state architecture](assets/banking-os-architecture.svg)

The rendered overview follows the visual language of the repository's System Map. The Mermaid source below preserves an editable, text-native representation of the same architectural intent.

```mermaid
flowchart TB
    subgraph EXP["Experience & Participation"]
        EMP[Employee workbenches]
        API[APIs and approved channels]
        HUMAN[Human tasks and decisions]
    end

    subgraph BOS["Banking OS — bank-owned control and coordination layer"]
        direction TB

        subgraph CTRL["Control Plane"]
            ID[Identity and delegated authority]
            CASE[Case and task services]
            REG[Process and capability registry]
            POLICY[Policy decisions and obligations]
        end

        subgraph EXEC["Composable Execution"]
            PROC[Versioned process packages]
            ORCH[Durable orchestration and checkpoints]
            AGENTS[Bounded domain agents]
            RULES[Deterministic rules and quality gates]
        end

        subgraph INTEL["Intelligence Fabric"]
            ROUTER[Policy-aware model routing]
            MODELS[Local and hosted models]
            KNOW[Governed knowledge and retrieval]
            EVAL[Evaluation and safety services]
        end

        subgraph CAP["Interoperability & Capability Fabric"]
            CONTRACTS[Canonical typed contracts]
            TOOLS[Guarded tools and capability APIs]
            ADAPTERS[Vendor and system adapters]
            EVENTS[Events and integration backbone]
        end

        subgraph TRUST["Evidence, Governance & Resilience — cross-cutting"]
            LEDGER[Immutable decision and evidence ledger]
            OBS[Traces, metrics, cost and lineage]
            RES[Retries, idempotency, fallback and recovery]
            OPS[Release controls, kill switch and incident response]
        end
    end

    subgraph BANK["Authoritative Bank & Enterprise Ecosystem"]
        CORE[Core banking and ledgers]
        PAY[Payments and transaction platforms]
        CRM[CRM, onboarding and servicing]
        DATA[Data, documents and knowledge systems]
        RISK[Risk, compliance and security services]
        EXT[Partners and regulated external services]
    end

    EXP --> CTRL
    HUMAN <--> ORCH
    CTRL --> EXEC
    EXEC <--> INTEL
    EXEC --> CAP
    CTRL --> CAP
    CAP <--> BANK

    CTRL -. governed by .-> TRUST
    EXEC -. evidenced by .-> TRUST
    INTEL -. evaluated by .-> TRUST
    CAP -. observed by .-> TRUST
```

## Architectural boundaries

| Layer | Responsibility | Key boundary |
|---|---|---|
| Experience and participation | Workbenches, APIs, channels and human decisions | A channel does not grant business authority |
| Control plane | Identity context, cases, registry, policies and obligations | Models do not decide permissions |
| Composable execution | Versioned workflows, durable state, agents and deterministic gates | Agents propose; controlled services authorize transitions |
| Intelligence fabric | Model routing, retrieval, evaluation and safety | Processes depend on contracts, not a specific model |
| Capability fabric | Canonical interfaces, guarded tools, adapters and events | Systems of record remain authoritative |
| Evidence, governance and resilience | Audit lineage, observability, recovery and operational control | Evidence is separate from transient agent memory |

## How a governed request flows

```mermaid
sequenceDiagram
    actor User as Employee or approved channel
    participant Control as Control plane
    participant Process as Process package
    participant Intel as Intelligence fabric
    participant Human as Authorized reviewer
    participant Capability as Guarded capability
    participant Record as System of record
    participant Evidence as Evidence ledger

    User->>Control: Submit request and identity context
    Control->>Evidence: Preserve request and policy context
    Control->>Process: Start versioned process
    Process->>Intel: Retrieve, interpret or propose
    Intel-->>Process: Typed output, citations and evaluation results
    Process->>Human: Present evidence-backed decision task
    Human-->>Process: Approve, reject or request changes
    Process->>Capability: Request authorized action
    Capability->>Control: Re-check policy and obligations
    Capability->>Record: Commit through idempotent adapter
    Record-->>Capability: Authoritative result
    Capability->>Evidence: Record decision, action and lineage
    Process-->>User: Return outcome and status
```

Not every process requires an agent or human approval. The process contract determines which steps apply. Consequential actions always pass through deterministic authorization and guarded capability boundaries.

## Composability and independence

The architecture avoids coupling along four axes:

- **Process independence:** workflows consume canonical capabilities rather than vendor-specific endpoints.
- **Model independence:** a routing policy selects models by classification, quality, residency, cost, latency and availability.
- **Framework independence:** agent runtimes implement typed task and tool contracts; orchestration state does not depend on hidden model memory.
- **Channel independence:** experiences enter through shared identity, case and process services instead of recreating business logic.

Open protocols such as event standards, OAuth/OIDC, OpenAPI and appropriate agent/tool protocols can support these seams. Protocol adoption does not replace bank-owned authorization, schemas, policy enforcement or evidence.

## Agentic execution model

Agents are bounded workers inside a governed process, not owners of the process. Each agent receives:

- a narrow objective and typed input/output contract;
- an approved knowledge scope and explicit source lineage;
- least-privilege tools with read/write distinctions;
- iteration, time, token and cost budgets;
- mandatory evaluation, stop and escalation conditions;
- a traceable model, prompt, tool and configuration version.

The preferred control rule is:

> Probabilistic components interpret, retrieve, prepare and propose. Deterministic services and authorized people control, approve, persist and commit.

## Resilience model

Banking OS resilience is designed at process level, not delegated to an LLM provider:

- durable checkpoints separate recovery state from the authoritative case and evidence ledgers;
- idempotency keys and transactional outbox/inbox patterns prevent duplicate side effects;
- timeouts, bounded retries and circuit breakers isolate failing dependencies;
- model routes support approved fallback, reduced-capability mode and human handoff;
- queues absorb temporary outages and preserve ordered work where required;
- kill switches can disable a model, tool, adapter, process version or automation class;
- replay, simulation and disaster-recovery tests verify that evidence and state remain reconstructable.

## Governance and evolution

Processes, policies, prompts, agent configurations, evaluations, models and adapters are independently versioned. Promotion to a broader scope should require evidence from offline tests, simulation or replay, shadow execution and controlled rollout. Runtime telemetry informs changes, but no production component silently self-modifies its governing policy or release version.

This creates a controlled evolution loop:

```text
Observe → evaluate → propose change → independently review → simulate
        → release gradually → monitor → retain or roll back
```

## How this repository maps to the target state

| Target-state capability | Evidence in this repository | Status |
|---|---|---|
| Operational experience | React control plane and synthetic run explorer | Implemented demo |
| Versioned process package | Product/process change manifest and specification | Implemented vertical slice |
| Durable orchestration | LangGraph graph, interrupt/resume and checkpoint seam | Implemented; production seam documented |
| Bounded agents | Parallel risk, operations and technology analysis | Implemented |
| Evaluation gates | Evidence, domain, citation and linkage checks | Implemented |
| Governed intelligence | Deterministic default; optional Ollama and Chroma | Partial/local |
| Policy-aware enterprise routing | Model gateway seam | Target state |
| Guarded enterprise capabilities | Interface and simulated proposal only | Target state |
| Enterprise identity and authorization | Boundary documented, not integrated | Target state |
| Authoritative case/evidence ledger | Events represented in state; separate ledger required | Target state |

The distinction is deliberate: the repository proves architectural mechanisms without claiming production authority, access to real bank data or the ability to mutate banking systems.
