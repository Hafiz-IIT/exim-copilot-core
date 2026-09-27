# EXIM Copilot Core

A small, inspectable workflow core for an AI-assisted export-import operations system.

This repository focuses on orchestration rather than pretending to contain production OCR, customs-system integrations, or a finished commercial platform.

## Implemented
- case state machine
- required-document tracking
- discrepancy recording
- verification state
- human-escalation gate
- auditable event history
- action recommendation: ACT / ASK / VERIFY / ESCALATE

## Run
```bash
python -m unittest discover -s tests -v
python exim_copilot_core.py
```

## Design principle
Automation should not jump directly from extracted text to consequential action. The workflow makes missing evidence, discrepancies, verification and escalation explicit states.
