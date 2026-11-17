# SE Lab 3: Component Modelling & Architectural Pattern Selection

**Venkata Srivaibhav Nukaraju | PES2UG24CS579 | 5-J**
**System:** Personalized Meal & Diet Subscription Manager (Lab 1, Problem Statement #19)
**Architecture selected:** Microservices

## Submission

| # | Deliverable | Format asked for | Submitted file |
|---|---|---|---|
| 1 | Component diagram | PNG or PDF | [`component-diagram.png`](component-diagram.png) (+ [PDF](component-diagram.pdf)) |
| 2 | Written justification, max 1 page | Word | [`PES2UG24CS579_SE_Lab3.docx`](PES2UG24CS579_SE_Lab3.docx) |

The PNG embeds the diagram XML, so it reopens as an editable diagram in draw.io; the PDF does
not. [`component-diagram.drawio`](component-diagram.drawio) is the source and opens directly
(app.diagrams.net → File ▸ Open, or the desktop app).

Step 6 asks for the justification as a PDF. The .docx ships here; export the PDF by hand after
any edits.

## Components (6)

The handout supplies the first two and asks for three more. The API Gateway is a sixth, added to
give the three client apps one authenticated entry point.

| Component | Responsibility | Requirements |
|---|---|---|
| Order Manager | Subscription orders, delivery schedule, 12-hour change cut-off | FR-004, NFR-001 |
| Payment Service | Billing and skip credits; holds gateway tokens, never card numbers | FR-004 |
| Meal Plan Service | Weekly plan generation, dietitian approval lifecycle | FR-001, FR-003 |
| Health Profile Service | Sole owner of allergens, carbohydrate limits, clinical notes | FR-002, NFR-002 |
| Delivery Tracking | Fulfilment outcomes and the dispatch manifest | FR-005 |
| API Gateway | Request routing, TLS termination, token authentication | NFR-001, NFR-002 |

## Interfaces (6)

| Interface | Provided by | Required by | Protocol |
|---|---|---|---|
| `IPayment` | Payment Service | Order Manager | REST / JSON over mTLS |
| `IMealPlan` | Meal Plan Service | API Gateway, Order Manager | REST / JSON over HTTPS |
| `IHealthProfile` | Health Profile Service | API Gateway, Meal Plan Service | REST / JSON over mTLS |
| `ISubscription` | Order Manager | API Gateway | REST / JSON over HTTPS |
| `IDelivery` | Delivery Tracking | API Gateway, Order Manager | REST / JSON over HTTPS |
| `IGatewayCharge` | Payment Gateway «external system» | Payment Service | HTTPS (PCI-DSS) |

`Order Manager ↔ Payment Service` is the interface the handout names. Each is drawn with ball
(provided) and socket (required) notation; the three client apps reach the API Gateway through
«use» dependencies.

## Why Microservices

Two requirements from Lab 1 drive the choice.

- **NFR-001** caps schedule changes at a 2-second 95th-percentile response under 500 concurrent
  requests, and those requests cluster in one evening peak. Meal plan generation is slow and
  compute-heavy with no such deadline. Separating the two means the evening peak replicates only
  the Order Manager.
- **NFR-002** requires AES-256 at rest, restricted reads, and an audit record per access. One
  service owns that store, so the access check and the audit record sit at a single boundary and
  no other service holds credentials for it.

Fault isolation is the third argument: the external payment gateway and the handheld delivery
devices fail often, and neither failure should stop a dietitian approving a plan.

## Rebuilding

```bash
python3 scripts/build.py     # -> PES2UG24CS579_SE_Lab3.docx  (needs python-docx)

# diagram, via the draw.io desktop app CLI
drawio -x -f png -e --crop -b 20 -s 2 -o component-diagram.png component-diagram.drawio
drawio -x -f pdf -e --crop -b 20    -o component-diagram.pdf component-diagram.drawio
```
