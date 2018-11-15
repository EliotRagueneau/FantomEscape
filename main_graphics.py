from tkinter import *
import random as rd


class Plateau:
    matrice = reception = porte = player = energy_frame = None
    root = main_frame = console = control_image = control = None
    dict_room_coords = {}
    dict_case_coords = {}

    # canvas = Canvas()

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
                                width=(len(Plateau.matrice[0])) * 50,
                                height=(len(Plateau.matrice)) * 50,
                                bg="black", bd=0)
        Plateau.canvas.pack()

        Plateau.console = Label(Plateau.main_frame)
        Plateau.console.pack(side="left")

        Plateau.control_image = PhotoImage(file="control.gif")
        Plateau.control = Label(Plateau.main_frame, text="Controles", image=Plateau.control_image)
        Plateau.control.pack(side="right")
        for case in Plateau.dict_case_coords:
            Plateau.dict_case_coords[case].draw()
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
            if contour[key]["coords"] in Plateau.dict_case_coords:
                keys[key] = contour[key]["tuple"]
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
        dict_drawings = {"⍈": self.t_h_room,

                         "x": self.reception,

                         "┏": self.c_tl_room,

                         "┣": self.tri_l_room,

                         "┗": self.c_bl_room,

                         "┓": self.c_tr_room,

                         "┫": self.tri_r_room,

                         "┛": self.c_br_room,

                         "┊": self.v_corridor,

                         "|": self.v_corridor,

                         "⎿": self.c_bl_corridor,

                         "⏌": self.c_br_corridor,

                         "+": self.cross_section,

                         "⎾": self.c_tl_corridor,

                         "⏤": self.h_corridor,

                         "⏋": self.c_tr_corridor,

                         "⏊": self.tri_b_corridor,

                         "O": self.porte

                         }
        dict_drawings[self.type]()

    def base_room(self):
        x = self.x * 50
        y = self.y * 50
        Plateau.canvas.create_polygon(x + 22, y + 42,
                                      x + 22, y + 40,
                                      x + 10, y + 40,
                                      x + 10, y + 28,
                                      x + 8, y + 28,
                                      x + 8, y + 42,
                                      fill="white")

        Plateau.canvas.create_polygon(x + 22, y + 8,
                                      x + 22, y + 10,
                                      x + 10, y + 10,
                                      x + 10, y + 22,
                                      x + 8, y + 22,
                                      x + 8, y + 8,
                                      fill="white")
        Plateau.canvas.create_polygon(x + 28, y + 42,
                                      x + 42, y + 42,
                                      x + 42, y + 28,
                                      x + 40, y + 28,
                                      x + 40, y + 40,
                                      x + 28, y + 40,
                                      fill="white")
        Plateau.canvas.create_polygon(x + 28, y + 8,
                                      x + 28, y + 10,
                                      x + 40, y + 10,
                                      x + 40, y + 22,
                                      x + 42, y + 22,
                                      x + 42, y + 8,
                                      fill="white")

    def h_wall(self, top: bool):
        diff = 32 if top else 0
        x = self.x * 50
        y = self.y * 50
        Plateau.canvas.create_polygon(x + 22, y + 42 - diff,
                                      x + 28, y + 42 - diff,
                                      x + 28, y + 40 - diff,
                                      x + 22, y + 40 - diff,
                                      fill="white")

    def v_wall(self, left: bool):
        diff = 32 if left else 0
        x = self.x * 50
        y = self.y * 50
        Plateau.canvas.create_polygon(x + 42 - diff, y + 28,
                                      x + 42 - diff, y + 22,
                                      x + 40 - diff, y + 22,
                                      x + 40 - diff, y + 28,
                                      fill="white")

    def h_door(self, top: bool):
        diff = -1 if top else 1

        x = self.x * 50
        y = self.y * 50
        Plateau.canvas.create_polygon(x + 20, y + 25 + diff * 25,
                                      x + 20, y + 25 + diff * 17,
                                      x + 30, y + 25 + diff * 17,
                                      x + 30, y + 25 + diff * 25,
                                      x + 28, y + 25 + diff * 25,
                                      x + 28, y + 25 + diff * 18,
                                      x + 22, y + 25 + diff * 18,
                                      x + 22, y + 25 + diff * 25,
                                      fill="white")

    def v_door(self, left: bool):
        diff = -1 if left else 1

        x = self.x * 50
        y = self.y * 50
        Plateau.canvas.create_polygon(x + 25 + diff * 25, y + 20,
                                      x + 25 + diff * 17, y + 20,
                                      x + 25 + diff * 17, y + 30,
                                      x + 25 + diff * 25, y + 30,
                                      x + 25 + diff * 25, y + 28,
                                      x + 25 + diff * 18, y + 28,
                                      x + 25 + diff * 18, y + 22,
                                      x + 25 + diff * 25, y + 22,
                                      fill="white")

    def t_h_room(self):
        self.base_room()
        self.h_wall(top=True)
        self.h_wall(top=False)
        self.v_door(left=False)
        self.v_door(left=True)

    def reception(self):
        self.t_h_room()

        Plateau.canvas.create_text(self.x * 50 + 25, self.y * 50 + 25, text="R", fill="white")

    def c_tl_room(self):
        self.base_room()
        self.h_wall(top=True)
        self.v_wall(left=True)
        self.h_door(top=False)
        self.v_door(left=False)

    def c_bl_room(self):
        self.base_room()
        self.h_wall(top=False)
        self.v_wall(left=True)
        self.h_door(top=True)
        self.v_door(left=False)

    def c_br_room(self):
        self.base_room()
        self.h_wall(top=False)
        self.v_wall(left=False)
        self.h_door(top=True)
        self.v_door(left=True)

    def c_tr_room(self):
        self.base_room()
        self.h_wall(top=True)
        self.v_wall(left=False)
        self.h_door(top=False)
        self.v_door(left=True)

    def tri_l_room(self):
        self.base_room()
        self.v_wall(left=True)
        self.h_door(top=True)
        self.h_door(top=False)
        self.v_door(left=False)

    def tri_r_room(self):
        self.base_room()
        self.v_wall(left=False)
        self.h_door(top=True)
        self.h_door(top=False)
        self.v_door(left=True)

    def tri_b_corridor(self):
        pass

    def v_corridor(self):
        x = self.x * 50
        y = self.y * 50
        Plateau.canvas.create_polygon(x + 20, y + 50,
                                      x + 20, y + 00,
                                      x + 22, y + 00,
                                      x + 22, y + 50,
                                      fill="white")
        Plateau.canvas.create_polygon(x + 30, y + 50,
                                      x + 30, y + 00,
                                      x + 28, y + 00,
                                      x + 28, y + 50,
                                      fill="white")

    def h_corridor(self):
        x = self.x * 50
        y = self.y * 50
        Plateau.canvas.create_polygon(x + 50, y + 20,
                                      x + 0, y + 22,
                                      x + 0, y + 20,
                                      x + 50, y + 22,
                                      fill="white")
        # Plateau.canvas.create_polygon(x + 50, y + 30,
        #                               x + 00, y + 30,
        #                               x + 00, y + 28,
        #                               x + 50, y + 28,
        #                               fill="white")

    def corner_corridor(self, left: bool, top: bool):
        l = 1 if left else -1
        t = 1 if top else -1

        x = self.x * 50 + 25
        y = self.y * 50 + 25
        Plateau.canvas.create_polygon(x + l * 3, y + t * 25,
                                      x + l * 5, y + t * 25,
                                      x + l * 5, y + t * 5,
                                      x + l * 25, y + t * 5,
                                      x + l * 25, y + t * 3,
                                      x + l * 3, y + t * 3,
                                      fill="white")
        Plateau.canvas.create_polygon(x + l * -3, y + t * 25,
                                      x + l * -5, y + t * 25,
                                      x + l * -5, y + t * -5,
                                      x + l * 25, y + t * -5,
                                      x + l * 25, y + t * -3,
                                      x + l * -3, y + t * -3,
                                      fill="white")

    def c_bl_corridor(self):
        self.corner_corridor(top=False, left=True)

    def c_tl_corridor(self):
        self.corner_corridor(top=True, left=True)

    def c_br_corridor(self):
        self.corner_corridor(top=False, left=False)

    def c_tr_corridor(self):
        self.corner_corridor(top=True, left=False)

    def cross_section(self):
        x = self.x * 50
        y = self.y * 50
        Plateau.canvas.create_polygon(x + 20, y + 50,
                                      x + 20, y + 30,
                                      x + 00, y + 30,
                                      x + 00, y + 28,
                                      x + 22, y + 28,
                                      x + 22, y + 50,
                                      fill="white")

        Plateau.canvas.create_polygon(x + 00, y + 22,
                                      x + 00, y + 20,
                                      x + 20, y + 20,
                                      x + 20, y + 00,
                                      x + 22, y + 00,
                                      x + 22, y + 22,
                                      fill="white")

        Plateau.canvas.create_polygon(x + 30, y + 50,
                                      x + 30, y + 30,
                                      x + 50, y + 30,
                                      x + 50, y + 28,
                                      x + 28, y + 28,
                                      x + 28, y + 50,
                                      fill="white")

        Plateau.canvas.create_polygon(x + 50, y + 22,
                                      x + 50, y + 20,
                                      x + 30, y + 20,
                                      x + 30, y + 00,
                                      x + 28, y + 00,
                                      x + 28, y + 22,

                                      fill="white")

    def porte(self):
        self.base_room()
        self.h_wall(top=True)
        self.v_wall(left=True)
        self.v_wall(left=False)
        self.h_door(top=False)


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
