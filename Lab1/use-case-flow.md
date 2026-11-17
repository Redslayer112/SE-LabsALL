# Use-Case Flow Specification

**System:** Personalized Meal &amp; Diet Subscription Manager &nbsp;•&nbsp; **Use Case:** UC-02 Generate Weekly Meal Plan<br>
**Primary Actor:** Subscriber &nbsp;•&nbsp; **Supporting Actors:** Dietitian, Nutrition Rules Engine<br>
**Related Requirements:** FR-001, FR-002, FR-003 &nbsp;•&nbsp; **Includes:** UC-06 Validate Nutritional Constraints

---

### Preconditions

1. The Subscriber is authenticated and holds an active subscription.
2. A health profile exists for the Subscriber with a calorie goal, carbohydrate limit, and allergen exclusion list (FR-002).
3. No Approved plan already exists for the target week.

### Postconditions

- **Success:** A seven-day plan exists for the target week with status *Approved*, every meal satisfies the profile's constraints, and the plan is visible to the Subscriber.
- **Failure:** No plan is released; the week remains unplanned and the Subscriber is told why. No partial plan is ever visible to the Subscriber.

---

### Main Success Scenario

1. Subscriber selects **Generate Plan** for the upcoming week.
2. System loads the Subscriber's health profile: calorie goal, carbohydrate ceiling, allergen exclusions, and cuisine preferences.
3. System retrieves candidate recipes from the menu catalogue for that week's kitchen availability.
4. System assembles a seven-day, twenty-one-meal draft plan matching the profile's daily calorie goal.
5. System **«includes» UC-06 Validate Nutritional Constraints**: every meal is checked against the allergen exclusion list, and each day's totals against the calorie and carbohydrate limits.
6. Validation passes. System saves the plan with status *Draft* and notifies the assigned Dietitian for review.
7. Dietitian opens the draft, reviews the daily macro breakdown, and **approves** it (FR-003).
8. System sets the plan status to *Approved* and schedules the week's deliveries against the Subscriber's delivery slots.
9. System displays the approved plan to the Subscriber and sends a confirmation notification.
10. Use case ends successfully.

---

### Alternate Flow 5a: Nutritional Validation Fails

Triggered at step 5 when one or more meals breach an allergen exclusion or a daily calorie/carbohydrate limit.

- **5a1.** System flags each offending meal with the specific constraint it violated.
- **5a2.** System searches the catalogue for a compliant substitute of equivalent meal type and calorie band, and replaces the flagged meal.
- **5a3.** System re-runs UC-06 on the amended plan.
- **5a4.** If validation now passes, the flow resumes at **step 6**.
- **5a5.** If no compliant substitute exists after two substitution attempts, the System does **not** save a Draft. It raises a *Constraint Conflict* task for the Dietitian listing the unsatisfiable constraint, and notifies the Subscriber that the plan is pending dietitian input.
- **5a6.** Use case ends in failure. No plan is released to the Subscriber, satisfying FR-001's zero-violation criterion.

### Alternate Flow 7a: Dietitian Rejects the Draft

- **7a1.** Dietitian rejects the draft and enters a mandatory reason (FR-003).
- **7a2.** System keeps the plan at status *Draft*, records the reason, and returns the flow to **step 4** for regeneration under the added constraint.
- **7a3.** The Subscriber never sees the rejected draft.
