# Requirements Table: Personalized Meal & Diet Subscription Manager

**Problem Statement #19 | Healthcare & Telemedicine**
Lab 1: Requirements Engineering & UML Use-Case Modelling. PES University, Dept. of CSE

**Scope.** A clinical dietary subscription service that generates weekly menus from patient
metabolic constraints (allergies, diabetic limits, calorie goals) and tracks daily delivery
fulfilment.

**Actors.** Subscriber, Dietitian, Delivery Agent, Payment Gateway (external system).

---

## Functional Requirements

| Req ID | Type | Description | Priority | Acceptance Criteria (measurable) | Rationale |
|---|---|---|---|---|---|
| **FR-001** | Functional | The system shall generate weekly meal plans strictly adhering to user macro-nutrient constraints and allergen exclusion lists. | High | **Pass:** Generated menu contains zero excluded allergen ingredients, and each day's totals fall within the profile's calorie goal ±10% and carbohydrate ceiling. **Fail:** Peanuts included for a peanut-allergic profile. | Core value of the service; a violated constraint is a clinical safety incident, not a usability defect. |
| **FR-002** | Functional | The system shall allow a Subscriber to create and update a health profile holding allergen exclusions, daily calorie goal, and diabetic carbohydrate limit. | High | **Pass:** After adding "peanut" and saving, reloading the profile lists peanut, and the next plan generated excludes it. **Fail:** A saved allergen is missing after reload, or appears in the next plan. | FR-001 cannot be evaluated without a stored, authoritative constraint set. |
| **FR-003** | Functional | The system shall require a Dietitian to approve or reject each generated weekly plan, recording a reason on rejection, before the plan is released to the Subscriber. | High | **Pass:** Plan status moves Draft → Approved only after a Dietitian action; a Draft plan requested by its Subscriber returns "not yet available". A rejection with an empty reason is refused. **Fail:** Subscriber can view or order from a Draft plan. | Clinical sign-off is mandatory for a dietary service treating diabetic and allergic patients. |
| **FR-004** | Functional | The system shall allow a Subscriber to pause, skip, or reschedule a scheduled delivery, and shall reject any such request submitted less than 12 hours before that delivery's dispatch time. | High | **Pass:** A skip submitted at dispatch − 12 h 01 min succeeds and the delivery disappears from the dispatch manifest; the same request at dispatch − 11 h 59 min is rejected with a cut-off message and the manifest is unchanged. **Fail:** A request inside the window alters the manifest. | Kitchen procurement is committed 12 h ahead; late changes produce food waste and mis-dispatch. |
| **FR-005** | Functional | The system shall record each daily delivery's fulfilment outcome (Delivered / Failed / Not Attempted) with a timestamp captured by the Delivery Agent, and expose it to the Subscriber and Dietitian. | Medium | **Pass:** When an agent marks a delivery Delivered, the Subscriber's dashboard shows Delivered with that timestamp on next load, and the daily fulfilment report totals equal the number of scheduled deliveries. **Fail:** A dispatched delivery has no outcome after its delivery window closes. | Fulfilment tracking is half the stated problem scope and is the evidence base for billing disputes and adherence review. |

## Non-Functional Requirements

| Req ID | Type | Description | Priority | Acceptance Criteria (measurable) | Rationale |
|---|---|---|---|---|---|
| **NFR-001** | Non-functional (Performance & Security) | The subscription engine must support schedule modifications (pause, skip, reschedule) up to 12 hours before dispatch. | High | **Pass:** Under a simulated peak of 500 concurrent modification requests, 95th-percentile response ≤ 2 s with zero errors; every request is authenticated and carried over TLS 1.2+; no request inside the 12 h window is accepted. **Fail:** p95 > 2 s, any unauthenticated modification accepted, or any accepted request inside the cut-off. | Schedule changes are the most frequently used feature and cluster in the evening peak; they also mutate billable state, so latency and authentication are graded together. |
| **NFR-002** | Non-functional (Security & Privacy) | The system shall store all subscriber health data (allergens, diabetic limits, clinical notes) encrypted at rest with AES-256, restrict read access to the owning Subscriber and their assigned Dietitian, and write an audit record for every access. | High | **Pass:** Direct database inspection shows no plaintext health fields; a Dietitian not assigned to a Subscriber receives HTTP 403, and that attempt appears in the audit log within 5 s. **Fail:** Any health field readable in plaintext, or any cross-account read that is served or goes unlogged. | The system holds identifiable clinical data; unauthorised disclosure is a regulatory breach, and audit records are what make the restriction provable. |
