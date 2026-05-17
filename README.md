# Agent-Based Disease Spread Simulation

Simulation of infectious disease spread in a population using an agent-based model (ABM), implemented in Python with the Mesa framework.

## Model

The model extends the classic SIR epidemiological model with six agent states:
- **S** – Susceptible
- **I** – Infected
- **R** – Recovered
- **D** – Dead
- **V** – Vaccinated
- **Q** – Quarantined

Agents move on a 40×40 grid and interact with neighbors. Model parameters are calibrated based on COVID-19 epidemiological data.

## Project Structure

```
agent-based-disease-spread/
|-- simulation/
|   |-- agent.py          # agent logic
|   |-- model.py          # model and grid
|   `-- visualization.py  # interactive visualization server
|-- experiments/
|   `-- experiments.py    # batch experiments
|-- figures/              # output charts
`-- report/               # LaTeX report
```

## Requirements

```bash
pip install mesa==2.3.0 mesa-viz-tornado pandas numpy matplotlib
```

## Usage

**Interactive visualization:**
```bash
python simulation/visualization.py
```
Open `http://localhost:8521` in your browser.

**Run experiments:**
```bash
python experiments/experiments.py
```
Results are saved to the `figures/` folder.

## Parameters

| Parameter | Symbol | Value | Source |
|-----------|--------|-------|--------|
| Infection rate | β | 0.08 | Alencar et al. (2022) |
| Recovery rate | γ | 0.07 | Alencar et al. (2022) |
| Mortality rate | δ | 0.001 | Alencar et al. (2022) |
| Vaccine effectiveness | ε | 0.84 | Tenforde et al. (2021) |
| Quarantine duration | q | 10 days | Liu et al. (2022) |

## Experiments

1. **Effect of infection rate (β)** — how transmissibility affects epidemic dynamics
2. **Intervention strategies** — comparing no intervention, quarantine, vaccination, and combined
3. **Vaccination campaign speed** — impact of daily vaccination rate on outcomes
4. **Age structure** — how population age distribution affects mortality

## References

- Kermack & McKendrick (1927) — original SIR model
- Railsback & Grimm (2011) — agent-based modeling methodology
- Kazil et al. (2020) — Mesa framework
- Alencar et al. (2022) — SIRD model parameters for UK COVID-19 data
- Tenforde et al. (2021) — vaccine effectiveness (CDC MMWR)
- Liu et al. (2022) — quarantine duration (JAMA Network Open)
- Levin et al. (2020) — age-specific infection fatality rates
