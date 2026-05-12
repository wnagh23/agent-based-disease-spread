from mesa_viz_tornado.ModularVisualization import ModularServer
from mesa_viz_tornado.modules import CanvasGrid, ChartModule
from mesa_viz_tornado.UserParam import Slider
from simulation.model import DiseaseModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5, "Layer": 0}
    if agent.state == "S":
        portrayal["Color"] = "blue"
    elif agent.state == "I":
        portrayal["Color"] = "red"
    elif agent.state == "D":
        portrayal["Color"] = "black"
        portrayal["r"] = 0.3
    elif agent.state == "V":
        portrayal["Color"] = "purple"
        portrayal["r"] = 0.5
    elif agent.state == "Q":
        portrayal["Color"] = "orange"
        portrayal["r"] = 0.4
    else:
        portrayal["Color"] = "green"
    return portrayal

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

chart = ChartModule([
    {"Label": "S", "Color": "blue"},
    {"Label": "I", "Color": "red"},
    {"Label": "R", "Color": "green"},
    {"Label": "D", "Color": "black"},
    {"Label": "V", "Color": "purple"},
    {"Label": "Q", "Color": "orange"},
])

model_params = {
    "N": Slider("Liczba agentów", 200, 50, 500, 50),
    "width": 20,
    "height": 20,
    "beta": Slider("Beta (zaraźliwość)", 0.05, 0.0, 0.3, 0.01),
    "gamma": Slider("Gamma (powrót do zdrowia)", 0.07, 0.0, 0.3, 0.01),
    "delta": Slider("Delta (śmiertelność)", 0.0007, 0.0, 0.05, 0.0001),
    "initial_infected": Slider("Początkowa liczba chorych", 5, 1, 50, 1),
    "vaccination_rate": Slider("Tempo szczepień (% populacji/dzień)", 0.003, 0.0, 0.02, 0.001),
    "vaccine_effectiveness": Slider("Skuteczność szczepionki", 0.85, 0.0, 1.0, 0.05),
    "quarantine_duration": Slider("Długość kwarantanny", 10, 0, 20, 1),
    "quarantine_rate": Slider("Prawdopodobieństwo kwarantanny", 0.2, 0.0, 1.0, 0.05),
}

server = ModularServer(
    DiseaseModel,
    [grid, chart],
    "Symulacja SIR",
    model_params
)

server.port = 8521
server.launch()