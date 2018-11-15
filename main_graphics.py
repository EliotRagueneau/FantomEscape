from tkinter import *
import random as rd


class Plateau:
    matrice = reception = porte = player =  energy_frame = None
    root = main_frame = console = control_image = control = None
    dict_room_coords = {}
    dict_case_coords = {}
    canvas = Canvas()

    def __init__(self, basic: bool = True):
        Plateau.matrice = Plateau._gen_basic() if basic else Plateau._gen_random()

        for y in range(len(Plateau.matrice)):
            for x in range(len(Plateau.matrice[y])):
                current_case = Plateau.matrice[y][x]
                if current_case != " ":
                    Plateau.dict_case_coords["{} {}".format(x, y)] = Case(x, y, current_case)

                if current_case in ["┏", "⍈", "┏", "┣", "┗", "┓", "┫", "┛"]:
                    Plateau.dict_room_coords["{} {}".format(x, y)] = Room(x, y, current_case)

                if current_case == "x":
                    Plateau.reception = Room(x, y, current_case)

                elif current_case == "O":
                    Plateau.porte = Room(x, y, current_case)

        total_pinte = 5
        liste_pinte = []
        while total_pinte != 0:
            new_amount = rd.randint(1, 3 if total_pinte >= 3 else total_pinte)
            liste_pinte.append(new_amount)
            total_pinte -= new_amount

        list_filled_room_coords = rd.sample(list(Plateau.dict_room_coords), 5 + len(liste_pinte))

        Plateau.dict_room_coords[list_filled_room_coords[0]].contenu = LandLord()

        Plateau.dict_room_coords[list_filled_room_coords[1]].contenu = MadScientist()

        for bibendum_coords in list_filled_room_coords[2:5]:
            Plateau.dict_room_coords[bibendum_coords].contenu = Bibendum()

        n = 0
        for pinte_room in list_filled_room_coords[5:]:
            Plateau.dict_room_coords[pinte_room].contenu = Energy(liste_pinte[n])
            n += 1

        Plateau.player = Player()

        # ====== GUI =======

        Plateau.root = Tk()
        Plateau.root.title("Fantom Escape")

        Plateau.main_frame = Frame(Plateau.root, bg="black", bd=0, height=15, width=50)
        Plateau.main_frame.pack()

        Plateau.energy_frame = Frame(Plateau.main_frame, bg="gray50")
        Plateau.energy_frame.pack()

        Plateau.energy = Label(Plateau.energy_frame, bg="black", fg="white",
                               text="{} pintes d'énergies".format(Plateau.player.energy))
        Plateau.energy.pack()

        Plateau.canvas = Canvas(Plateau.main_frame,
                                width=len(Plateau.matrice) * 50,
                                height=len(Plateau.matrice[0]) * 50,
                                bg="black", bd=0)
        Plateau.canvas.pack()

        Plateau.console = Label(Plateau.main_frame)
        Plateau.console.pack(side="left")

        Plateau.control_image = PhotoImage(file="control.gif")
        Plateau.control = Label(Plateau.main_frame, image=Plateau.control_image)
        Plateau.control.pack(side="right")
        Plateau.root.mainloop()

    @staticmethod
    def _gen_basic():
        return [[" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", "⎾", "⏤", "⏋", " ", "O", " ", " "],
                [" ", " ", "|", " ", "|", " ", "|", " ", " "],
                [" ", "┏", "+", "⍈", "+", "⍈", "+", "┓", " "],
                [" ", "┊", "|", " ", "|", " ", "|", "┊", " "],
                [" ", "┣", "+", "⍈", "+", "⍈", "+", "┫", " "],
                [" ", "┊", "|", " ", "|", " ", "|", "┊", " "],
                [" ", "┗", "+", "⍈", "+", "⍈", "⏊", "┛", " "],
                [" ", " ", "|", " ", "|", " ", " ", " ", " "],
                [" ", " ", "⎿", "x", "⏌", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " "]]

    @staticmethod
    def _gen_random():
        pass

    def __repr__(self):
        return "\n".join(["".join(line) for line in Plateau.matrice])

    def turn(self):
        x = Plateau.player.x
        y = Plateau.player.y
        keys = {}

        contour = {"z": {"coords": "{} {}".format(x, y - 1), "tuple": (x, y - 1)},
                   "q": {"coords": "{} {}".format(x - 1, y), "tuple": (x - 1, y)},
                   "s": {"coords": "{} {}".format(x, y + 1), "tuple": (x, y + 1)},
                   "d": {"coords": "{} {}".format(x + 1, y), "tuple": (x + 1, y)}
                   }

        for key in contour:
            if contour[key]["coords"] in Plateau.dict_room_coords:
                Plateau.dict_room_coords[contour[key]["coords"]].contenu.signature()

        print(Plateau.dict_case_coords[Plateau.player.coords])
        order = input()

        if order in keys:
            Plateau.player.move(keys[order][0], keys[order][1])

            if Plateau.player.coords in Plateau.dict_room_coords:
                Plateau.dict_room_coords[Plateau.player.coords].contenu.effect()

                if Plateau.player.energy <= 0:
                    self.loose()

            if Plateau.player.coords == Plateau.porte.coords:
                self.win()

            self.turn()

        else:
            print("Tu ne peut pas aller par là")
            self.turn()

    @staticmethod
    def win():
        pass

    @staticmethod
    def loose():
        pass


