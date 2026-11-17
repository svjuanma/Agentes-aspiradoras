''' 
# - Description: Python's main module to join agent and model classes
# 
# - Authors:
# A01802469 Juan Manuel Sanchez Velazquez
# A01763687 David Elias Vargas Ayala
# 
# - Creation date: November 15th 2026
# - Last Modification: November 15th 2026
'''
from agentes_aspiradoras.models import VacuumAgent, VacuumModel

def dirtyCount(model: VacuumModel) -> int:
    '''Calculates the number of cells that are dirty
    Args:
        None

    Return:
        None
            
    '''
    return sum(1 for cell in model.grid.all_cells if cell.dirty)

def runSim(height: int, width: int, n: int, dirtPercentage: float, maxTime: int) -> tuple[int, float, int]:
    '''run a simulation until all cells are clean or the room is empty
    
    Args:
        height: the rooms height (M)
        width: the rooms width (N)
        n: number of agents
        dirtPercentage: The iniciator of the quantity of dirt in the room
        maxTime: The max number of steps

    Return:
        tuple: as in steps taken, % of clean cells in the end, the total of moves
    '''
    model = VacuumModel(height = height, width = width, n = n, dirtPercentage = dirtPercentage, maxTime = maxTime)
    totalCells: int = height * width
    while dirtyCount(model) > 0 and model.steps < maxTime:
        model.step()
    cleanCellsPercent: float = 100 * (totalCells - dirtyCount(model)) / totalCells
    totalMoves: int = sum(agent.moves for agent in model.agents)
    return model.steps, cleanCellsPercent, totalMoves
    

def main() -> None:
    ''' Main flow to glue all Python's modules together.
    
    Args:
        No args.

    Return:
        None
    '''
    print("Hello from agentes-aspiradoras!")

    height, width = 10, 10
    dirtyPercentage: float = 0.4
    maxTime: int = 700
    rounds: int = 30

