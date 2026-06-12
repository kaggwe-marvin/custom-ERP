# CustomERP

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![Django](https://img.shields.io/badge/Django-6.x-green)
![DRF](https://img.shields.io/badge/DRF-3.17+-red)
![Poetry](https://img.shields.io/badge/Poetry-Dependency%20Management-blueviolet)
![Mypy](https://img.shields.io/badge/Type_Checked-Mypy-success)
![Pytest](https://img.shields.io/badge/Tested-Pytest-yellow)
![License](https://img.shields.io/badge/License-TBD-lightgrey)

A secure, type-safe, and modular Enterprise Resource Planning (ERP) platform built on Django. CustomERP is designed using a modular monolithic architecture that enables rapid development while maintaining clear domain boundaries, strong typing, and enterprise-grade security practices.

---

## Overview

CustomERP provides a foundation for building business-critical applications such as:

* Financial Management
* Identity & Access Management
* Organizational Administration
* Resource Allocation
* Auditing & Compliance
* Business Process Automation

The platform emphasizes:

* Strong static typing
* Domain-driven modularization
* Maintainable architecture
* Secure access controls
* Automated testing
* Reproducible deployments

---

## Key Features

### Core Platform

* Django 6.x
* Django REST Framework
* ASGI-first deployment with Daphne
* WhiteNoise static asset delivery
* Environment-based configuration

### Engineering Standards

* Poetry dependency management
* Mypy static type checking
* django-stubs integration
* pytest testing framework
* Automated development workflows

### Security Foundation

* Authentication and authorization framework
* Role-based access control foundations
* Audit logging support
* Environment-based secrets management

---

## Technology Stack

| Layer                 | Technology             |
| --------------------- | ---------------------- |
| Backend Framework     | Django 6.x             |
| API Framework         | Django REST Framework  |
| ASGI Server           | Daphne                 |
| Dependency Management | Poetry                 |
| Type Checking         | Mypy + django-stubs    |
| Testing               | pytest + pytest-django |
| Static Assets         | WhiteNoise             |
| Environment Variables | python-dotenv          |
| Frontend Styling      | Tailwind CSS           |
| Icons                 | Lucide                 |
| Automation            | Makefile               |

---

## Architecture

CustomERP follows a **Modular Monolith Architecture**.

```text
┌─────────────────────────────────────┐
│             CustomERP               │
├─────────────────────────────────────┤
│                                     │
│  IAM Module                         │
│  Finance Module                     │
│  Future Business Modules            │
│                                     │
├─────────────────────────────────────┤
│         Shared Django Core          │
├─────────────────────────────────────┤
│         PostgreSQL / SQLite         │
└─────────────────────────────────────┘
```

### Benefits

* Simple deployment model
* Strong module boundaries
* Reduced operational complexity
* Easier refactoring
* Shared infrastructure and tooling

---

## Project Structure

```text
enterprise_erp/
├── apps/
│   ├── core_finance/
│   └── iam/
│
├── config/
│   ├── settings/
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
│
├── pyproject.toml
├── pytest.ini
├── Makefile
└── manage.py
```

---

## Requirements

* Python 3.12+
* Poetry 2.x+

Verify installation:

```bash
python --version
poetry --version
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd enterprise_erp
```

Install dependencies:

```bash
poetry install
```

Activate the virtual environment:

```bash
poetry shell
```

---

## Environment Configuration

Create a `.env` file:

```env
DEBUG=True

SECRET_KEY=your-secret-key

ALLOWED_HOSTS=localhost,127.0.0.1
```

Configure additional environment variables as needed for deployment.

---

## Database Setup

Apply migrations:

```bash
make migrate
```

Or:

```bash
poetry run python manage.py migrate
```

Create an administrator account:

```bash
poetry run python manage.py createsuperuser
```

---

## Running the Application

Start the ASGI server:

```bash
make dev
```

Equivalent:

```bash
poetry run daphne config.asgi:application
```

Application URL:

```text
http://localhost:8000
```

---

## Development Workflow

### Format Code

```bash
make format
```

### Static Type Checking

```bash
make lint
```

### Run Test Suite

```bash
make test
```

### Clean Cache Files

```bash
make clean
```

### Execute Full Validation Pipeline

```bash
make pipeline
```

Pipeline stages:

```text
Migration Validation
↓
Code Formatting
↓
Type Checking
↓
Test Execution
```

---

## Dependency Overview

### Production Dependencies

* Django
* Django REST Framework
* django-filter
* Daphne
* WhiteNoise
* python-dotenv
* Twisted
* Markdown

### Development Dependencies

* Black
* Mypy
* django-stubs
* pytest
* pytest-django

---

## Type Safety

CustomERP adopts a strict typing strategy:

* Mypy validation
* django-stubs integration
* djangorestframework-stubs integration
* Type-annotated services
* Type-annotated models
* Type-annotated APIs

Benefits include:

* Earlier bug detection
* Improved IDE support
* Safer refactoring
* Better documentation through types

---

## Current Modules

### IAM

Identity and Access Management.

Planned capabilities:

* Authentication
* Authorization
* Role Management
* Permission Policies
* Audit Events

### Core Finance

Financial domain services.

Planned capabilities:

* Chart of Accounts
* General Ledger
* Journal Entries
* Invoicing
* Financial Reports

---

## Roadmap

### Phase 1

* IAM Foundation
* Authentication
* Authorization
* Audit Logging

### Phase 2

* Financial Core
* Chart of Accounts
* Journal Entries
* Ledger Operations

### Phase 3

* Invoicing
* Reporting
* Dashboard Analytics

### Phase 4

* Procurement
* Inventory
* Human Resources

---

## Contributing

1. Create a feature branch.
2. Implement changes.
3. Run the validation pipeline.

```bash
make pipeline
```

4. Submit a pull request.

---

## License

Specify the project license.

Examples:

* MIT
* Apache 2.0
* Proprietary / Internal Use Only

---

## Design Principles

* Security First
* Type Safety by Default
* Modular Architecture
* Explicit Dependencies
* Automated Quality Gates
* Maintainable Domain Boundaries
