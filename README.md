# Project Architecture — Django Inventory Tracker

---

## 1. System Overview

A Django monolith with three domain apps:

- **inventory** — product stock tracking and CSV export
- **bookmarks** — reference links with tags
- **api** — REST endpoint for bookmarks with token authentication and request throttling

---

## 2. Main Components

| Module | Responsibility |
|---|---|
| `config/` | Global settings, root URLs, middleware wiring, app registration |
| `inventory/` | `Product` model, low-stock signal, CSV report view, sales simulation management command |
| `bookmarks/` | `Bookmark` and `Tag` models, form logic for comma-separated tag creation, list/create views |
| `api/` | DRF `ListAPIView` for bookmarks, serializer, URL routing, custom throttle middleware integration |
| `templates/` | Unified dashboard UI combining bookmarks and inventory with SKU filtering and pagination |

---

## 3. Request Flow

```
User Request
     │
     ▼
/ (root)
     │
     ▼
UnifiedDashboardView
     │
     ▼
Session Guard ── missing is_authenticated_operator ──► /login/
     │
     ▼ (authenticated)
Dashboard fetches:
  ├── Latest bookmarks (prefetch tags)
  └── Inventory list (SKU filter + pagination)

/api/* requests
     │
     ▼
IP-based Throttle Middleware (60 req/min)
     │
     ▼
Token Validation (Authorization: Bearer <token>)
     │
     ▼
DRF Serialization Response
```

---

## 4. Data Layer

**Bookmark ↔ Tag** — many-to-many relationship

**Product** — stock quantity, SKU identifier, low-stock threshold

**Signals** — `post_save` on `Product` emits low-stock alerts when stock falls below threshold

---

## 5. Security and Access

| Layer | Mechanism |
|---|---|
| Dashboard | Session-based operator login |
| API endpoint | Token-based header check (`Authorization: Bearer`) |
| Rate limiting | Middleware enforces 60 requests/minute per IP |

---

## 6. Operational Tooling

| Task | Command |
|---|---|
| Run server | `make run` or `make dev` |
| Apply migrations | `make migrate` |
| Format code | `make format` |
| Type checks | `make view-types` |
| Run tests | `make test` |
| Full CI pipeline | `make pipeline` |