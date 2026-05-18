# Cargo Routing Optimization (CO-008) Synthetic Dataset

# 1. Business Use Case

This synthetic dataset simulates a production-grade airline cargo routing optimization system used by Saudi Logistics Services (SAL).

The objective of the system is to help:

- Routing Managers
- Cargo Operations Controllers
- Commercial Cargo Teams
- Network Planning Teams
- Revenue Optimization Teams

select the most operationally efficient and commercially optimal cargo route for shipments destined to Jeddah (`JED`).

The dataset represents a realistic environment where every shipment may have multiple possible candidate routes.

The Machine Learning model evaluates all candidate routes and predicts an `optimization_score` between:

- `0.0` → Extremely poor route
- `1.0` → Highly optimal route

The system mimics real-world airline cargo decision-making logic.

---

# 2. Primary Business Objectives

The optimization engine attempts to balance multiple operational factors simultaneously:

| Objective | Description |
|---|---|
| Reduce Cost | Minimize transportation expense |
| Reduce Transit Time | Deliver cargo faster |
| Improve Reliability | Avoid delays and disruptions |
| Ensure Capacity | Verify sufficient aircraft space |
| Minimize Risk | Reduce weather and operational disruption |
| Reduce Connections | Avoid missed transshipments |
| Preserve Cargo Integrity | Ensure SHC compatibility |

---

# 3. Real-World Operational Scenario

For a single shipment from:

- Frankfurt (`FRA`)
to
- Jeddah (`JED`)

the system may evaluate:

| Candidate Route | Airline | Transit Time | Cost | Connections | Reliability |
|---|---|---|---|---|---|
| CR_01 | Lufthansa Cargo | 9 hrs | High | 0 | Very High |
| CR_02 | Qatar Airways Cargo | 13 hrs | Medium | 1 | High |
| CR_03 | Emirates SkyCargo | 18 hrs | Low | 2 | Medium |

The ML model assigns optimization scores to rank them.

Example:

| Candidate Route | optimization_score |
|---|---|
| CR_01 | 0.93 |
| CR_02 | 0.76 |
| CR_03 | 0.48 |

---

# 4. Dataset Files

| File Name | Description |
|---|---|
| cargo_routing_train.csv | Training dataset |
| cargo_routing_validation.csv | Validation dataset |
| cargo_routing_test.csv | Testing dataset |
| README.md | Complete dataset documentation |
| feature_contribution_reference.txt | Feature impact summary |

---

# 5. Dataset Statistics

| Split | Rows |
|---|---|
| Training | 14,000 |
| Validation | 3,500 |
| Testing | 3,500 |
| Total | 21,000 |

---

# 6. Temporal Coverage

Date Range:
- March 2025 → February 2026

The dataset intentionally spans:
- multiple seasons
- varying weather patterns
- changing operational conditions
- varying airline load factors

This helps the ML model generalize across real-world airline operational cycles.

---

# 7. Destination Airport

Destination is always:

- `JED`
- King Abdulaziz International Airport
- Jeddah, Saudi Arabia

This reflects SAL’s operational hub routing environment.

---

# 8. Feature Documentation

---

# 8.1 record_id

Unique routing record identifier.

Example:
- `RTE_000001`

Purpose:
- Identifies a single candidate route row.

Type:
- Identifier String

Characteristics:
- Globally unique
- Never repeated

---

# 8.2 timestamp

Datetime when the routing decision was generated.

Example:
- `2025-07-18 14:22:11`

Purpose:
- Simulates operational planning timestamp.

Type:
- Datetime

Used For:
- Season derivation
- Weather modeling
- Operational trend analysis

---

# 8.3 shipment_id

Unique shipment identifier.

Example:
- `SHP_000248`

Purpose:
- Groups multiple candidate routes together.

Important:
One shipment can have:
- 3 candidate routes
- 4 candidate routes
- 5 candidate routes
- 6 candidate routes

This simulates real airline route evaluation.

---

# 8.4 candidate_route_id

Unique candidate route within a shipment.

Examples:
- `CR_01`
- `CR_02`
- `CR_03`

