"""Pure game rules for the ROS pellet collection game.

This module deliberately has no ROS or Pygame dependency. Keeping the rules here
makes the behavior easy to test and gives the ROS node a small, clear interface.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import Iterable


@dataclass(frozen=True)
class Cell:
    """A zero-based location in the rectangular game grid."""

    column: int
    row: int


@dataclass
class GameState:
    """Track movement, pellets, timing, and the final game result."""

    columns: int = 20
    rows: int = 15
    pellet_count: int = 10
    seed: int | None = None
    spawn: Cell = field(default_factory=lambda: Cell(1, 1))

    player: Cell = field(init=False)
    pellets: set[Cell] = field(init=False)
    collected: int = field(default=0, init=False)
    elapsed_seconds: float = field(default=0.0, init=False)
    complete: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        if self.columns < 1 or self.rows < 1:
            raise ValueError("The grid must have at least one row and column")
        if not 0 <= self.spawn.column < self.columns or not 0 <= self.spawn.row < self.rows:
            raise ValueError("The spawn cell must be inside the grid")
        if self.pellet_count < 0 or self.pellet_count > self.columns * self.rows - 1:
            raise ValueError("pellet_count must fit on the grid outside the spawn cell")
        self.reset()

    @property
    def total_pellets(self) -> int:
        """Return the number of pellets placed for this round."""

        return self.collected + len(self.pellets)

    @property
    def pellets_per_minute(self) -> float:
        """Return the completed-round collection rate, guarding zero seconds."""

        if self.elapsed_seconds <= 0.0:
            return 0.0
        return self.collected / (self.elapsed_seconds / 60.0)

    def reset(self) -> None:
        """Start a fresh round with the configured pellet count."""

        self.player = self.spawn
        self.collected = 0
        self.elapsed_seconds = 0.0
        self.complete = self.pellet_count == 0

        generator = random.Random(self.seed)
        available = [
            Cell(column, row)
            for row in range(self.rows)
            for column in range(self.columns)
            if Cell(column, row) != self.spawn
        ]
        self.pellets = set(generator.sample(available, self.pellet_count))

    def move(self, column_delta: int, row_delta: int) -> bool:
        """Move one cell when the destination is inside the hard grid border."""

        if self.complete:
            return False
        destination = Cell(
            self.player.column + column_delta,
            self.player.row + row_delta,
        )
        if not 0 <= destination.column < self.columns or not 0 <= destination.row < self.rows:
            return False
        self.player = destination
        if destination in self.pellets:
            self.pellets.remove(destination)
            self.collected += 1
            self.complete = not self.pellets
        return True

    def advance_time(self, seconds: float) -> None:
        """Advance the timer while a round is active."""

        if seconds < 0:
            raise ValueError("seconds cannot be negative")
        if not self.complete:
            self.elapsed_seconds += seconds

    def place_pellets(self, cells: Iterable[Cell]) -> None:
        """Replace pellets for deterministic tests or a future level loader."""

        pellet_set = set(cells)
        if self.spawn in pellet_set:
            raise ValueError("A pellet cannot occupy the spawn cell")
        if any(
            not 0 <= cell.column < self.columns or not 0 <= cell.row < self.rows
            for cell in pellet_set
        ):
            raise ValueError("All pellets must be inside the grid")
        self.pellets = pellet_set
        self.pellet_count = len(pellet_set)
        self.collected = 0
        self.complete = not self.pellets
