# SE Lab 2: Agile Backlog Creation & Sprint Simulation in Jira

**Vaibhav .N** · PES University, Dept. of CSE
**System:** Personalized Meal & Diet Subscription Manager (Lab 1, Problem Statement #19)
**Jira project:** [Diet Subscription Manager (DSM)](https://srivaibhav.atlassian.net/jira/software/c/projects/DSM/boards/34) — company-managed Scrum

## Submission

| Deliverable | File |
|---|---|
| Report + reflection answers | [`LAB2_SE_Final_Report.docx`](LAB2_SE_Final_Report.docx) |
| Backlog with epics and user stories | [`screenshots/01-backlog-epics-stories.png`](screenshots/01-backlog-epics-stories.png) |
| Story point assignments | [`screenshots/02-story-points.png`](screenshots/02-story-points.png) |
| Active sprint board | [`screenshots/03-active-sprint-board.png`](screenshots/03-active-sprint-board.png) |
| Burndown chart | [`screenshots/04-burndown-chart.png`](screenshots/04-burndown-chart.png) |
| Issue comments (step 4) | [`screenshots/05-issue-comments.png`](screenshots/05-issue-comments.png) |

Export the .docx to PDF by hand after any edits.

## Coverage of the assignment steps

| Step | Where |
|---|---|
| 1. Create stories | 9 stories, DSM-4 … DSM-12 |
| 2. Story points (planning poker, team discussion) | Fibonacci 3/5/8, rationale in report §3 |
| 3. Prioritise & rank backlog | High/Medium set; backlog reordered so High ranks above Medium |
| 4. Mock sprint (create, simulate, comment) | 2 sprints, 9 comments across 7 stories |
| 5. Burndown chart | Sprint 1, with event log |
| 6. Reflection | Report §5, four questions plus next-sprint actions |

## What was built in Jira

- **3 epics** (DSM-1 … DSM-3) mapped from the Lab 1 requirements table
- **9 user stories** (DSM-4 … DSM-12), 40 story points, ranked High → Medium
- **Sprint 1** — 26 points committed, 18 delivered, DSM-6 (8 pts) carried over
- **Sprint 2** — 16 points committed, 16 delivered
- 34 of 40 points done; DSM-11 and DSM-12 remain in the backlog
- Velocity: 18, then 16

## Rebuilding the report

```bash
python3 scripts/build.py      # report.md + screenshots/ -> LAB2_SE_Final_Report.docx
```

Needs `python3-markdown` and `libreoffice`. Screenshots are inlined as data URIs so the .docx
carries them rather than linking to local paths.