Purpose:
- Distinguishes competing routing options.

---

# 8.5 origin

Origin airport IATA code.

---

## Europe

| Code | Airport |
|---|---|
| AMS | Amsterdam Schiphol |
| FRA | Frankfurt |
| LHR | London Heathrow |
| CDG | Paris Charles de Gaulle |
| BRU | Brussels |
| IST | Istanbul |
| MAD | Madrid |

---

## Middle East

| Code | Airport |
|---|---|
| DXB | Dubai |
| DOH | Doha |
| AUH | Abu Dhabi |
| RUH | Riyadh |
| KWI | Kuwait |

---

## Asia

| Code | Airport |
|---|---|
| SIN | Singapore |
| HKG | Hong Kong |
| PVG | Shanghai Pudong |
| ICN | Seoul Incheon |
| NRT | Tokyo Narita |
| DEL | Delhi |
| BOM | Mumbai |

---

## North America

| Code | Airport |
|---|---|
| JFK | New York |
| LAX | Los Angeles |
| ORD | Chicago |
| ATL | Atlanta |
| MIA | Miami |

---

## Africa

| Code | Airport |
|---|---|
| ADD | Addis Ababa |
| NBO | Nairobi |
| CAI | Cairo |
| JNB | Johannesburg |

---

# 8.6 destination

Destination airport.

Always:
- `JED`

Reason:
This dataset specifically models inbound cargo optimization into Saudi Arabia.

---

# 8.7 cargo_type

Defines operational cargo classification.

---

## General

Standard commercial freight.

Examples:
- Electronics
- Textiles
- Consumer goods

Characteristics:
- Lowest handling complexity
- Standard routing rules

---

## Perishable

Temperature-sensitive cargo.

Examples:
- Fresh food
- Flowers
- Seafood

Characteristics:
- Requires rapid routing
- Requires cold chain support

---

## Valuable

High-security cargo.

Examples:
- Gold
- Jewelry
- Luxury goods

Characteristics:
- Requires enhanced security
- Higher operational cost

---

## Dangerous

Hazardous materials.

Examples:
- Chemicals
- Flammable liquids
- Batteries

Characteristics:
- Strict airline regulations
- Restricted routing flexibility

---

## Heavy

Oversized or extremely heavy cargo.

Examples:
- Industrial equipment
- Machinery
- Engines

Characteristics:
- Special loading equipment required
- Higher handling cost

---

## Pharmaceutical

Medical and healthcare shipments.

Examples:
- Vaccines
- Biotech products
- Medical samples

Characteristics:
- Strict temperature control
- Extremely reliability-sensitive

---

# 8.8 cargo_weight_kg

Cargo shipment weight.

Type:
- Numeric

Typical Range:
- 50 kg → 15,000 kg

Operational Impact:
Higher weight:
- increases cost
- reduces routing flexibility
- requires higher capacity

---

# 8.9 cost_sar

Total route transportation cost in Saudi Riyal.

Currency:
- SAR

Factors affecting cost:
- Distance
- Cargo weight
- SHC requirements
- Priority level
- Connections
- Airline pricing
- Load factor

Typical Range:
- 4,000 SAR → 60,000 SAR

---

# 8.10 total_transit_time_hours

Total shipment transit duration.

Includes:
- flight time
- ground handling
- warehouse transfer
- transshipment delays

Important Rule:
Decimal portion represents minutes.

Examples:

| Value | Meaning |
|---|---|
| 10.15 | 10 hrs 15 mins |
| 12.45 | 12 hrs 45 mins |
| 8.05 | 8 hrs 5 mins |

Invalid examples intentionally avoided:
- 10.78
- 15.92

Because minutes cannot exceed 59.

---

# 8.11 capacity_available_kg

Available cargo space.

Purpose:
Determines if shipment can physically fit.

Important Operational Rule:
Capacity is usually greater than cargo weight.

Higher load factor reduces effective flexibility.

---

# 8.12 reliability_score

Operational reliability probability.

Range:
- 0.0 → 1.0

Higher values indicate:
- lower delay risk
- fewer disruptions
- better operational consistency

