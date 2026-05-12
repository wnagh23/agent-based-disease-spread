from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from simulation.agent import PersonAgent
import random

class DiseaseModel(Model):

    def __init__(self, N, width, height, beta, gamma, delta,
                 vaccination_rate, vaccine_effectiveness,
                 quarantine_duration, quarantine_rate, initial_infected=5):
        super().__init__()
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.vaccination_rate = vaccination_rate
        self.vaccine_effectiveness = vaccine_effectiveness
        self.quarantine_rate = quarantine_rate
        self.quarantine_duration = quarantine_duration
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)

        self.datacollector = DataCollector(
            model_reporters={
                "S": lambda m: sum(1 for a in m.schedule.agents if a.state == "S"),
                "I": lambda m: sum(1 for a in m.schedule.agents if a.state == "I"),
                "R": lambda m: sum(1 for a in m.schedule.agents if a.state == "R"),
                "D": lambda m: sum(1 for a in m.schedule.agents if a.state == "D"),
                "V": lambda m: sum(1 for a in m.schedule.agents if a.state == "V"),
                "Q": lambda m: sum(1 for a in m.schedule.agents if a.state == "Q"),
            }
        )

        for i in range(N):
            state = "I" if i < initial_infected else "S"
            agent = PersonAgent(i, self, state)
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        self.running = True

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

        if self.vaccination_rate > 0:
            susceptible = [a for a in self.schedule.agents if a.state == "S"]
            to_vaccinate_count = max(1, int(self.vaccination_rate * self.schedule.get_agent_count()))
            to_vaccinate = self.random.sample(
                susceptible,
                min(to_vaccinate_count, len(susceptible))
            )
            for agent in to_vaccinate:
                agent.state = "V"