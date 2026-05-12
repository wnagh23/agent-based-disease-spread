import random
from mesa import Agent

class PersonAgent(Agent):

    def __init__(self, unique_id, model, state="S"):
        super().__init__(unique_id, model)
        self.state = state
        self.age_group = random.choices(
            ["young","adult","senior"],
            weights=[0.2, 0.6, 0.2]
        )[0]
        self.quarantine_days_left = 0

    def step(self):
        if self.state == "D":
            return
        if self.state == "Q":
            self.quarantine_days_left -= 1
            if self.quarantine_days_left <= 0:
                self.state = "I"
            self._try_recover()
            return
        self._move()
        if self.state == "I":
            self._try_quarantine()
            if self.state == "I":
                self._try_infect_neighbors()
                self._try_recover()

    def _try_quarantine(self):
        if random.random() < self.model.quarantine_rate:
            self.state = "Q"
            self.quarantine_days_left = self.model.quarantine_duration

    def _move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def _try_infect_neighbors(self):
        neighbors = self.model.grid.get_cell_list_contents(
            self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        )
        for neighbor in neighbors:
            if neighbor.state == "S":
                if random.random() < self.model.beta:
                    neighbor.state = "I"
            elif neighbor.state == "V":
                effective_beta = self.model.beta * (1 - self.model.vaccine_effectiveness)
                if random.random() < effective_beta:
                    neighbor.state = "I"

    def _try_recover(self):
        delta, gamma = self._get_age_params()
        if random.random() < delta:
            self.state = "D"
        elif random.random() < gamma:
            self.state = "R"

    def _get_age_params(self):
        base_gamma = self.model.gamma
        base_delta = self.model.delta
        if self.age_group == "young":
            return base_delta * 0.1, base_gamma * 2.0
        if self.age_group == "adult":
            return base_delta, base_gamma
        else:
            return base_delta * 3.0, base_gamma * 0.6