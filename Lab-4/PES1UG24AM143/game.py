from board import Board
from ai import AI


class Battleship:
    RESULT_TEXT = {"miss": "MISS!", "hit": "HIT!", "sunk": "HIT! SUNK!"}

    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI()
        self._setup()

    def _setup(self):
        # Ships of length 4, 3 and 2 for each side, as 0-indexed (row, col).
        for cells in (
            {(0, 0), (0, 1), (0, 2), (0, 3)},
            {(2, 1), (3, 1), (4, 1)},
            {(5, 4), (5, 5)},
        ):
            self.player.place_ship(cells)
        for cells in (
            {(1, 2), (2, 2), (3, 2), (4, 2)},
            {(5, 0), (5, 1), (5, 2)},
            {(3, 4), (3, 5)},
        ):
            self.enemy.place_ship(cells)

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print("Enemy ships afloat:", self.enemy.ships_afloat())
        print("Ship cells remaining:", len(self.enemy.ships - self.enemy.shots))

    def run(self):
        print("Battleship")
        while True:
            self.show()
            raw = input("> ").strip().lower()
            if raw == "q":
                return
            try:
                r, c = map(int, raw.split(","))
                pos = (r - 1, c - 1)
            except ValueError:
                print("Use row,col.")
                continue
            if not (0 <= pos[0] < Board.SIZE and 0 <= pos[1] < Board.SIZE):
                print("Outside board.")
                continue
            if pos in self.enemy.shots:
                print("Already fired there.")
                continue
            result = self.enemy.fire(pos)
            print(self.RESULT_TEXT[result])
            if self.enemy.all_sunk():
                print("You sank the fleet.")
                return

            ai_pos = self.ai.choose()
            if ai_pos is None:
                print("AI has no cells left to fire at.")
                continue
            print(f"AI fired at {ai_pos[0] + 1},{ai_pos[1] + 1}")
            result = self.player.fire(ai_pos)
            self.ai.record(ai_pos, result in ("hit", "sunk"))
            print("AI " + self.RESULT_TEXT[result])
            if self.player.all_sunk():
                print("The AI sank your fleet.")
                return