class Plateau:
    def __init__(self, basic: bool = True):
        self.matrice = self._gen_basic() if basic else self._gen_random()
        self.list_room = []

    @staticmethod
    def _gen_basic():
        return [[" ", "r", "⏤", "˥", " ", "O", " "],
                [" ", "|", " ", "|", " ", "|", " "],
                ["o", "+", "o", "+", "o", "+", "o"],
                ["|", "|", " ", "|", " ", "|", "|"],
                ["o", "+", "o", "+", "o", "+", "o"],
                ["|", "|", " ", "|", " ", "|", "|"],
                ["o", "+", "o", "+", "o", "⏊", "o"],
                [" ", "|", " ", "|", " ", " ", " "],
                [" ", "⎿", "o", "⏌", " ", " ", " "]]

    @staticmethod
    def _gen_random():
        pass

    def __repr__(self):
        return "\n".join(["".join(line) for line in self.matrice])


class Room:
    def __init__(self, x, y, contenu):
        self.x = x
        self.y = y
        self.contenu = contenu


print(Plateau())
