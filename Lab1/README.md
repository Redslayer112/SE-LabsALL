# SE Lab 1: Requirements Engineering & UML Use-Case Modelling

**Problem Statement #19 | Healthcare & Telemedicine**
**System:** Personalized Meal & Diet Subscription Manager
PES University, Dept. of CSE

A clinical dietary subscription service that generates weekly menus from patient metabolic
constraints (allergies, diabetic limits, calorie goals) and tracks daily delivery fulfilment.

## Deliverables

| # | Deliverable | Format asked for | Submitted file | Source |
|---|---|---|---|---|
| 1 | Requirements Table (5 FRs + 2 NFRs) | Word/Excel | [`exports/requirements-table.docx`](exports/requirements-table.docx) (+ [PDF](exports/requirements-table.pdf)) | [`requirements-table.md`](requirements-table.md) |
| 2 | UML Use-Case Diagram | PDF | [`exports/use-case-diagram.pdf`](exports/use-case-diagram.pdf) | [`use-case-diagram.drawio`](use-case-diagram.drawio) |
| 3 | Use-Case Flow Specification (1 page) | Word (PDF per step 7) | [`exports/use-case-flow.docx`](exports/use-case-flow.docx) (+ [PDF](exports/use-case-flow.pdf)) | [`use-case-flow.md`](use-case-flow.md) |

The handout names Word/Excel for the table and Word for the flow doc, while step 7 says export
as PDF. Both formats are here, so either reading is covered.

`use-case-diagram.drawio` opens directly in draw.io (app.diagrams.net → File ▸ Open, or the desktop app).

## Model Summary

**Actors (4):** Subscriber · Dietitian · Delivery Agent · Payment Gateway «external system»

**Use Cases (7):**

| ID | Use Case | Actor | Traces to |
|---|---|---|---|
| UC-01 | Manage Health Profile | Subscriber | FR-002, NFR-002 |
| UC-02 | Generate Weekly Meal Plan | Subscriber | FR-001 |
| UC-03 | Approve Weekly Meal Plan | Dietitian | FR-003 |
| UC-04 | Modify Delivery Schedule | Subscriber | FR-004, NFR-001 |
| UC-05 | Record Delivery Fulfilment | Delivery Agent, Subscriber | FR-005 |
| UC-06 | Validate Nutritional Constraints | — («include» target) | FR-001 |
| UC-07 | Apply Skip Credit | Payment Gateway | FR-004 |

**Relationships:**
- **«include»**: UC-02 *Generate Weekly Meal Plan* → UC-06 *Validate Nutritional Constraints*.
  UC-02 validates every plan it builds, without exception. Unconditional behaviour belongs in a
  separate use case that the base one reuses, so it goes in `include`.
- **«extend»**: UC-07 *Apply Skip Credit* → UC-04 *Modify Delivery Schedule*.
  UC-04 issues a credit only when the subscriber skips a delivery, not when they pause or
  reschedule. That condition is what makes it `extend` rather than `include`.

`use-case-flow.md` specifies UC-02 in full, including what happens when nutritional validation
fails and when the dietitian rejects the draft.

## Regenerating the PDFs

Requires the draw.io desktop app (set `$DRAWIO` if it isn't auto-detected) and Chromium:

```bash
python3 scripts/build.py     # rebuilds all three PDFs into exports/
```
