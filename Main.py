import random as rd


class Plateau:
    matrice = reception = player = None
    list_case, list_room = [], []

    def __init__(self, basic: bool = True):
        Plateau.matrice = Plateau._gen_basic() if basic else Plateau._gen_random()
        Plateau.list_room = []
        for y in range(len(Plateau.matrice)):
            for x in range(len(Plateau.matrice[y])):
                current_case = Plateau.matrice[y][x]
                if current_case not in [" ", "O"]:
                    Plateau.list_case.append(Case(x, y))
                if current_case == "o":
                    Plateau.list_room.append(Room(x, y))
                elif current_case == "x":
                    Plateau.reception = Room(x, y, label="Reception")
                elif current_case == "O":
                    Plateau.reception = Room(x, y, label="Porte")

        total_pinte = 5
        liste_pinte = []
        while total_pinte != 0:
            max_pinte_per_room = 3 if total_pinte >= 3 else total_pinte
            new_amount = rd.randint(1, max_pinte_per_room)
            liste_pinte.append(new_amount)
            total_pinte -= new_amount

        filled_rooms = rd.sample(Plateau.list_room, 5 + len(liste_pinte))
        filled_rooms[0].contenu = LandLord()
        filled_rooms[1].contenu = MadScientist()
        for enemy_room in filled_rooms[2:5]:
            enemy_room.contenu = Bibbendum()

        n = 0
        for pinte_room in filled_rooms[5:]:
            pinte_room.contenu = Energy(liste_pinte[n])
            n += 1

        for room in Plateau.list_room:
            print(room.x, room.y, room.contenu)

        Plateau.joueur = Player()

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
                [" ", "⎿", "x", "⏌", " ", " ", " "]]

    @staticmethod
    def _gen_random():
        pass

    def __repr__(self):
        return "\n".join(["".join(line) for line in Plateau.matrice])


class Case:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Room(Case):
    def __init__(self, x, y, contenu=None, label: str = None):
        super(Room, self).__init__(x, y)
        self.contenu = contenu
        self.label = label


class Contenu:
    pass


class Enemy(Contenu):
    def signature(self):
        pass

    def effect(self):
        pass


class LandLord(Enemy):
    def signature(self):
        print("Cling Cling !")

    def effect(self):
        Plateau.player.move(Plateau.reception.x, Plateau.reception.y)

    def __repr__(self):
        return "LandLord"


class MadScientist(Enemy):
    def signature(self):
        print("Mwah ah ah ah !")

    def effect(self):
        print("Oh non ! Un scientifique fou se tient devant vous !!!")
        print("Dans sa fureur, il vous téléporte dans une salle aléatoire !")
        Plateau.player.energy -= 1
        chosen_case = rd.choice(Plateau.list_case)
        Plateau.player.move(chosen_case.x, chosen_case.y)

        print("Le bougre en a profiter pour vous subtiliser une pinte d'énergie ...")

    def __repr__(self):
        return "MadScientist"


class Bibbendum(Enemy):
    def signature(self):
        print("Ça sent bon par ici !")

    def effect(self):
        print("Vous êtes paralysés, vous perdez 2 d'énergie")
        Plateau.player.energy -= 2

    def __repr__(self):
        return "Bibbendum"


class Energy(Contenu):
    def __init__(self, amount):
        self.amount = amount

    def __repr__(self):
        return "{} pintes vertes d'énergie".format(self.amount)


class Player:

    def __init__(self):
        self.x = Plateau.reception.x
        self.y = Plateau.reception.y
        self.energy = 3

    def move(self, x, y):
        self.x = x
        self.y = y


if __name__ == "__main__":
    print(Plateau())
    print(Player().x)
