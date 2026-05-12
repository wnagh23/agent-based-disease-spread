import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simulation.model import DiseaseModel

os.makedirs("figures", exist_ok=True)

BASE_PARAMS = {
    "N": 1000,
    "width": 40,
    "height": 40,
    "beta": 0.05,
    "gamma": 0.07,
    "delta": 0.0007,
    "initial_infected": 5,
    "vaccination_rate": 0.0,
    "vaccine_effectiveness": 0.85,
    "quarantine_duration": 10,
    "quarantine_rate": 0.0,
}

STEPS = 300
RUNS = 20


def run_simulation(params, steps=STEPS):
    model = DiseaseModel(**params)
    for _ in range(steps):
        model.step()
    return model.datacollector.get_model_vars_dataframe()


def average_runs(params, runs=RUNS):
    results = [run_simulation(params) for _ in range(runs)]
    avg = pd.concat(results).groupby(level=0).mean()
    std = pd.concat(results).groupby(level=0).std()
    return avg, std


def plot_with_std(ax, data_avg, data_std, column, label, color, smooth=7):
    avg_smooth = data_avg[column].rolling(smooth, center=True, min_periods=1).mean()
    std_smooth = data_std[column].rolling(smooth, center=True, min_periods=1).mean()
    ax.plot(avg_smooth, label=label, color=color)
    ax.fill_between(
        data_avg.index,
        avg_smooth - std_smooth,
        avg_smooth + std_smooth,
        alpha=0.2,
        color=color
    )


def experiment_1():
    print("Eksperyment 1: wpływ β...")

    beta_values = [0.02, 0.05, 0.08, 0.12, 0.20]
    colors = ["#2ecc71", "#3498db", "#f39c12", "#e74c3c", "#8e44ad"]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("Eksperyment 1 — Wpływ współczynnika zaraźliwości β", fontsize=13)

    for beta, color in zip(beta_values, colors):
        params = {**BASE_PARAMS, "beta": beta}
        avg, std = average_runs(params)
        label = f"β={beta}"
        for ax, col in zip(axes, ["I", "R", "D"]):
            plot_with_std(ax, avg, std, col, label, color)

    titles = ["Zarażeni (I)", "Odporni (R)", "Zgony (D)"]
    for ax, title in zip(axes, titles):
        ax.set_title(title)
        ax.set_xlabel("Dzień")
        ax.set_ylabel("Liczba agentów")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("figures/exp1_beta.png", dpi=150)
    plt.close()
    print("zapisano figures/exp1_beta.png")


def experiment_2():
    print("Eksperyment 2: scenariusze interwencji...")

    scenarios = {
        "Brak interwencji":        {**BASE_PARAMS},
        "Tylko kwarantanna":       {**BASE_PARAMS, "quarantine_rate": 0.3},
        "Tylko szczepienia":       {**BASE_PARAMS, "vaccination_rate": 0.003},
        "Kwarantanna + szczepienia": {**BASE_PARAMS, "quarantine_rate": 0.3, "vaccination_rate": 0.003},
    }
    colors = ["#e74c3c", "#f39c12", "#3498db", "#2ecc71"]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("Eksperyment 2 — Porównanie strategii interwencji", fontsize=13)

    for (label, params), color in zip(scenarios.items(), colors):
        avg, std = average_runs(params)
        for ax, col in zip(axes, ["I", "R", "D"]):
            plot_with_std(ax, avg, std, col, label, color)

    titles = ["Zarażeni (I)", "Odporni (R)", "Zgony (D)"]
    for ax, title in zip(axes, titles):
        ax.set_title(title)
        ax.set_xlabel("Dzień")
        ax.set_ylabel("Liczba agentów")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("figures/exp2_interventions.png", dpi=150)
    plt.close()
    print("zapisano figures/exp2_interventions.png")


def experiment_3():
    print("Eksperyment 3: tempo kampanii szczepień...")

    vaccination_rates = [0.0, 0.001, 0.003, 0.007, 0.015]
    labels = ["brak", "0.1%/dzień", "0.3%/dzień (Szwecja avg)", "0.7%/dzień", "1.5%/dzień"]
    colors = ["#e74c3c", "#f39c12", "#f1c40f", "#2ecc71", "#3498db"]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("Eksperyment 3 — Wpływ tempa kampanii szczepień", fontsize=13)

    for rate, label, color in zip(vaccination_rates, labels, colors):
        params = {**BASE_PARAMS, "vaccination_rate": rate}
        avg, std = average_runs(params)
        for ax, col in zip(axes, ["I", "V", "D"]):
            plot_with_std(ax, avg, std, col, label, color)

    titles = ["Zarażeni (I)", "Zaszczepieni (V)", "Zgony (D)"]
    for ax, title in zip(axes, titles):
        ax.set_title(title)
        ax.set_xlabel("Dzień")
        ax.set_ylabel("Liczba agentów")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("figures/exp3_vaccination.png", dpi=150)
    plt.close()
    print("zapisano figures/exp3_vaccination.png")

def experiment_4():
    print("Eksperyment 4: struktura wiekowa...")

    age_scenarios = {
        "Młoda\n(70/20/10)":        [0.7, 0.2, 0.1],
        "Przeciętna\n(20/60/20)":   [0.2, 0.6, 0.2],
        "Starzejąca się\n(10/50/40)": [0.1, 0.5, 0.4],
    }
    colors = ["#3498db", "#f39c12", "#e74c3c"]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Eksperyment 4 — Wpływ struktury wiekowej na przebieg epidemii", fontsize=13)

    for (label, weights), color in zip(age_scenarios.items(), colors):
        mortality_rates = []
        peak_infected = []
        for _ in range(RUNS):
            model = DiseaseModel(**BASE_PARAMS)
            for agent in model.schedule.agents:
                agent.age_group = random.choices(
                    ["young", "adult", "senior"], weights=weights
                )[0]
            for _ in range(STEPS):
                model.step()
            df = model.datacollector.get_model_vars_dataframe()
            mortality_rates.append(df["D"].iloc[-1] / BASE_PARAMS["N"] * 100)
            peak_infected.append(df["I"].max())

        axes[0].bar(label, np.mean(mortality_rates), color=color, alpha=0.8,
                    yerr=np.std(mortality_rates), capsize=5)
        axes[1].bar(label, np.mean(peak_infected), color=color, alpha=0.8,
                    yerr=np.std(peak_infected), capsize=5)

    axes[0].set_title("Śmiertelność (%)")
    axes[1].set_title("Szczyt zachorowań")
    axes[0].set_ylabel("% populacji")
    axes[1].set_ylabel("Liczba agentów")
    for ax in axes:
        ax.tick_params(axis='x', labelsize=8)
        ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig("figures/exp4_age.png", dpi=150)
    plt.close()
    print("zapisano figures/exp4_age.png")


if __name__ == "__main__":
    experiment_1()
    experiment_2()
    experiment_3()
    experiment_4()