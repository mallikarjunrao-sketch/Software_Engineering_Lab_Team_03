# SE Lab 4: VibeCoding. Battleship vs AI

| | |
|---|---|
| **Name** | Kshitij Satish Shetty |
| **SRN** | PES1UG24AM143 |
| **Section** | C |
| **Course** | UE24CS341A, Software Engineering, PES University |
| **Assigned repo** | `SETAPESU26/19_battleship` |
| **LLM used** | Claude (full chat history included) |

A terminal Battleship game (6x6 board) against an AI. The assigned code had a
coordinate bug and was missing fleet, win, AI and feedback logic. I used an LLM as
a coding assistant to fix it one task at a time, then tested each change.

## Contents of this folder

| File | Description |
|---|---|
| `before_video.mp4` | 10 s gameplay before any changes, showing the broken behaviour |
| `after_video.mp4` | 10 s gameplay after all changes, showing the fixes and new features |
| `main.py` | Entry point |
| `game.py` | Setup, turn flow, input validation, result messages |
| `board.py` | Fleet, shot tracking, sinking and win detection |
| `ai.py` | Computer targeting |
| `test_*.py` | Tests for AI targeting, AI win, and output messages (in the repo root) |
| `PES1UG24AM143_ChatHistory.pdf` | Complete LLM chat history |

## How to run

```bash
python main.py
```

Type shots as `row,col` (1-indexed, for example `3,4`). Type `q` to quit.
Python 3.9+ and the standard library only, with no external dependencies.

## What was broken (before)

- Coordinates were not consistent. The AI returned a 1-indexed string that
  `game.py` checked against 0-indexed ship cells, so AI hits and misses were
  judged on the wrong cell.
- AI shots were never recorded on the board, so the AI could not win.
- The ship counter and the repeat-shot check read the wrong board, so repeated
  shots were accepted.

## Tasks completed (one commit each)

1. **Consistent coordinates.** All code uses 0-indexed `(row, col)` tuples. 1 is
   added only when printing, and subtracted once when reading player input.
   Every real ship cell is a hit and every empty cell is a miss, for both sides.
2. **Fleet and win logic.** Three ships per side (lengths 4, 3 and 2), with
   per-ship damage tracking and sunk detection (`Board.fire` returns `hit`,
   `miss`, `sunk` or `repeat`). Repeated shots are rejected and the game ends
   when a whole fleet is sunk (`Board.all_sunk`).
3. **Improved AI.** After a hit, the AI queues the up/down/left/right
   neighbours and fires at those first. It never fires at the same cell twice,
   and `choose()` returns `None` when no cells are left, which the game handles.
4. **Shot-level feedback.** Each real shot prints exactly one result line:
   `MISS!`, `HIT!` or `HIT! SUNK!` for the player, and the same text with an
   `AI ` prefix for the AI. Rejected input (repeat, out of range, bad format) and
   the AI's internal target selection print no result line.

## Testing

Run from the project root:

```bash
python -m unittest discover -p "test_*.py"
python test_ai_wins.py
```

Covered cases: hits, misses, repeated shots, sinking one ship, sinking all
ships, AI repeated-shot prevention, adjacent targeting after a hit, invalid
coordinates, quitting, and the one-result-line-per-shot check.

## Constraints followed

- No whole-project rewrite and no new dependencies.
- All state is kept in memory, with no files, JSON, CSV or SQLite.
- Separate commits for each task, and no PR to `SETAPESU26`.
