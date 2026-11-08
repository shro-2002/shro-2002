# Shroddha Ghosh

**Software engineer · Reliable AI agents for payments and other high-stakes workflows**

I'm a software engineer with professional experience in Python, SQL, analytics and backend engineering. I specialize in end-to-end AI engineering: agents that call real tools, measured against frozen evaluations, and allowed to act only within limits enforced in code.

The rule behind my recent work: **the model proposes, deterministic code decides, a human approves what matters.**

## Core capabilities

- **Agent systems:** tool calling, multi-agent workflows, Model Context Protocol servers, permission boundaries
- **Money-safe execution:** policy engines, idempotency, database constraints, read-back verification
- **Evaluation:** frozen and held-out test sets, prompt-injection cases, provider comparisons, results reported as counts
- **Security and audit:** threat models, approval bound to an exact action, tamper-evident logs
- **Backend and data:** Python, FastAPI, PostgreSQL, SQLite, SQL, TypeScript, Next.js, PyTorch

## Featured: fintech agents

### [PayOps Sentinel](https://github.com/shro-2002/payops-sentinel)

**Payment-incident investigator with verified claims** · PayPal AI Hackathon 2026

Explains refund spikes for payment-ops teams. The agent has read-only, argument-validated tools; the server checks every number it states against the query it cites. Refunds pass 16 deterministic policy checks and a second-operator approval bound to a SHA-256 hash of the action. They are then executed with a stable request ID and verified against PayPal.

- 84/84 numeric claims matched source; 16/16 safety cases passed. [Evaluation](https://github.com/shro-2002/payops-sentinel/blob/main/docs/EVALUATION.md) · [Security model](https://github.com/shro-2002/payops-sentinel/blob/main/docs/SECURITY_MODEL.md)
- `FastAPI` `PostgreSQL` `Next.js` `AG Grid` `Claude` · CI on main · PayPal sandbox

### [DisputeDesk](https://github.com/shro-2002/disputedesk)

**Multi-agent chargeback defense** · Flip the Switch · Hackathon Submission

Three agents and a finance team defend card-not-present fraud disputes (Visa 10.4). Visa CE3.0 evidence rules run in code and the model only drafts letters. Small, provable cases file automatically; large ones wait for an identity-checked approver. An HMAC-SHA256 audit chain is verified before every money call. Receipts are unique per dispute and approval, so replays fail.

- [Demo video (2:43)](https://youtu.be/A_EF8L1ivME) · [Claim audit](https://github.com/shro-2002/disputedesk/blob/main/docs/README_CLAIM_AUDIT.md)
- `Python` `Switch` `FastAPI` `SQLite` `Claude` · mock gateway, synthetic data

### [countersign](https://github.com/shro-2002/countersign)

**Agent refunds limited to the merchant's mandate** · Early prototype

An agent tricked into requesting a $1.00 refund against a $0.25 mandate is blocked. The merchant approves the safe correction, which executes exactly once and is re-verified with PayPal.

- Frozen 8-case evaluation: 2/8 safety violations unprotected, **0/8** with countersign. [Results](https://github.com/shro-2002/countersign/blob/main/evals/FROZEN_RESULTS_2026-10-16.md) · [Threat model](https://github.com/shro-2002/countersign/blob/main/docs/THREAT_MODEL.md)
- `FastAPI` `PostgreSQL` `Gemini` · PayPal sandbox

### [AuditGlimmer](https://github.com/shro-2002/auditglimmer)

**Inspection photos to traceable lending-collateral evidence** · Built for Meta Global AI Developer Hackathon 2026

SAM 3.1 and Muse Spark read equipment serials. Deterministic rules match them to the asset register and route uncertainty to a reviewer.

- Pre-registered study: 11/16 exact serials (69%, below its own 70% bar), 0 invented. [Results](https://github.com/shro-2002/auditglimmer/blob/master/docs/muse-study-results.md) · [Demo (2:55)](https://youtu.be/xvGoop1LOUE)

## Additional work

- [Action Graph AI](https://github.com/shro-2002/action-graph-ai): meeting-to-execution agent with a held-out Claude vs Muse Spark comparison
- [KinSync](https://github.com/shro-2002/KinSync): MCP server whose agent permission boundary is tested against a compromised planner · built for the [Amazon Developer Hackathon 2026](https://amazonappdev2026.devpost.com/)
- [Territory](https://github.com/shro-2002/territory): localization planning on the Qloo API · [live demo](https://territory-qloo.netlify.app)
- [Metric Mirage](https://github.com/shro-2002/metric-mirage): detects Simpson's paradox in reported rates · [live demo](https://shro-2002.github.io/metric-mirage/)
- [RSNA knee MRI](https://github.com/shro-2002/rsna-knee-abnormality-detection): solo Kaggle entry with DICOM pipeline and DINOv2 fine-tunes

## How I build

I use AI coding assistants for much of the implementation, and commit history records where. My role is scoping the problem, designing the architecture and controls, directing and reviewing the code, defining tests and evaluations, and deciding what ships. ADRs, decision logs and evaluation reports in these repositories document many of those choices. All payment work runs on sandboxes or mocks; none is a production deployment.

## Contact

[LinkedIn](https://www.linkedin.com/in/shroddha-ghosh-90b332232/) · [All repositories](https://github.com/shro-2002?tab=repositories)
