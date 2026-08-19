# Evaluation Strategy

## Offline release evaluation

- Golden classification cases
- Missing and conflicting evidence
- Source retrieval and duplicate matches
- Adversarial content in attachments
- Domain impact and citation completeness
- Approval and rejection paths
- Cost and latency budgets

## In-run gates

- Mandatory evidence references present
- Risk, operations and technology findings returned
- Every finding carries an approved citation
- Change case links to a versioned source
- No controlled action before human approval

## Production signals

- Task success and human override rate
- Unsupported claim and citation failure rate
- Policy denials and forbidden-tool attempts
- Retry, timeout and escalation rates
- Cost and latency by case, node, model and provider
- Process lead time, rework and change failure rate

The backend implements `required_evidence`, `impact_coverage`, `citation_coverage` and `source_linkage`. All are mandatory. Web Eval Lab values are representative synthetic data, not production measurements.
