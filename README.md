# NexusERP // Principal Enterprise Systems Engine

A highly secure, granular, and type-safe corporate resource allocation platform engineered on a modern Python and Django monolithic stack framework.

---

## 🛠 Mandated Development Stack

- **Framework Core**: Django 5.0+ (Structured Monolithic Namespace Architecture)
- **Dependency Pipeline**: Poetry (Deterministic builds via exact dependency tracking locking)
- **Task Automation**: Unified Makefile Lifecycle Controllers
- **Static Typings Parsing**: Mypy paired with strict `django-stubs` compliance
- **Testing Architecture**: Pytest-django with isolated parallelized testing suites
- **Asset Interception**: WhiteNoise Compressed Production Distribution Layout
- **Interface Layouts**: Tailwind CSS Core UI backed by Lucide Graphic Tokens

---

## 🚀 Rapid Initialization & Setup Protocol

### 1. Prerequisites Execution
Ensure your system hosts `Python 3.12+` and `Poetry` globally before launching the environment setup commands.

### 2. Environment Assembly
Run the standardized installation routine to build your local isolated package shell:
```bash
make install
```

### 3. Database Schema Synthesis
Generate your table blueprints and compile structural models into the local engine:
```bash
# Compile structural migration blueprints
make migrations

# Map migrations onto your local file database storage
make migrate
```

### 4. Create Master Administrative Credentials
Instantiate a system-wide root admin account to interact with your secure admin dashboard panels:
```bash
poetry run python manage.py createsuperuser
```

### 5. Launch the Development Server Node
Fire up the server layer using our standardized ASGI container setup tool:
```bash
make dev
```
Open your browser and navigate to `http://localhost:8000` to interact with the interface panels.

---

## 🛡 System Quality Controls & Automated Verification

Our build pipeline enforces strict, non-negotiable code quality gates before any module code can be merged into production or staging environments.

### Code Style Formatting Checks
To format the entire project tree automatically to match strict PEP rules, execute:
```bash
make format
```

### Static Type Checker Linting Loop
To run strict compile-time checks across all 33 source files and model properties, run:
```bash
make lint
```

### Automated Unit Test Verification
To execute our complete, multi-currency accounting calculation validation and auth test suites, run:
```bash
make test
```

---

## 📂 Structural Directory Organization

```text
enterprise_erp/
├── apps/
│   ├── core_finance/       # Phase 3: Ledger, Accounts, Invoicing & Multi-Currency APIs
│   └── iam/                # Option 1 & 2: RBAC/ABAC Engines, Auditing & User Controls
├── config/                 # Core framework control configuration kernel settings files
├── templates/              # Tailored global template workspaces styled with Tailwind
├── pyproject.toml          # Poetry package dependencies and strict Mypy compiler flags
├── pytest.ini              # Test runner configurations and nested path mapping scopes
└── Makefile                # Central automation script registry targets
```

---

## 🔒 Authorization Architecture Design Principles

The platform secures sensitive business assets using a robust **Hybrid Authorization Strategy**:
1. **RBAC Basis**: Baseline organizational privileges are tied directly to an employee's functional **Job Title**.
2. **ABAC Overrides**: Real-time attribute checking (such as geographic region tracking or sensitivity rules) intercept access requests to protect data at the object layer.
3. **Audit Trail Engine**: High-throughput request interceptor middleware logs every database mutation and security event automatically.
