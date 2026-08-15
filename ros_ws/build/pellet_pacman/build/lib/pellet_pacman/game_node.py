"""ROS 2 node and Pygame renderer for the pellet collection game."""

from __future__ import annotations

import random
import time

import pygame
import rclpy
from geometry_msgs.msg import Point
from rclpy.node import Node
from std_msgs.msg import Bool, Float32, UInt32

from .game_state import Cell, GameState


class PelletPacmanNode(Node):
    """Connect the pure game rules to a Pygame window and ROS topics."""

    def __init__(self) -> None:
        super().__init__("pellet_pacman")
        self.columns = self.declare_parameter("columns", 20).value
        self.rows = self.declare_parameter("rows", 15).value
        self.min_pellets = self.declare_parameter("min_pellets", 5).value
        self.max_pellets = self.declare_parameter("max_pellets", 20).value
        self.seed = self.declare_parameter("seed", -1).value
        self.window_width = self.declare_parameter("window_width", 900).value
        self.window_height = self.declare_parameter("window_height", 700).value
        self.frame_rate = self.declare_parameter("frame_rate", 30).value

        self._validate_parameters()
        self._random = random.Random(None if self.seed < 0 else self.seed)
        self.game = self._new_game()
        self.last_update = time.monotonic()

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("ROS 2 Pellet Pac-Man")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.large_font = pygame.font.Font(None, 46)

        self.position_publisher = self.create_publisher(Point, "player_position", 10)
        self.remaining_publisher = self.create_publisher(UInt32, "pellets_remaining", 10)
        self.collected_publisher = self.create_publisher(UInt32, "pellets_collected", 10)
        self.elapsed_publisher = self.create_publisher(Float32, "elapsed_seconds", 10)
        self.complete_publisher = self.create_publisher(Bool, "complete", 10)
        self.timer = self.create_timer(1.0 / self.frame_rate, self.update)
        self.get_logger().info("Pellet game started. Use arrows or WASD to move.")

    def _validate_parameters(self) -> None:
        """Reject settings that would create an unusable game window."""

        if self.columns < 2 or self.rows < 2:
            raise ValueError("columns and rows must both be at least 2")
        if self.min_pellets < 0 or self.max_pellets < self.min_pellets:
            raise ValueError("pellet range must satisfy 0 <= min_pellets <= max_pellets")
        if self.max_pellets > self.columns * self.rows - 1:
            raise ValueError("max_pellets must fit outside the player spawn cell")
        if self.window_width < 320 or self.window_height < 240:
            raise ValueError("window dimensions are too small")
        if self.frame_rate < 1:
            raise ValueError("frame_rate must be positive")

    def _new_game(self) -> GameState:
        """Create a round using the configured pellet range and random seed."""

        pellet_count = self._random.randint(self.min_pellets, self.max_pellets)
        seed = self._random.randrange(2**32)
        spawn = Cell(self.columns // 2, self.rows // 2)
        return GameState(self.columns, self.rows, pellet_count, seed, spawn)

    def update(self) -> None:
        """Process one frame, advance the rules, render, and publish state."""

        now = time.monotonic()
        elapsed = now - self.last_update
        self.last_update = now
        self._process_events()
        self.game.advance_time(elapsed)
        self._publish_state()
        self._draw()
        pygame.display.flip()
        self.clock.tick(self.frame_rate)

    def _process_events(self) -> None:
        """Translate keyboard events into one-cell game movements."""

        movement = {
            pygame.K_LEFT: (-1, 0),
            pygame.K_a: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_d: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_w: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_s: (0, 1),
        }
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_q
            ):
                rclpy.shutdown()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.game = self._new_game()
                self.last_update = time.monotonic()
            elif event.type == pygame.KEYDOWN and event.key in movement:
                self.game.move(*movement[event.key])

    def _publish_state(self) -> None:
        """Expose the current round through small, inspectable ROS topics."""

        position = Point()
        position.x = float(self.game.player.column)
        position.y = float(self.game.player.row)
        self.position_publisher.publish(position)

        remaining = UInt32()
        remaining.data = len(self.game.pellets)
        self.remaining_publisher.publish(remaining)

        collected = UInt32()
        collected.data = self.game.collected
        self.collected_publisher.publish(collected)

        elapsed = Float32()
        elapsed.data = float(self.game.elapsed_seconds)
        self.elapsed_publisher.publish(elapsed)

        complete = Bool()
        complete.data = self.game.complete
        self.complete_publisher.publish(complete)

    def _draw(self) -> None:
        """Render the board, HUD, player, pellets, and completion result."""

        background = (12, 18, 30)
        board = (25, 35, 52)
        border = (75, 95, 125)
        yellow = (250, 210, 55)
        white = (235, 240, 248)
        green = (90, 220, 150)
        self.screen.fill(background)

        hud_height = 70
        cell_size = min(
            (self.window_width - 40) // self.columns,
            (self.window_height - hud_height - 40) // self.rows,
        )
        board_width = cell_size * self.columns
        board_height = cell_size * self.rows
        origin_x = (self.window_width - board_width) // 2
        origin_y = hud_height + (self.window_height - hud_height - board_height) // 2

        pygame.draw.rect(
            self.screen,
            board,
            (origin_x, origin_y, board_width, board_height),
        )
        for column in range(self.columns + 1):
            x = origin_x + column * cell_size
            pygame.draw.line(self.screen, border, (x, origin_y), (x, origin_y + board_height), 1)
        for row in range(self.rows + 1):
            y = origin_y + row * cell_size
            pygame.draw.line(self.screen, border, (origin_x, y), (origin_x + board_width, y), 1)

        for pellet in self.game.pellets:
            center = (
                origin_x + pellet.column * cell_size + cell_size // 2,
                origin_y + pellet.row * cell_size + cell_size // 2,
            )
            pygame.draw.circle(self.screen, yellow, center, max(4, cell_size // 8))

        player_center = (
            origin_x + self.game.player.column * cell_size + cell_size // 2,
            origin_y + self.game.player.row * cell_size + cell_size // 2,
        )
        pygame.draw.circle(self.screen, yellow, player_center, max(8, cell_size // 3))
        mouth = [
            player_center,
            (player_center[0] + cell_size // 3, player_center[1] - cell_size // 5),
            (player_center[0] + cell_size // 3, player_center[1] + cell_size // 5),
        ]
        pygame.draw.polygon(self.screen, board, mouth)

        hud = self.font.render(
            f"Pellets: {self.game.collected}/{self.game.total_pellets}    "
            f"Time: {self.game.elapsed_seconds:.1f}s    R: reset  Q: quit",
            True,
            white,
        )
        self.screen.blit(hud, (20, 20))
        if self.game.complete:
            result = self.large_font.render(
                f"Complete! {self.game.collected} pellets in "
                f"{self.game.elapsed_seconds:.1f}s "
                f"({self.game.pellets_per_minute:.1f} pellets/min)",
                True,
                green,
            )
            self.screen.blit(
                result,
                result.get_rect(center=(self.window_width // 2, self.window_height - 30)),
            )

    def destroy_node(self) -> bool:
        """Close Pygame before handing shutdown back to ROS 2."""

        pygame.quit()
        return super().destroy_node()


def main(args: list[str] | None = None) -> None:
    """Run the game node until the window is closed or Q is pressed."""

    rclpy.init(args=args)
    node = PelletPacmanNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
