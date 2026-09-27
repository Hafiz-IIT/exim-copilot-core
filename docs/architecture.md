# Architecture

```mermaid
flowchart LR
    A0[case intake] --> A1
    A1[document requirements] --> A2
    A2[discrepancy checks] --> A3
    A3[verification] --> A4
    A4[risk gate] --> A5
    A5[recommendation] --> A6
    A6[evidence packet]
```

## Case state
Stores required documents, received evidence, discrepancies, verification status, risk, and audit events.

## Recommendation gate
Prioritizes high-risk conflict escalation, missing-evidence requests, verification, and only then ACT.

## Evidence packet
Produces a structured snapshot suitable for a human reviewer or downstream UI.

## Principle
Operational workflow should expose uncertainty and missing evidence as first-class states instead of hiding them behind an AI answer.
