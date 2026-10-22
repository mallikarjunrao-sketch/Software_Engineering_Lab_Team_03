# Lab 4: VibeCoding - Donkey Kong Repair Lab

**Student SRN:** PES1UG24AM155
**Assigned repo:** [SETAPESU26/30_donkeykong](https://github.com/SETAPESU26/30_donkeykong)
**Working repo (one commit per task):** [mallikarjunrao-sketch/30_donkeykong](https://github.com/mallikarjunrao-sketch/30_donkeykong)
**AI tool used:** Claude (Anthropic)
**Chat history link:** https://claude.ai/chat/97f6e25c-b1e8-4fac-a278-78dde08428fe

---

## Overview

A single-file Donkey Kong-style game written in Python with Pygame. The player climbs ladders and
jumps barrels to reach the princess. The starter code had one deliberate bug and three empty
feature hooks. This lab fixes the bug and implements all three features by prompting an AI
assistant, then reviewing and testing the result.

## Deliverables in this folder

| File | Description |
|------|-------------|
| `game.py` | Final updated game with all tasks completed |
| `before.mp4` | 10-second gameplay video before any changes (showing the bug) |
| `after.mp4` | 10-second gameplay video after all changes |
| Chat history PDF | Record of the AI-assisted work |
| `README.md` | This file |

## How to run

Requires Python 3.10 or newer.

```bash
pip install pygame
python game.py
```

**Controls**

| Key | Action |
|-----|--------|
| Left / Right | Move |
| Space | Jump |
| Up / Down | Climb a ladder (stand near it first) |
| R | Reset the game |

Reach the princess at the top to win. Three barrel hits end the game.

## Tasks completed

### Task 1: Fix the ladder-descent bug

**Problem:** Barrels took the first ladder they reached about 7 times out of 10, so the lower
platforms flooded with barrels and the top platform emptied out.

**Fix:** In `Barrel.update`, the probability check `random.random() < 0.7` was changed to use
`LADDER_DESCENT_CHANCE = 0.3`, so barrels descend about 3 times out of 10.

```python
# Before
if random.random() < 0.7:
# After
if random.random() < LADDER_DESCENT_CHANCE:   # 0.3
```

**Verified:** 20,000 simulated ladder encounters gave a descent rate of 29.97%.

### Task 2: `theme_color(score)`

The background colour shifts from the default navy `(15, 15, 25)` toward a warm dark red
`(90, 25, 15)` as the score rises. It returns `None` at score 0 (keeping the default) and reaches
the full warm colour at a score of 2000 (`THEME_MAX_SCORE`).

### Task 3: `on_barrel_jumped(player, barrel)`

When the player clears a barrel, a floating label spawns at the barrel's position. It rises and
fades out over 0.9 seconds. The label shows the real points awarded (`+100`, or `+200` once the
multiplier is active). Labels are updated every frame in the main loop and cleared on reset.

### Task 4: `score_multiplier(score)`

Returns `2` once the score reaches 500 (`MULTIPLIER_THRESHOLD`) and `None` otherwise (the default
1x). Late-game barrel jumps are therefore worth 200 points instead of 100.

## Additional fix: barrel-jump scoring window

While testing, the score never increased from jumping. The original scoring check only counted a
barrel if it passed less than 40 px below the player's feet and within 12 px horizontally, but a
jump peaks at about 80 px, so normal jumps almost never scored. The window was widened using two
named constants:

```python
JUMP_CLEAR_HEIGHT = 90   # was 40
JUMP_CLEAR_DX = 18       # was 12
```

A jump started roughly 20 to 70 px from an approaching barrel now scores. To revert to the
original strict behaviour, set the constants back to 40 and 12.

## Tunable constants

All new behaviour is controlled by constants at the top of `game.py`:

| Constant | Value | Meaning |
|----------|-------|---------|
| `LADDER_DESCENT_CHANCE` | 0.3 | Chance a barrel takes a ladder |
| `THEME_MAX_SCORE` | 2000 | Score at which the background is fully warm |
| `THEME_WARM_COLOR` | (90, 25, 15) | Final background colour |
| `MULTIPLIER_THRESHOLD` | 500 | Score after which jump bonuses double |
| `FLOAT_LIFETIME` | 0.9 | Seconds a floating label stays visible |
| `JUMP_CLEAR_HEIGHT` / `JUMP_CLEAR_DX` | 90 / 18 | Barrel-jump scoring window |

## How the work was tested

Each change was checked with a headless script (no window) before being used:

- **Task 1:** simulated barrel-ladder encounters and measured the descent rate.
- **Task 2:** score 0 returns `None`; score 1000 returns `(52, 20, 20)`; scores of 2000 and above
  return `(90, 25, 15)`.
- **Task 3:** a label appears with the right text, rises, fades, and is removed after about 0.9 s.
- **Task 4:** multiplier is `None` below 500 and `2` at 500 or more.
- **Scoring window:** simulated jumps at different distances from an approaching barrel.

## Commit history (working repo)

| Commit | Message |
|--------|---------|
| `f631c75` | Task 1: fix ladder descent probability (0.7 -> 0.3) |
| `5162180` | Task 2: implement theme_color |
| `d0279c4` | Task 3: implement on_barrel_jumped floating +100 label |
| `26e55dd` | Task 4: implement score_multiplier (2x after 500) |
| `fcc8f3a` | Widen barrel-jump scoring window so jumps register |
| `1fa76dd` | Add Lab-4 deliverables |

## What to see in the videos

- **`before.mp4`:** barrels mostly take the first ladder they reach; the background stays navy;
  no floating labels appear.
- **`after.mp4`:** barrels often keep rolling past ladders; "+100" labels appear when jumping a
  barrel; the background warms as the score grows; labels become "+200" past a score of 500.
