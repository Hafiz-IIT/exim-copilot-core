# EXIM Copilot Core

> **Evidence-aware workflow orchestration for trade documents, discrepancies, verification, and human escalation.**

The larger EXIM AI vision spans documents, compliance, logistics, scanning, alerts, and decision support. This repository deliberately extracts the smallest trustworthy workflow core: what evidence is required, what is missing, what conflicts, what has been verified, and whether a case should ACT, ASK, VERIFY, or ESCALATE.

## Implemented
- case state with required/received documents
- missing-document calculation
- discrepancy recording
- verification state
- high-risk flag
- ACT/ASK/VERIFY/ESCALATE recommendation
- auditable event history
- structured evidence packet

## Repository structure
- `exim_copilot_core.py` — core implementation
- `tests/` — deterministic tests
- `examples/` — synthetic example
- `docs/architecture.md` — design
- `docs/research-agenda.md` — experiments and paper lineage
- `STATUS.md` — claims boundary
- `CITATION.cff` — citation metadata

## Run
```bash
python -m unittest discover -s tests -v
python exim_copilot_core.py
```

## Pipeline
**case intake → document requirements → discrepancy checks → verification → risk gate → recommendation → evidence packet**

## Research lineage
Directly grounded in the long-running EXIM AI / trade-processing work: unified workflows, document validation, evidence verification, operational escalation, and the separation between extracted information and trustworthy action.

## Evaluation direction
Run synthetic case families with missing documents, benign discrepancies, high-risk conflicts, and completed verification. Compare the explicit state machine with a naive 'documents present → act' baseline.

## Maturity
**Research prototype.** This core is not an ICEGATE/DGFT integration, customs broker system, legal compliance engine, payment platform, or deployed trade product.
