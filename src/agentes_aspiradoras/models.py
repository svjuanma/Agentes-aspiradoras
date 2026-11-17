''' 
# - Description: Vacuum cleaner (Agent) and Model class definitions
# 
# - Authors:
# A01802469 Juan Manuel Sanchez Velazquez
# A01763687 David Elias Vargas Ayala
# 
# - Creation date: November 15th 2026
# - Last Modification: November 15th 2026
'''

import mesa
from mesa import agentset
from mesa.discrete_space import CellAgent
from math import floor

DIRECTIONS: list[tuple[int, int]] = [
    (-1, -1), (-1, 0 ), (-1, 1),  (0, -1), (0, 1),  (1, -1) , (1, 0), (1, 1),
] 


class VacuumAgent(CellAgent):
    moves: int  = 0

    def __init__(self, model: mesa.Model) -> None:
        super().__init__(model)
        self.cell: mesa.discrete_space.Cell | None = None
    
    def clean(self):
        ''' Cleans the current cell if dirty
        
        Args: 
            None

        Return:
            None
        '''

        if self.cell is not None and self.cell.dirty:
            self.cell.dirty = False
    
    def navigate(self):
        '''Navigates from the cell to a random neighboring cell based on a grid navigation system,
         updates the number of moves
        
        Args: 
                    None
        
                Return:
                    None
        '''
        if self.cell is None:
            return
        #Check if cell is dirty to clean it 
        if self.cell.dirty:
            self.clean()
            return
        #Get random direction to move
        randomDir = self.random.choice(DIRECTIONS)
        target = self.cell.connections.get(randomDir)

        #Move to a dirty target
        if target is not None:
            self.move_to(target)
            self.moves += 1





class VacuumModel(mesa.Model):
    def __init__(
            self, 
            height: int = 3, 
            width: int = 3, 
            n: int = 10, 
            dirtyPercentage: float = 0.10) -> None:
        ''' Vacuum cleaner model constructor.
    
        Args:
            height: Grid's height for agents navigation. Defaults 3 (minimum logical threshold for a 8 neighbors grid).
            width: Grid's width for agents navigation. Defaults 3 (minimum logical threshold for a 8 neighbors grid).
            n: Agents number in simulation. Defaults 10.
            dirtyPercentage: Initial percentage of cells being dirty.

        Return:
            None
        '''
        super().__init__()

        # Create grid with vertical, horizontal and diagonal possible movements and declare dirtiness property
        self.grid = mesa.discrete_space.OrthogonalMooreGrid((width,height), torus=False)
        self.grid.create_property_layer("dirty", default_value=False, dtype=bool) 

        self.agents: agentset.AgentSet[VacuumAgent] = VacuumAgent.create_agents(self, n)

        # Check if dirtiness percentage is valid [0,1]
        if dirtyPercentage <= 1 and dirtyPercentage >= 0: 
            self.dirtyCellsPercent: float = dirtyPercentage 
        else: 
            raise ValueError(f"Value {dirtyPercentage =} out of range.\n\tSet a float between 0 and 1")
        
        # Place agents in location [1,1] of grid
        for agent in self.agents:
            cell = self.grid.all_cells.select(lambda cell: cell.position == (1,1))
            agent.cell = cell

        # Dirt cells
        cells2Dirt: int = floor(width * height * dirtyPercentage)
        for _ in range(cells2Dirt):
            cell = self.grid.all_cells.select(lambda cell: not cell.dirty).select_random_cell()
            cell.dirty = True


    def step(self) -> None:
        ''' Step function to define what do agents do at every time unit
        
        Args:
            None

        Returns:
            None

        '''
        for agent in self.agents:
            agent.navigate() 