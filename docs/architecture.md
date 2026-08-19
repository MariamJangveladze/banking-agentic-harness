# Architecture

The harness sits between employee-facing operational channels and authoritative bank systems. It owns orchestration and evidence, while existing systems retain business authority and final persistence.

## Planes

| Plane | Owns | Does not own |
|---|---|---|
| Experience | Workbench, API and human tasks | Business authorization |
| Control | Routing, process registry, policies and obligations | LLM reasoning |
| Runtime | LangGraph state, nodes, branches, checkpoints and interrupts | Authoritative case ledger |
| Intelligence | Models, retrieval, prompts and bounded agents | Permission decisions |
| Integration | Typed guarded capabilities and adapters | Unrestricted system access |
| Evidence | Events, evals, traces, cost/error attribution | Informal chain-of-thought |

## Runtime sequence

```text
Request → preserve → classify → validate → retrieve → parallel impacts
       → evaluate → interrupt → human decision → controlled proposal → close
```

The graph is deterministic at its edges. Model-backed behavior is confined to nodes with typed input/output contracts. Every consequential transition is driven by deterministic code or an authenticated human decision.

## Identifiers and persistence

- `case_id`: stable business case identifier
- `thread_id`: LangGraph checkpoint sequence
- `process_version`: immutable process-package release
- `trace_id`: observability correlation identifier
- `approval_id`: external human-decision evidence identifier
- `source_id@version`: authoritative knowledge lineage

The local demo uses `InMemorySaver`. When `LANGGRAPH_DATABASE_URL` is present, the runtime selects `PostgresSaver`. Production additionally requires a separate case/evidence ledger; checkpoints are recovery state, not the sole audit record.

## Model and knowledge routing

The default route is deterministic. Optional local mode uses Ollama chat, Ollama embeddings and persistent Chroma. A production policy-aware gateway would select local or Bedrock-hosted models based on data classification, task, budget, latency and availability.

## Failure boundaries

- Missing evidence stops before agent execution.
- Missing source linkage fails the evaluation gate.
- Evaluation failure escalates instead of committing an action.
- A rejected human decision terminates the controlled path.
- The implemented adapter creates only a simulated proposal.
