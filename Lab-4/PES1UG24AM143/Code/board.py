class Board:
    SIZE = 6

    def __init__(self):
        self.fleet = []      # list of ships, each a set of (row, col) cells
        self.ships = set()   # every ship cell, for quick lookups
        self.shots = set()

    def place_ship(self, cells):
        cells = set(cells)
        if not cells or any(not (0 <= r < self.SIZE and 0 <= c < self.SIZE)
                            for r, c in cells):
            raise ValueError("Ship is outside the board.")
        if cells & self.ships:
            raise ValueError("Ships overlap.")
        self.fleet.append(cells)
        self.ships |= cells

    def fire(self, pos):
        """Return 'repeat', 'miss', 'hit' or 'sunk'. A repeat is not recorded."""
        if pos in self.shots:
            return "repeat"
        self.shots.add(pos)
        for ship in self.fleet:
            if pos in ship:
                return "sunk" if ship <= self.shots else "hit"
        return "miss"

    def ships_afloat(self):
        return sum(1 for ship in self.fleet if not ship <= self.shots)

    def all_sunk(self):
        return all(ship <= self.shots for ship in self.fleet)