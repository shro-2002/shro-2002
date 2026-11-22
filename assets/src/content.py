"""Profile copy for the artwork. Every figure here is checked against its repository."""

NAME = "Shroddha Ghosh"
ROLE = "Software Engineer · AI Systems & Agentic Applications"
TAGLINE = ("Building reliable AI systems that use tools,", "enforce policies, and verify outcomes.")
META = "GE VERNOVA  ·  BENGALURU  ·  B.TECH CSE 2024"

STAGES = [
    ("PROPOSE", "the model plans"),
    ("ENFORCE", "policy in code"),
    ("AUTHORIZE", "above risk limits"),
    ("VERIFY", "at the source"),
]

# accent: key into the theme palette. metrics: (value, label lines).
PROJECTS = [
    {
        "slug": "payops", "num": "01", "name": "PayOps Sentinel", "accent": "amber",
        "category": "PAYMENTS · INCIDENT INVESTIGATION", "status": "SANDBOX",
        "pitch": "Disproves its own explanations before money moves",
        "pitch_lines": ("Investigates refund spikes and tries to", "disprove its own explanations first."),
        "hero_evidence": "False attribution 26.9% → 2.8%",
        "shot": "projects/payops-investigation.jpg",
        "metrics": [
            ("26.9% → 2.8%", ("false attributions,", "360 held-out runs")),
            ("84 / 84", ("numeric claims matched", "their source query")),
            ("16 / 16", ("safety cases passed;", "158 backend tests")),
        ],
        "stack": ("Python · FastAPI · PostgreSQL", "Claude · Next.js · PayPal sandbox"),
    },
    {
        "slug": "agentdoor", "num": "02", "name": "AgentDoor", "accent": "cyan",
        "category": "AGENT COMMERCE · MCP", "status": "LIVE DEMO",
        "pitch": "Owner-approved rules, served to people and AI agents",
        "pitch_lines": ("Owner-approved rules, served to people", "and AI shopping agents over MCP."),
        "hero_evidence": "Live MCP endpoint · signed quotes",
        "shot": "projects/agentdoor-rehearsal.jpg",
        "metrics": [
            ("Live", ("agentdoor.shop, MCP over", "Streamable HTTP, 3 tools")),
            ("Ed25519", ("quotes signed and bound", "to the approved policy")),
            ("0 oversold", ("in a simulated rush of", "50 customers")),
        ],
        "stack": ("TypeScript · Express · Zod · MySQL", "MCP SDK · Claude · fast-check"),
    },
    {
        "slug": "disputedesk", "num": "03", "name": "DisputeDesk", "accent": "green",
        "category": "MULTI-AGENT · CHARGEBACKS", "status": "PROTOTYPE",
        "pitch": "Agents draft, code decides, a person signs large ones",
        "pitch_lines": ("Agents draft, code decides, and a", "person signs the large ones."),
        "hero_evidence": "99 approval-gate attack tests",
        "shot": "projects/disputedesk-approval.jpg",
        "metrics": [
            ("349 tests", ("99 of them attacks on", "the approval gate")),
            ("$500", ("auto-file limit; above it", "the FinOps lead signs")),
            ("HMAC chain", ("audit chain checked before", "every money call")),
        ],
        "stack": ("Python · FastAPI · SQLite", "Claude · Switch (Mattermost)"),
    },
]

# False-accept share on dev-A with the registered seeds (rewardshield/RESULTS.md).
REWARD_BARS = [
    ("AgentTune 1.1.5", "1 db", 4.31),
    ("single-1", "1 db", 3.88),
    ("random-4", "4 db", 3.13),
    ("targeted-4", "4 db", 1.39),
    ("random-16", "16 db", 1.00),
]
REWARD_FACTS = [
    ("1,360 agent trajectories, labelled by an", "independent Spider test-suite oracle"),
    ("Better-filtered fine-tuning data: no", "measurable change (−1.06 pts, CI spans 0)"),
    ("Upstream: my fix merged in AgentTune #22;", "root-cause fix shipped in agenttune 1.1.7"),
]
REWARD_NOTE = ("Registered seeds. Averaged over 200 database draws, targeted-4 beats",
               "random-4 by 0.25 pts on dev-A and 1.57 pts on held-out schemas.")