Direct routes usually have:
- higher reliability

Multi-connection routes usually have:
- lower reliability

---

# 8.13 num_connections

Number of transshipment points.

| Value | Meaning |
|---|---|
| 0 | Direct flight |
| 1 | Single connection |
| 2 | Double connection |

Operational Effects:
- increases transit time
- increases missed connection risk
- lowers reliability
- usually lowers cost

---

# 8.14 priority

Defines shipment urgency.

---

## Express

Characteristics:
- Fastest routing
- Highest reliability preference
- Higher cost acceptable

Operational Bias:
- favors direct flights

---

## Standard

Characteristics:
- Balanced optimization
- moderate cost sensitivity
- moderate speed sensitivity

---

## Economy

Characteristics:
- Lowest cost preference
- transit time less important

Operational Bias:
- may allow multiple connections

---

# 8.15 airline

Cargo airline operating the route.

Examples:
- Saudia Cargo
- Qatar Airways Cargo
- Emirates SkyCargo
- Lufthansa Cargo
- Turkish Cargo
- Etihad Cargo
- Cargolux
- Cathay Cargo

Different airlines simulate:
- operational reliability differences
- network efficiency differences
- regional connectivity

---

# 8.16 distance_km

Approximate routing distance to Jeddah.

Range:
- 850 km → 13,500 km

Operational Relationship:
Longer distance:
- increases cost
- increases flight time

---

# 8.17 weather_risk_score

Operational weather disruption probability.

Range:
- 0.0 → 1.0

Higher values indicate:
- thunderstorms
- sandstorms
- heavy rain
- low visibility
- airport disruption risk

Important Seasonal Logic:
- May includes sandstorm risk
- August includes rainfall instability

Weather scores are intentionally month-consistent.

---

# 8.18 season

Derived from timestamp month.

| Season | Months |
|---|---|
| Winter | December → February |
| Spring | March → April |
| Summer | May → August |
| Monsoon | September → November |

Important:
Season assignment strictly follows month consistency.

---

# 8.19 load_factor

Aircraft cargo utilization ratio.

Range:
- 0.0 → 1.0

Meaning:
Higher values indicate flights are nearing full capacity.

Operational Effects:
- reduces routing flexibility
- reduces available cargo space
- may increase operational risk

---

# 8.20 shc_code (Special Handling Code)

Special cargo handling classification.

---

## GEN — General Cargo

Standard commercial cargo.

---

## PER — Perishable Cargo

Requires rapid handling.

---

## ICE — Ice Cooling Required

Temperature-controlled cargo requiring refrigeration.

---

## FRO — Frozen Cargo

Frozen shipment requiring strict cold-chain compliance.

---

## DGR — Dangerous Goods

Hazardous material shipment.

---

## VAL — Valuable Cargo

High-security monitored cargo.

---

## AVI — Live Animals

Live animal transportation.

---

## ELI — Lithium Ion Batteries

Hazardous lithium-ion battery cargo.

---

## ELM — Lithium Metal Batteries

Lithium metal battery shipment.

---

## CAO — Cargo Aircraft Only

Shipment restricted to freighter aircraft.

---

## HEA — Heavy Cargo

Oversized or extremely heavy cargo.

---

# SHC Compatibility Rules

| Cargo Type | Typical SHC Codes |
|---|---|
| General | GEN |
| Perishable | PER, ICE, FRO |
| Valuable | VAL |
| Dangerous | DGR, CAO |
| Heavy | HEA |
| Pharmaceutical | PER, ICE |

---

# 8.21 optimization_score

Target variable.

Range:
- 0.0 → 1.0

Meaning:
Higher score = more operationally optimal route.

Purpose:
Used for:
- route ranking
- recommendation systems
- cargo optimization AI

---

# 9. Optimization Score Generation Logic

The optimization score is generated using realistic multi-factor operational logic.

The score is NOT random.

It combines:
- operational feasibility
- cost efficiency
- transit efficiency
- risk reduction
- reliability optimization

---

# 10. Weighted Contribution Structure

