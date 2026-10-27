import builtins
import contextlib
import io

from game import Battleship

# Your fleet, 1-indexed as typed, converted to 0-indexed (row, col) tuples.
FLEET_1_INDEXED = [
    (1, 1), (1, 2), (1, 3), (1, 4),
    (3, 2), (4, 2), (5, 2),
    (6, 5), (6, 6),
]
AI_SHOTS = [(r - 1, c - 1) for r, c in FLEET_1_INDEXED]

# Player shots, all misses (none are enemy cells). The 10th is a spare that
# must never be read if the game stops correctly.
PLAYER_INPUTS = ["1,1", "1,2", "1,3", "1,4", "1,5", "1,6", "2,1", "2,2", "3,1",
                 "3,2"]

game = Battleship()
ai_iter = iter(AI_SHOTS)
ai_calls = []
game.ai.choose = lambda: ai_calls.append(1) or next(ai_iter)

inputs = iter(PLAYER_INPUTS)
inputs_read = []
builtins.input = lambda *_: inputs_read.append(1) or next(inputs)

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    game.run()
output = buf.getvalue()
print(output)

assert game.player.all_sunk(), "AI should have sunk the whole player fleet"
assert not game.enemy.all_sunk(), "Player must not have won"
assert "The AI sank your fleet." in output, "AI win message missing"
assert "You sank the fleet." not in output, "Player win message should not appear"
assert len(ai_calls) == 9, f"AI should take exactly 9 turns, took {len(ai_calls)}"
assert len(inputs_read) == 9, f"Game should stop after 9 prompts, read {len(inputs_read)}"
assert output.rstrip().endswith("The AI sank your fleet."), "Game kept printing after the AI won"
print("PASS: AI wins after 9 turns and the game stops.")
