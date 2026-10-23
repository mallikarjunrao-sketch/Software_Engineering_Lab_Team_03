import contextlib
import io
import random
import re
import unittest
from unittest import mock

from ai import AI
from board import Board
from game import Battleship

RESULT_WORD = re.compile(r"\b(HIT|MISS|SUNK)\b")
SIZE = 6


def play(inputs, forced_ai=None, seed=None):
    """Run one game on scripted input. Returns (output lines, real shot log).

    shot_log holds ("P" or "AI", result) for every shot Board.fire accepted.
    """
    if seed is not None:
        random.seed(seed)
    game = Battleship()
    if forced_ai is not None:
        cells = iter(forced_ai)
        game.ai.choose = lambda: next(cells)

    shot_log = []
    real_fire = Board.fire

    def spy(self, pos):
        result = real_fire(self, pos)
        if result != "repeat":
            shot_log.append(("AI" if self is game.player else "P", result))
        return result

    feed = iter(inputs)
    buf = io.StringIO()
    with mock.patch.object(Board, "fire", spy), \
            mock.patch("builtins.input", lambda *_: next(feed)), \
            contextlib.redirect_stdout(buf):
        game.run()
    return buf.getvalue().splitlines(), shot_log


def result_lines(lines):
    return [line for line in lines if RESULT_WORD.search(line)]


def expected_lines(shot_log):
    text = Battleship.RESULT_TEXT
    return [text[res] if side == "P" else "AI " + text[res]
            for side, res in shot_log]


class TestOutputMessages(unittest.TestCase):
    def test_one_result_line_per_real_shot(self):
        junk = ["abc", "9,9", "0,0", "1", "1,2,3", ""]
        for seed in range(100):
            random.seed(seed)
            inputs = []
            for _ in range(300):
                if random.random() < 0.15:
                    inputs.append(random.choice(junk))
                else:
                    inputs.append(f"{random.randint(1, 6)},{random.randint(1, 6)}")
            inputs.append("q")
            lines, shot_log = play(inputs, seed=seed)
            self.assertGreater(len(shot_log), 0)
            self.assertEqual(result_lines(lines), expected_lines(shot_log),
                             f"seed {seed}")

    def test_ai_result_line_follows_its_fired_at_line(self):
        inputs = [f"{r},{c}" for r in range(1, 7) for c in range(1, 7)] + ["q"]
        lines, _ = play(inputs, seed=1)
        fired = [i for i, line in enumerate(lines) if line.startswith("AI fired at")]
        self.assertGreater(len(fired), 0)
        for i in fired:
            self.assertRegex(lines[i + 1], r"^AI (MISS!|HIT!|HIT! SUNK!)$")

    def test_rejected_input_prints_no_result_line(self):
        # 1,1 is a real shot (a miss). Everything after it is rejected.
        inputs = ["1,1", "1,1", "9,9", "0,0", "abc", "1", "1,2,3", "", "q"]
        lines, shot_log = play(inputs, seed=0)
        self.assertEqual(len(shot_log), 2, "only your shot and one AI reply")
        self.assertEqual(len(result_lines(lines)), 2)
        text = "\n".join(lines)
        self.assertEqual(text.count("Already fired there."), 1)
        self.assertEqual(text.count("Outside board."), 2)   # 9,9 and 0,0
        self.assertEqual(text.count("Use row,col."), 4)     # abc, 1, 1,2,3, blank

    def test_ai_does_not_move_on_rejected_input(self):
        inputs = ["1,1", "1,1", "1,1", "9,9", "q"]
        lines, _ = play(inputs, seed=0)
        self.assertEqual(sum(l.startswith("AI fired at") for l in lines), 1)

    def test_sunk_text_for_both_sides(self):
        # You sink all three enemy ships; the AI only misses.
        enemy_cells = ["2,3", "3,3", "4,3", "5,3", "6,1", "6,2", "6,3", "4,5", "4,6"]
        ai_misses = [(1, 0), (1, 1), (2, 0), (2, 2), (2, 3), (3, 3), (3, 4), (4, 0)]
        lines, _ = play(enemy_cells, forced_ai=ai_misses)
        self.assertEqual(lines.count("HIT! SUNK!"), 3)
        self.assertEqual(lines.count("AI MISS!"), 8)

        # The AI sinks all three of your ships; you only miss.
        ai_cells = [(0, 0), (0, 1), (0, 2), (0, 3), (2, 1), (3, 1), (4, 1),
                    (5, 4), (5, 5)]
        my_misses = ["1,1", "1,2", "1,3", "1,4", "1,5", "1,6", "2,1", "2,2", "3,1"]
        lines, _ = play(my_misses, forced_ai=ai_cells)
        self.assertEqual(lines.count("AI HIT! SUNK!"), 3)
        self.assertEqual(lines.count("AI HIT!"), 6)
        self.assertEqual(lines.count("MISS!"), 9)

    def test_ai_choose_and_record_print_nothing(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            for seed in range(30):
                random.seed(seed)
                ai = AI()
                for _ in range(SIZE * SIZE):
                    pos = ai.choose()
                    ai.record(pos, random.random() < 0.5)
                self.assertIsNone(ai.choose())          # full board
                ai.record((0, 0), True)                 # hit, nothing left to queue
        self.assertEqual(buf.getvalue(), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
