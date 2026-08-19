# Product & Process Change — Process Package

## Objective

Prepare governed, evidence-backed change packages for Product Support without replacing human ownership, departmental review or authoritative record systems.

The implemented path is `CHANGE_TO_EXISTING / PROCESS`.

## Required input

- Request title, owner, purpose and requested change
- Existing authoritative item identifier
- Risk, Legal and Information Security evidence references
- Related department evidence reference
- AML evidence when declared applicable

## Node contracts

| Node | Type | Output | Control |
|---|---|---|---|
| Register | System | Case and evidence event | Preserve before AI |
| Classify | Agent-ready | Request/subject class | Typed enum |
| Validate | Deterministic | Missing evidence list | Stop on incomplete |
| Retrieve | Knowledge | Versioned sources | Approved corpus only |
| Impacts | Bounded agents | Cited domain findings | Three named domains |
| Evaluate | Deterministic | Mandatory eval results | Every gate must pass |
| Review | Human | Approval or rejection | Durable interrupt |
| Controlled action | System | Simulated proposal | No external write |

Inside an agent node the permitted loop is `plan → retrieve → analyze → cite → evaluate → stop/retry/escalate`. The intended maximum is three iterations, approved read tools only, required citations and no system-of-record mutation.

Product Support sees findings and eval results. Approval resumes the exact checkpoint; rejection ends the path. Side effects are placed after approval because interrupt nodes restart from the beginning on resume.

Version `0.1.0` is approved for simulation only. Production requires enterprise identity, policy service, evidence ledger, durable case service, authorized adapters, resilience and independent review.