class Case:
    def __init__(self, x, y, symbole):
        self.x = x
        self.y = y
        self.coords = "{} {}".format(x, y)
        self.type = symbole

    def draw(self):
        dict_drawings = {"⍈": Case.t_h_room,

                         "x": Case.reception,

                         "┏": Case.c_tl_room,

                         "┣": Case.tri_l_room,

                         "┗": Case.c_bl_room,

                         "┓": Case.c_tr_room,

                         "┫": Case.tri_r_room,

                         "┛": Case.c_br_room,

                         "┊": Case.two_doors_v_corridor,

                         "|": Case.v_corridor,

                         "⎿": Case.c_bl_corridor,

                         "⏌": Case.c_br_corridor,

                         "+": Case.cross_section,

                         "⎾": Case.c_tl_corridor,

                         "⏤": Case.h_corridor,

                         "⏋": Case.c_tr_corridor,

                         "⏊": Case.tri_b_room

                         }
        dict_drawings[self.type]()

    def t_h_room(self):
        Plateau.canvas.create_polygon()

    def reception(self):
        pass

    def c_tl_room(self):
        pass

    def c_bl_room(self):
        pass

    def c_br_room(self):
        pass

    def c_tr_room(self):
        pass

    def tri_l_room(self):
        pass

    def tri_r_room(self):
        pass

    def tri_b_room(self):
        pass

    def two_doors_v_corridor(self):
        pass

    def v_corridor(self):
        pass

    def h_corridor(self):
        pass

    def c_bl_corridor(self):
        pass

    def c_br_corridor(self):
        pass

    def c_tl_corridor(self):
        pass

    def c_tr_corridor(self):
        pass

    def cross_section(self):
        pass


class Contenu:
    def __repr__(self):
        return "Salle vide"

    def effect(self):
        pass

    def signature(self):
        pass


class Room(Case):
    def __init__(self, x, y, symbole, contenu=Contenu()):
        super(Room, self).__init__(x, y, symbole)
        self.contenu = contenu
        Plateau.dict_case_coords["{} {}".format(x, y)] = self


class Enemy(Contenu):
    pass


class LandLord(Enemy):
    def signature(self):
        pass

    def effect(self):
        Plateau.player.move(Plateau.reception.x, Plateau.reception.y)

    def __repr__(self):
        return "LandLord"


class MadScientist(Enemy):
    def signature(self):
        print("Mwah ah ah ah !")

    def effect(self):
        Plateau.player.energy -= 1
        chosen_case = Plateau.dict_case_coords[rd.choice(list(Plateau.dict_case_coords))]
        Plateau.player.move(chosen_case.x, chosen_case.y)

    def __repr__(self):
        return "MadScientist"


class Bibendum(Enemy):
    def signature(self):
        pass

    def effect(self):
        Plateau.player.energy -= 2

    def __repr__(self):
        return "Bibbendum"


class Energy(Contenu):
    def __init__(self, amount):
        self.amount = amount

    def __repr__(self):
        return "{} pintes vertes d'énergie".format(self.amount)

    def effect(self):
        print("Vous avez trouver {} pintes d'ectoplasme vert".format(self.amount))
        Plateau.player.energy += self.amount
        self.amount = 0


class Player:

    def __init__(self):
        self.x = Plateau.reception.x
        self.y = Plateau.reception.y
        self.coords = "{} {}".format(self.x, self.y)
        self.energy = 3

    def move(self, x, y):
        self.x = x
        self.y = y
        self.coords = "{} {}".format(self.x, self.y)


if __name__ == "__main__":
    print(Plateau())
