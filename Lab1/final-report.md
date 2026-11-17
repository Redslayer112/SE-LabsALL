# LAB 1 SE

NAME : {{NAME}}

SRN : {{SRN}}

SECTION : {{SECTION}}

**Personalized Meal & Diet Subscription Manager (19)**

Healthcare & Telemedicine. A clinical dietary subscription service that generates weekly menus
from patient metabolic constraints (allergies, diabetic limits, calorie goals) and tracks daily
delivery fulfilment.

## 1. REQUIREMENTS TABLE :

| Req ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|---|---|---|---|---|---|
| FR-001 | Functional | The system shall generate weekly meal plans strictly adhering to user macro-nutrient constraints and allergen exclusion lists. | High | **Pass:** Generated menu contains zero excluded allergen ingredients, and each day's totals fall within the profile's calorie goal ±10% and carbohydrate ceiling. **Fail:** Peanuts included for a peanut-allergic profile. | Core value of the service; a violated constraint is a clinical safety incident, not a usability defect. |
| FR-002 | Functional | The system shall allow a Subscriber to create and update a health profile holding allergen exclusions, daily calorie goal, and diabetic carbohydrate limit. | High | **Pass:** After adding "peanut" and saving, reloading the profile lists peanut, and the next plan generated excludes it. **Fail:** A saved allergen is missing after reload, or appears in the next plan. | FR-001 cannot be evaluated without a stored, authoritative constraint set. |
| FR-003 | Functional | The system shall require a Dietitian to approve or reject each generated weekly plan, recording a reason on rejection, before the plan is released to the Subscriber. | High | **Pass:** Plan status moves Draft → Approved only after a Dietitian action; a Draft plan requested by its Subscriber returns "not yet available". A rejection with an empty reason is refused. **Fail:** Subscriber can view or order from a Draft plan. | Clinical sign-off is mandatory for a dietary service treating diabetic and allergic patients. |
| FR-004 | Functional | The system shall allow a Subscriber to pause, skip, or reschedule a scheduled delivery, and shall reject any such request submitted less than 12 hours before that delivery's dispatch time. | High | **Pass:** A skip submitted at dispatch − 12 h 01 min succeeds and the delivery disappears from the dispatch manifest; the same request at dispatch − 11 h 59 min is rejected with a cut-off message and the manifest is unchanged. **Fail:** A request inside the window alters the manifest. | Kitchen procurement is committed 12 h ahead; late changes produce food waste and mis-dispatch. |
| FR-005 | Functional | The system shall record each daily delivery's fulfilment outcome (Delivered / Failed / Not Attempted) with a timestamp captured by the Delivery Agent, and expose it to the Subscriber and Dietitian. | Medium | **Pass:** When an agent marks a delivery Delivered, the Subscriber's dashboard shows Delivered with that timestamp on next load, and the daily fulfilment report totals equal the number of scheduled deliveries. **Fail:** A dispatched delivery has no outcome after its delivery window closes. | Fulfilment tracking is half the stated problem scope and is the evidence base for billing disputes and adherence review. |
| NFR-001 | Nonfunctional (Performance & Security) | The subscription engine must support schedule modifications (pause, skip, reschedule) up to 12 hours before dispatch. | High | **Pass:** Under a simulated peak of 500 concurrent modification requests, 95th-percentile response ≤ 2 s with zero errors; every request is authenticated and carried over TLS 1.2+; no request inside the 12 h window is accepted. **Fail:** p95 > 2 s, any unauthenticated modification accepted, or any accepted request inside the cut-off. | Schedule changes are the most frequently used feature and cluster in the evening peak; they also mutate billable state, so latency and authentication are graded together. |
| NFR-002 | Nonfunctional (Security & Privacy) | The system shall store all subscriber health data (allergens, diabetic limits, clinical notes) encrypted at rest with AES-256, restrict read access to the owning Subscriber and their assigned Dietitian, and write an audit record for every access. | High | **Pass:** Direct database inspection shows no plaintext health fields; a Dietitian not assigned to a Subscriber receives HTTP 403, and that attempt appears in the audit log within 5 s. **Fail:** Any health field readable in plaintext, or any cross-account read that is served or goes unlogged. | The system holds identifiable clinical data; unauthorised disclosure is a regulatory breach, and audit records are what make the restriction provable. |

## UML USE CASE DIAGRAM :

![UML Use-Case Diagram](USE_CASE_DIAGRAM_PNG)

