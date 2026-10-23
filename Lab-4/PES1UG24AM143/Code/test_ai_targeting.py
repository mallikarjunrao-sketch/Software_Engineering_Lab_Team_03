import random
import unittest

from ai import AI
from game import Battleship

SIZE = 6


def neighbors(cell):
    r, c = cell
    return {(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)}


class TestAITargeting(unittest.TestCase):
    def test_never_repeats_over_all_36_cells(self):
        for seed in range(50):
            random.seed(seed)
            ai = AI()
            shots = []
            for _ in range(SIZE * SIZE):
                pos = ai.choose()
                self.assertIsNotNone(pos, f"seed {seed}: ran out early")
                ai.record(pos, random.random() < 0.5)  # random hits and misses
                shots.append(pos)
            self.assertEqual(len(set(shots)), 36, f"seed {seed}: repeated a cell")
            self.assertTrue(all(0 <= r < SIZE and 0 <= c < SIZE for r, c in shots))

    def test_all_hits_still_never_repeats(self):
        ai = AI()
        shots = []
        for _ in range(SIZE * SIZE):
            pos = ai.choose()
            ai.record(pos, True)
            shots.append(pos)
        self.assertEqual(len(set(shots)), 36)

    def test_adjacent_targeting_after_hit_order(self):
        ai = AI()
        ai.tried.add((2, 2))
        ai.record((2, 2), True)
        # up, down, left, right
        self.assertEqual([ai.choose() for _ in range(4)],
                         [(1, 2), (3, 2), (2, 1), (2, 3)])

    def test_adjacent_targeting_in_real_games(self):
        # Whenever a hit has an untried neighbor, the next shot must be one.
        for seed in range(200):
            random.seed(seed)
            game = Battleship()
            ai = game.ai
            hits = []
            while not game.player.all_sunk():
                pending = {n for h in hits for n in neighbors(h)
                           if 0 <= n[0] < SIZE and 0 <= n[1] < SIZE
                           and n not in ai.tried}
                pos = ai.choose()
                if pending:
                    self.assertIn(pos, pending,
                                  f"seed {seed}: ignored a neighbor of a hit")
                result = game.player.fire(pos)
                ai.record(pos, result in ("hit", "sunk"))
                if result in ("hit", "sunk"):
                    hits.append(pos)

    def test_miss_queues_nothing(self):
        ai = AI()
        ai.tried.add((2, 2))
        ai.record((2, 2), False)
        self.assertEqual(ai.targets, [])

    def test_corner_hit_queues_only_in_bounds_neighbors(self):
        expected = {
            (0, 0): [(1, 0), (0, 1)],
            (0, 5): [(1, 5), (0, 4)],
            (5, 0): [(4, 0), (5, 1)],
            (5, 5): [(4, 5), (5, 4)],
        }
        for corner, cells in expected.items():
            ai = AI()
            ai.tried.add(corner)
            ai.record(corner, True)
            self.assertEqual(ai.targets, cells, f"corner {corner}")

    def test_tried_neighbors_are_not_queued(self):
        ai = AI()
        ai.tried |= {(2, 2), (1, 2), (2, 3)}
        ai.record((2, 2), True)
        self.assertEqual(ai.targets, [(3, 2), (2, 1)])

    def test_choose_returns_none_on_full_board(self):
        ai = AI()
        for _ in range(SIZE * SIZE):
            self.assertIsNotNone(ai.choose())
        self.assertIsNone(ai.choose())
        self.assertIsNone(ai.choose())  # stays safe when called again

    def test_choose_returns_none_when_queue_holds_only_tried_cells(self):
        ai = AI()
        ai.tried = {(r, c) for r in range(SIZE) for c in range(SIZE)}
        ai.targets = [(0, 0), (1, 1)]  # stale entries, all already tried
        self.assertIsNone(ai.choose())


if __name__ == "__main__":
    unittest.main(verbosity=2)
