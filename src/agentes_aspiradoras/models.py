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
from mesa.discrete_space import CellAgent
from math import floor

DIRECTIONS: list[tuple[int, int]] = [
    (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1),
]


class VacuumAgent(CellAgent):
    def __init__(self, model: mesa.Model, cell) -> None:
        super().__init__(model)
        self.cell = cell
        self.moves = 0

    def clean(self) -> None:
        '''Cleans the current cell if dirty'''
        if self.cell.dirty:
            self.cell.dirty = False

    def navigate(self) -> None:
        '''Cleans if the cell is dirty, otherwise moves to a random neighbor'''
        if self.cell.dirty:
            self.clean()
            return
        target = self.cell.connections.get(self.random.choice(DIRECTIONS))
        if target is not None:
            self.cell = target
            self.moves += 1


class VacuumModel(mesa.Model):
    def __init__(self, height: int = 3, width: int = 3, n: int = 10,
                 dirtyPercentage: float = 0.10) -> None:
        '''Vacuum cleaner model constructor.

        Args:
            height: Grid height. Defaults 3.
            width: Grid width. Defaults 3.
            n: Number of agents. Defaults 10.
            dirtyPercentage: Initial percentage of dirty cells, in [0, 1].
        '''
        super().__init__()
        if not 0 <= dirtyPercentage <= 1:
            raise ValueError(f"Value {dirtyPercentage = } out of range.\n\tSet a float between 0 and 1")
        self.dirtyCellsPercent = dirtyPercentage

        self.grid = mesa.discrete_space.OrthogonalMooreGrid((width, height), torus=False)
        self.grid.create_property_layer("dirty", default_value=False, dtype=bool)

        # All agents start at (1, 1)
        start = self.grid[(1, 1)]
        VacuumAgent.create_agents(self, n, [start] * n)

        # Dirty cells
        cells2Dirt = floor(width * height * dirtyPercentage)
        for cell in self.random.sample(list(self.grid.all_cells), cells2Dirt):
            cell.dirty = True

    def step(self) -> None:
        '''What every agent does at each time unit'''
        self.agents.shuffle_do("navigate")