### ACTORS :

**Actor 1 — Subscriber**<br>
The patient who holds the dietary subscription, maintains their health profile, requests weekly
meal plans, and modifies their delivery schedule.

**Actor 2 — Dietitian**<br>
The clinician who reviews each generated weekly plan and approves or rejects it before it is
released to the Subscriber.

**Actor 3 — Delivery Agent**<br>
The courier who delivers each day's meals and records the fulfilment outcome against the schedule.

**Actor 4 — Payment Gateway** («external system»)<br>
The external payment service that issues a credit when a Subscriber skips a scheduled delivery.

### Use Cases

UC-01 — Manage Health Profile

UC-02 — Generate Weekly Meal Plan

UC-03 — Approve Weekly Meal Plan

UC-04 — Modify Delivery Schedule

UC-05 — Record Delivery Fulfilment

UC-06 — Validate Nutritional Constraints &nbsp;*(«include» from UC-02)*

UC-07 — Apply Skip Credit &nbsp;*(«extend» to UC-04)*

**Relationships**

«include» : UC-02 Generate Weekly Meal Plan → UC-06 Validate Nutritional Constraints.
UC-02 validates every plan it builds, without exception. Unconditional behaviour is factored into
a separate use case that the base one reuses, so it is modelled as «include».

«extend» : UC-07 Apply Skip Credit → UC-04 Modify Delivery Schedule.
UC-04 issues a credit only when the Subscriber skips a delivery, not when they pause or
reschedule. That condition is what makes it «extend» rather than «include».

## USE-CASE FLOW DOCUMENT :

**Use Case: UC-02 Generate Weekly Meal Plan**

Primary Actor : Subscriber &nbsp;•&nbsp; Supporting Actors : Dietitian, Nutrition Rules Engine
&nbsp;•&nbsp; Related Requirements : FR-001, FR-002, FR-003

**Preconditions :**

1. The Subscriber is authenticated and holds an active subscription.
2. A health profile exists for the Subscriber with a calorie goal, carbohydrate limit, and allergen exclusion list (FR-002).
3. No Approved plan already exists for the target week.

**Postconditions :**

1. A seven-day plan exists for the target week with status Approved.
2. Every meal in the plan satisfies the profile's allergen and macro-nutrient constraints.
3. The week's deliveries are scheduled against the Subscriber's delivery slots.
4. On failure, no plan is released and no partial plan is ever visible to the Subscriber.

**Main Success Scenario :**

1. Subscriber selects Generate Plan for the upcoming week.
2. System loads the Subscriber's health profile: calorie goal, carbohydrate ceiling, allergen exclusions, and cuisine preferences.
3. System retrieves candidate recipes from the menu catalogue for that week's kitchen availability.
4. System assembles a seven-day, twenty-one-meal draft plan matching the profile's daily calorie goal.
5. System «includes» UC-06 Validate Nutritional Constraints: every meal is checked against the allergen exclusion list, and each day's totals against the calorie and carbohydrate limits.
6. Validation passes. System saves the plan with status Draft and notifies the assigned Dietitian for review.
7. Dietitian opens the draft, reviews the daily macro breakdown, and approves it (FR-003).
8. System sets the plan status to Approved and schedules the week's deliveries against the Subscriber's delivery slots.
9. System displays the approved plan to the Subscriber and sends a confirmation notification.
10. Use case ends successfully.

**Alternate Flow : 5a. Nutritional Validation Fails**

Triggered at step 5 when one or more meals breach an allergen exclusion or a daily calorie/carbohydrate limit.

1. System flags each offending meal with the specific constraint it violated.
2. System searches the catalogue for a compliant substitute of equivalent meal type and calorie band, and replaces the flagged meal.
3. System re-runs UC-06 on the amended plan.
4. If validation now passes, the flow resumes at step 6.
5. If no compliant substitute exists after two substitution attempts, the System does not save a Draft. It raises a Constraint Conflict task for the Dietitian listing the unsatisfiable constraint, and notifies the Subscriber that the plan is pending dietitian input.
6. Use case ends in failure. No plan is released to the Subscriber, satisfying FR-001's zero-violation criterion.

**Alternate Flow : 7a. Dietitian Rejects the Draft**

1. Dietitian rejects the draft and enters a mandatory reason (FR-003).
2. System keeps the plan at status Draft and records the reason.
3. System returns the flow to step 4 for regeneration under the added constraint.
4. The Subscriber never sees the rejected draft.
