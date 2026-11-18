''' 
# - Description: Python's main module to join agent and model classes
# 
# - Authors:
# A01802469 Juan Manuel Sanchez Velazquez
# A01763687 David Elias Vargas Ayala
# 
# - Creation date: November 15th 2026
# - Last Modification: November 16th 2026
'''
import matplotlib.pyplot as plt

from agentes_aspiradoras.models import VacuumAgent, VacuumModel


def dirtyCount(model: VacuumModel) -> int:
    '''Calculates the number of cells that are dirty

    Args:
        model: The simulation model whose grid is inspected.

    Return:
        int: Number of cells that are still dirty.
    '''
    return sum(1 for cell in model.grid.all_cells if cell.dirty)


def totalMoves(model: VacuumModel) -> int:
    '''Adds up the moves made so far by every agent

    Args:
        model: The simulation model whose agents are inspected.

    Return:
        int: Total number of moves of all agents.
    '''
    return sum(agent.moves for agent in model.agents)


def runSim(height: int, width: int, n: int, dirtPercentage: float, maxTime: int
           ) -> tuple[int, float, int, dict[str, list[float]]]:
    '''Run a simulation until all cells are clean or the max time is reached

    Args:
        height: the rooms height (M)
        width: the rooms width (N)
        n: number of agents
        dirtPercentage: The iniciator of the quantity of dirt in the room
        maxTime: The max number of steps

    Return:
        tuple: steps taken, % of clean cells in the end, the total of moves and
        a history dict with the per-step series "clean" (% of clean cells) and
        "moves" (cumulative moves), both starting at step 0.
    '''
    model = VacuumModel(height = height, width = width, n = n, dirtyPercentage = dirtPercentage)
    totalCells: int = height * width
    history: dict[str, list[float]] = {
        "clean": [100 * (totalCells - dirtyCount(model)) / totalCells],
        "moves": [totalMoves(model)],
    }
    while dirtyCount(model) > 0 and model.steps < maxTime:
        model.step()
        history["clean"].append(100 * (totalCells - dirtyCount(model)) / totalCells)
        history["moves"].append(totalMoves(model))
    cleanCellsPercent: float = history["clean"][-1]
    return model.steps, cleanCellsPercent, totalMoves(model), history


def plotMetrics(history: dict[str, list[float]], steps: int, cleanPercent: float,
                moves: int, outputPath: str = "metricas.png") -> None:
    '''Plot the simulation metrics, save them to a PNG file and show them

    Draws three charts: clean cells % over time, cumulative agent moves over
    time and a bar chart with the final summary (steps, clean %, moves).

    Args:
        history: Per-step series returned by runSim ("clean" and "moves").
        steps: Total steps taken by the simulation.
        cleanPercent: Final % of clean cells.
        moves: Total moves made by all agents.
        outputPath: File where the figure is saved. Defaults "metricas.png".

    Return:
        None
    '''
    fig, (axClean, axMoves, axSummary) = plt.subplots(1, 3, figsize=(16, 4.5))

    axClean.plot(history["clean"], color="tab:green")
    axClean.set_title("Celdas limpias a lo largo del tiempo")
    axClean.set_xlabel("Paso de tiempo")
    axClean.set_ylabel("Celdas limpias (%)")
    axClean.set_ylim(0, 105)
    axClean.grid(alpha=0.3)

    axMoves.plot(history["moves"], color="tab:blue")
    axMoves.set_title("Movimientos acumulados de los agentes")
    axMoves.set_xlabel("Paso de tiempo")
    axMoves.set_ylabel("Movimientos")
    axMoves.grid(alpha=0.3)

    labels = ["Pasos", "% limpio", "Movimientos"]
    values = [steps, cleanPercent, moves]
    bars = axSummary.bar(labels, values, color=["tab:orange", "tab:green", "tab:blue"])
    axSummary.bar_label(bars, fmt="%g")
    axSummary.set_title("Resumen final")

    fig.tight_layout()
    fig.savefig(outputPath, dpi=150)
    plt.show()


def main() -> None:
    ''' Main flow to glue all Python's modules together.

    Runs the simulation, prints the metrics and plots them.

    Args:
        No args.

    Return:
        None
    '''

    height, width = 10, 10
    n = 29
    dirtyPercentage: float = 0.4
    maxTime: int = 700

    steps, cleanPercent, moves, history = runSim(height, width, n, dirtyPercentage, maxTime)
    print(f"Tiempo hasta que todas las celdas estén limpias (o tiempo máximo): {steps}")
    print(f"Porcentaje de celdas limpias al final: {cleanPercent:.2f}%")
    print(f"Número total de movimientos de los agentes: {moves}")
    plotMetrics(history, steps, cleanPercent, moves)
