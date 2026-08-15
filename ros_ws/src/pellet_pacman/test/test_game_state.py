import unittest

from pellet_pacman.game_state import Cell, GameState


class GameStateTest(unittest.TestCase):
    def test_seeded_pellets_are_inside_grid_and_avoid_spawn(self):
        game = GameState(columns=5, rows=4, pellet_count=5, seed=4)

        self.assertEqual(len(game.pellets), 5)
        self.assertNotIn(game.spawn, game.pellets)
        self.assertTrue(all(0 <= cell.column < 5 and 0 <= cell.row < 4 for cell in game.pellets))

    def test_movement_cannot_leave_grid(self):
        game = GameState(columns=3, rows=3, pellet_count=1, spawn=Cell(0, 0), seed=1)

        self.assertFalse(game.move(-1, 0))
        self.assertFalse(game.move(0, -1))
        self.assertEqual(game.player, Cell(0, 0))

    def test_collecting_pellet_completes_round_once(self):
        game = GameState(columns=3, rows=3, pellet_count=1, spawn=Cell(0, 0), seed=1)
        game.place_pellets([Cell(1, 0)])

        self.assertTrue(game.move(1, 0))
        self.assertEqual(game.collected, 1)
        self.assertTrue(game.complete)
        self.assertFalse(game.move(-1, 0))
        self.assertEqual(game.collected, 1)

    def test_rate_is_zero_before_time_and_correct_after_time(self):
        game = GameState(columns=3, rows=3, pellet_count=1, seed=1)
        game.place_pellets([Cell(1, 0)])

        self.assertEqual(game.pellets_per_minute, 0.0)
        game.elapsed_seconds = 30.0
        game.collected = 1
        self.assertEqual(game.pellets_per_minute, 2.0)

    def test_reset_restores_round(self):
        game = GameState(columns=3, rows=3, pellet_count=1, seed=1)
        original_pellets = game.pellets.copy()
        game.place_pellets([Cell(1, 0)])
        game.move(1, 0)
        game.advance_time(10)

        game.reset()

        self.assertEqual(game.player, game.spawn)
        self.assertEqual(game.collected, 0)
        self.assertEqual(game.elapsed_seconds, 0.0)
        self.assertFalse(game.complete)
        self.assertEqual(game.pellets, original_pellets)


if __name__ == "__main__":
    unittest.main()
