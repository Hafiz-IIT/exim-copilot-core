# EXIM Copilot Core

> Governed workflow engine for AI-assisted export-import operations: documents, discrepancies, verification, escalation and auditable action.

## Status
**Reproducible prototype** with executable Python, deterministic tests, and CI. It does not claim production deployment, regulatory approval, or real-world validation.

## Problem
Trade automation often jumps from extracted text straight to action. This core makes missing information, discrepancy handling, verification and human escalation explicit workflow states.

## Architecture
Case intake → required-document tracking → discrepancy registry → verification state → risk gate → ACT / ASK / VERIFY / ESCALATE → evidence packet.

## Quick start
```bash
python -m unittest discover -s tests -v
python exim_copilot_core.py
```

## Implemented
- Case state model
- Required-document tracking
- Discrepancy recording
- Verification state
- High-risk escalation
- Evidence packet generation
- Audit events
- Tests and CI

## Evaluation
Tests check whether incomplete, unverified, discrepant and high-risk cases produce the intended governance outcome.

## Research lineage
- *Modular AI Frameworks for Multi-Vertical Startup Innovation*
- *Human–AI Symbiosis: Toward Next-Generation Consumer Applications*
- *The Future of Digital Trust: Secure Data Interactions in User-Centric Platforms*

## Limitations
- No production workflow engine
- No customs-system credentials or APIs
- No real client data bundled
- No claim of end-to-end deployed EXIM platform

## Structure
`exim_copilot_core.py` · `tests/` · `docs/` · `ROADMAP.md` · `CITATION.cff` · CI

## License
MIT.

## Extended implementation

- `role_policy.py` — role-based permissions for trader, broker, freight/logistics actors and reviewer workflows.
- Explicit separation between document submission, discrepancy recording and verification authority.
