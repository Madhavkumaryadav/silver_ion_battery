# Architecture Diagram and Experiment Template

## Architecture Diagram

```mermaid
flowchart TD
    A[Material Selection] --> B[Slurry Formulation]
    B --> C[Coating and Drying]
    C --> D[Cell Assembly and Sealing]
    D --> E[Formation Cycling]
    E --> F[Baseline Electrochemical Tests]
    F --> G[Parameter Extraction]
    G --> G1[q_ah]
    G --> G2[r0_ohm]
    G --> G3[r1_ohm]
    G --> G4[c1_f]
    G --> G5[v_min and v_max]
    G1 --> H[ECM Simulation]
    G2 --> H
    G3 --> H
    G4 --> H
    G5 --> H
    H --> I[Outputs: SOC, OCV, Vp, Vt]
```

## Clean Documentation Template for Each Experiment

Record these fields for every run:

- Run ID and date
- Cell format and dimensions
- Material lot numbers
- Ratio used (active/conductive/binder)
- Slurry solids percentage
- Coating thickness and drying condition
- Electrolyte quantity used
- Formation protocol
- Capacity and efficiency results
- Extracted ECM parameters
