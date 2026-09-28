# Architecture

## Flow
Case intake → required-document tracking → discrepancy registry → verification state → risk gate → ACT / ASK / VERIFY / ESCALATE → evidence packet.

## Invariants
1. Missing required documents must trigger ASK.
2. Unverified complete cases must not ACT.
3. High-risk discrepancies must escalate.

## Boundary
Adapters for OCR, government systems, sensors, databases or LLMs must preserve provenance and explicit failure states.
