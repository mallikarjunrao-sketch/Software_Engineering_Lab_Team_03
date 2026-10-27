import random


class AI:
    def __init__(self, size=6):
        self.size = size
        self.tried = set()
        self.targets = []  # untried cells next to earlier hits, in firing order

    def choose(self):
        """Return an untried (row, col), or None if every cell has been tried."""
        pos = None
        while self.targets and pos is None:
            candidate = self.targets.pop(0)
            if candidate not in self.tried:
                pos = candidate
        if pos is None:
            options = [(r, c) for r in range(self.size) for c in range(self.size)
                       if (r, c) not in self.tried]
            if not options:
                return None
            pos = random.choice(options)
        self.tried.add(pos)
        return pos

    def record(self, pos, hit):
        """Tell the AI how its shot went; after a hit, queue the neighbors."""
        if not hit:
            return
        r, c = pos
        for nxt in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):  # up, down, left, right
            if (0 <= nxt[0] < self.size and 0 <= nxt[1] < self.size
                    and nxt not in self.tried and nxt not in self.targets):
                self.targets.append(nxt)