| Feature Group | Approximate Weight |
|---|---|
| Cost efficiency | 24% |
| Transit time efficiency | 24% |
| Reliability | 22% |
| Weather risk | 10% |
| Connection penalty | 8% |
| Capacity adequacy | 7% |
| Load factor efficiency | 5% |

---

# 11. Mathematical Foundation

The production routing engine is assumed to use:
- XGBoost Regressor
- Gradient Boosted Trees
- Additive feature contributions

---

# 11.1 Core Ensemble Equation

$$
\hat{y}_i = \sum_{k=1}^{K} f_k(x_i)
$$

Where:

| Symbol | Meaning |
|---|---|
| $\hat{y}_i$ | Final predicted optimization score |
| $K$ | Total decision trees |
| $f_k$ | Individual tree |
| $x_i$ | Route feature vector |

---

# 11.2 Explainable Additive Formula

$$
Score = Base\_Score + \sum_{j=1}^{N} Impact(Feature_j)
$$

Expanded:

$$
Score =
0.5000
+
\Delta_{Reliability}
+
\Delta_{Capacity}
-
\Delta_{Cost}
-
\Delta_{TransitTime}
-
\Delta_{WeatherRisk}
-
\Delta_{Connections}
-
\Delta_{LoadFactor}
$$

---

# 11.3 Simplified Operational Formula

$$
Score =
(W_{rel} \times Reliability)
+
(W_{cap} \times Capacity)
+
(W_{cost} \times CostEfficiency)
+
(W_{time} \times TimeEfficiency)
+
(W_{weather} \times WeatherSafety)
-
Penalty_{Connections}
-
Penalty_{LoadFactor}
$$

---

# 12. Example Operational Calculation

Example Route:

| Feature | Value |
|---|---|
| Cost | 15,000 SAR |
| Transit Time | 11.25 hrs |
| Reliability | 0.91 |
| Connections | 0 |
| Weather Risk | 0.18 |

Feature Impacts:

| Feature | Contribution |
|---|---|
| Reliability | +0.18 |
| Transit Efficiency | +0.16 |
| Cost Penalty | -0.07 |
| Weather Risk | -0.02 |
| Connection Penalty | 0.00 |

Final:

$$
Score = 0.50 + 0.18 + 0.16 - 0.07 - 0.02 = 0.75
$$

Interpretation:
- Strongly recommended route

---

# 13. Operational Relationships Enforced

---

## Distance vs Transit Time

Longer distance:
- increases cost
- increases transit duration

---

## Direct Flights

Advantages:
- faster
- safer
- more reliable

Disadvantages:
- more expensive

---

## Multi-Connection Flights

Advantages:
- lower cost

Disadvantages:
- longer transit
- higher delay risk
- lower reliability

---

## Weather Logic

Higher weather risk:
- reduces reliability
- reduces optimization score

---

## Load Factor Logic

Higher load factor:
- reduces effective capacity
- reduces operational flexibility

---

## Priority Logic

Express cargo:
- prioritizes speed and reliability

Economy cargo:
- prioritizes lower cost

---

# 14. Machine Learning Characteristics

The dataset is intentionally designed to support:

- Regression modeling
- Ranking systems
- Explainable AI
- Route recommendation engines
- Operational simulation
- Feature importance analysis
- SHAP explainability
- XGBoost/CatBoost/LightGBM training

---

# 15. Data Quality Guarantees

The dataset guarantees:

- No null values
- No duplicate rows
- Realistic operational logic
- Consistent SHC mappings
- Consistent seasonal behavior
- Realistic cargo-airline relationships
- Realistic routing patterns

---

# 16. Intended AI Applications

This dataset can power:

- Smart cargo routing engines
- Airline decision support systems
- Revenue optimization tools
- AI-powered cargo dashboards
- Commercial route recommendation systems
- Operational disruption prediction systems

---

# 17. Final Notes

This dataset was intentionally engineered to resemble:
- real airline cargo operational exports
- freight forwarder optimization systems
- airport cargo planning systems
- Saudi cargo logistics environments

The optimization target is fully learnable and suitable for:
- supervised machine learning
- explainable AI
- ranking optimization
- operational analytics
- dashboard demonstrations
