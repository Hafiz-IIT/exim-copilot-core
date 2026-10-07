# EXIM Copilot Core

<p align="center">
  <strong>Governed Workflow Core for AI-Assisted Trade Operations</strong><br/>
  <sub>Documents → discrepancies → verification → evidence → authorized action.</sub>
</p>

<p align="center">
  <a href="https://github.com/Hafiz-IIT/exim-copilot-core/actions"><img src="https://img.shields.io/github/actions/workflow/status/Hafiz-IIT/exim-copilot-core/ci.yml?label=CI" alt="CI"/></a>
  <img src="https://img.shields.io/badge/status-reproducible%20prototype-blue" alt="Prototype"/>
  <img src="https://img.shields.io/badge/domain-export--import-orange" alt="EXIM"/>
</p>

## The problem

Trade workflows contain many points where an AI assistant could move too quickly from **extracted information → operational action**.

This core deliberately inserts governance states:

```
Case intake
   ↓
Required documents
   ↓
Discrepancies
   ↓
Verification
   ↓
Risk / permission gate
   ↓
ACT · ASK · VERIFY · ESCALATE
```

## Try it

```bash
python exim_copilot_core.py
python -m unittest discover -s tests -v
```

The second-stage `role_policy.py` layer separates authority for traders, brokers, freight/logistics operators and reviewers.

## Implemented

- case state model
- required-document tracking
- discrepancy registry
- verification state
- role-based permissions
- explicit action states
- audit events
- deterministic tests + CI

## Engineering principle

**Workflow authority is explicit.** A user who can upload evidence is not automatically authorized to verify it.

## Relationship to the larger EXIM Copilot

This repository is the **governance/core layer**, not the full commercial product vision. OCR, customs integrations, HS/RITC assistance, shipment intelligence, physical scanning and enterprise workflows remain separate research/product layers unless explicitly implemented elsewhere.

## Research boundary

Prototype only. No claim of customs-law automation, regulatory approval, production deployment or integration with ICEGATE/DGFT.

Related work: [EXIM Document Truth Bench](https://github.com/Hafiz-IIT/exim-document-truth-bench) · [Secure Document RAG Agent](https://github.com/Hafiz-IIT/secure-doc-rag-agent) · [Cargo Scan Consistency Lab](https://github.com/Hafiz-IIT/cargo-scan-consistency-lab)
