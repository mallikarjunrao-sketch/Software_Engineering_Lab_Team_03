# Lab 5 Issues Table: music_catalog.py

Name: Kshitij Satish Shetty | SRN: PES1UG24AM143 | Repo: L5_19_music_catalog

Line numbers refer to the original file. Pylint score: 4.57/10 -> 10.00/10. Bandit: 4 issues -> 0. Flake8: 7 issues -> 0.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection (B608, Medium) | Security | 10 | The INSERT query is built with `%` string formatting, so a title like `x'); DROP TABLE songs;--` alters the SQL. | Use a parameterized query: `VALUES (?, ?, ?)` with a tuple of values. |
| Insecure deserialization (B301, Medium) | Security | 33 | `pickle.loads` can execute arbitrary code when given untrusted data. | Replace pickle with `json.dumps` / `json.loads` (a playlist is just a list of strings). |
| Pickle import (B403, Low) | Security | 1 | Importing `pickle` is flagged as a security risk. | Removed the import after switching to `json`. |
| Weak random generator (B311, Low) | Security | 17 | `random.choice` is not cryptographically secure. | Use `secrets.choice`. |
| Mutable default argument (W0102) | Bug | 9 | `playlist=[]` is created once and shared across all calls, so unrelated callers share one playlist. | Default to `None` and create a new list inside the function. |
| Bare except (E722 / W0702) | Bug | 39 | `except:` swallows every error, including KeyboardInterrupt. Also `SUM` returns `None` on an empty table, which the except never handled. | Catch `sqlite3.Error` only and use `or 0` for the empty-table case. |
| Line too long (E501 / C0301) | Style | 6, 10, 21, 49 | Lines exceed 79 characters. | Wrap long strings and calls over multiple lines. |
| Ambiguous variable name `l` (E741) | Style | 47 | `l` is easily confused with `1` or `I`. | Renamed to `songs`. |
| Multiple statements on one line (E701 / C0321) | Style | 48 | `if ...: print(...)` on one line. | Put the body on its own line. |
| Non-snake_case function names (C0103) | Style | 9, 15, 28, 32, 36 | `addSong`, `shufflePick`, `savePlaylist`, `loadPlaylist`, `totalPlays` break PEP 8. | Renamed to `add_song`, `shuffle_pick`, `save_playlist`, `load_playlist`, `total_plays`. |
| Missing docstrings (C0114 / C0116) | Style | 1, 9, 15, 20, 28, 32, 36, 43 | No module or function docstrings. | Added concise docstrings. |
| Unnecessary else after return (R1705) | Style | 22 | `else` after `return` adds nesting. | Removed `else` and de-indented. |
| Code runs on import | Design | 52 | `main()` is called at module level. | Added `if __name__ == "__main__":` guard. |
