# Evaluation Protocol

## Question
Can explicit workflow state and evidence gates reduce unsafe automation in document-heavy EXIM operations?

## Metrics
- Correct governance outcome
- Missing-document recovery
- Discrepancy escalation
- Unsafe ACT rate
- Audit completeness

## Falsification
- A high-risk discrepancy returns ACT.
- A required-document gap is ignored.
- An unverified case is treated as verified.

Run:
```bash
python -m unittest discover -s tests -v
```
