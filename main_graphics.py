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
                                width=len(Plateau.matrice[0]) * 50,
                                height=len(Plateau.matrice) * 25,
                                bg="black", bd=0)
        Plateau.canvas.pack()

        Plateau.console = Label(Plateau.main_frame, bg="black", fg="white")
        Plateau.console.pack(side="left")

        control_image = PhotoImage(file="Ressources/gif/control.gif")
        control = Label(Plateau.main_frame, text="Controles", image=control_image)
        control.pack(side="right")

        self.show_surroundings()
        Plateau.root.bind_all("<Key>", self.move)

        Plateau.root.mainloop()

    @staticmethod
    def move(event):
        x = Plateau.player.x
        y = Plateau.player.y
        contour = {"z": {"coords": "{} {}".format(x, y - 1), "tuple": (x, y - 1)},
                   "q": {"coords": "{} {}".format(x - 1, y), "tuple": (x - 1, y)},
                   "s": {"coords": "{} {}".format(x, y + 1), "tuple": (x, y + 1)},
                   "d": {"coords": "{} {}".format(x + 1, y), "tuple": (x + 1, y)}
                   }
        order = event.char
        Plateau.console["text"] = ""

        if order in contour:
            if contour[event.char]["coords"] in Plateau.dict_case_coords:
                Plateau.dict_case_coords[Plateau.player.coords].clear()
                Plateau.player.move(contour[order]["tuple"][0], contour[order]["tuple"][1])
                Plateau.show_surroundings()

        for key in Plateau.player.surrounding_coords:
            if key in Plateau.dict_room_coords:
                Plateau.dict_room_coords[key].contenu.signature()

        if Plateau.player.coords in Plateau.dict_room_coords:
            Plateau.dict_room_coords[Plateau.player.coords].contenu.effect()
            Plateau.show_surroundings()

        if Plateau.player.coords == Plateau.porte.coords:
            Plateau.win()

        Plateau.energy["text"] = "{} pintes d'énergies".format(Plateau.player.energy)

    @staticmethod
    def _gen_basic():
        return [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", "⎾", "⏤", "⏋", " ", "O", " ", " ", " "],
                [" ", " ", " ", "|", " ", "|", " ", "|", " ", " ", " "],
                [" ", "┏", "⏤", "+", "⍈", "+", "⍈", "+", "⏤", "┓", " "],
                [" ", "┊", " ", "|", " ", "|", " ", "|", " ", "┊", " "],
                [" ", "┣", "⏤", "+", "⍈", "+", "⍈", "+", "⏤", "┫", " "],
                [" ", "┊", " ", "|", " ", "|", " ", "|", " ", "┊", " "],
                [" ", "┗", "⏤", "+", "⍈", "+", "⍈", "⏊", "⏤", "┛", " "],
                [" ", " ", " ", "|", " ", "|", " ", " ", " ", " ", " "],
                [" ", " ", " ", "⎿", "x", "⏌", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]

    @staticmethod
    def show_surroundings():
        Plateau.canvas.delete("all")
        if Plateau.player.coords not in Plateau.dict_room_coords:
            for surounding in Plateau.player.surrounding_coords:
                if surounding in Plateau.dict_case_coords:
                    if surounding in Plateau.dict_room_coords:
                        Plateau.dict_case_coords[surounding].draw("gray22")
                    Plateau.dict_case_coords[surounding].draw("gray22")
        Plateau.dict_case_coords[Plateau.player.coords].draw()

    def show_map(self):
        for case in Plateau.dict_case_coords:
            Plateau.dict_case_coords[case].draw()

    @staticmethod
    def _gen_random():
        pass

    def __repr__(self):
        return "\n".join(["".join(line) for line in Plateau.matrice])

    @staticmethod
    def win():
        Affiche("Ressources/gif/stairway-to-heaven.gif", "Félicitations, vous êtes arrivés à la porte du Paradis !")
        Plateau.root.bind_all("<Key>", exit)

    @staticmethod
    def loose():
        Affiche("Ressources/gif/ghost_buster.gif", "Tu n'as plus d'énergie et tu erreras désormais à jamais dans les limbes")
        Plateau.root.bind_all("<Key>", exit)


class Case:
    def __init__(self, x, y, symbole):
        self.x = x
        self.y = y
        self.coords = "{} {}".format(x, y)
        self.type = symbole
        self.color = "white"

    def draw(self, color="white"):
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
        self.color = color
        dict_drawings[self.type]()

    def base_room(self):
        x = self.x * 50 + 25
        y = self.y * 25 + 12.5
        for x_sign in (1, -1):
            for y_sign in (1, -1):
                Plateau.canvas.create_polygon(x + x_sign * 3, y + y_sign * 17,
                                              x + x_sign * 3, y + y_sign * 15,
                                              x + x_sign * 15, y + y_sign * 15,
                                              x + x_sign * 15, y + y_sign * 3,
                                              x + x_sign * 17, y + y_sign * 3,
                                              x + x_sign * 17, y + y_sign * 17,
                                              fill=self.color, tags=self.coords)

    def h_wall(self, top: bool):
        diff = 32 if top else 0
        x = self.x * 50
        y = self.y * 25 - 12.5
        Plateau.canvas.create_polygon(x + 22, y + 42 - diff,
                                      x + 28, y + 42 - diff,
                                      x + 28, y + 40 - diff,
                                      x + 22, y + 40 - diff,
                                      fill=self.color, tags=self.coords)

    def v_wall(self, left: bool):
        diff = 32 if left else 0
        x = self.x * 50
        y = self.y * 25 - 12.5
        Plateau.canvas.create_polygon(x + 42 - diff, y + 28,
                                      x + 42 - diff, y + 22,
                                      x + 40 - diff, y + 22,
                                      x + 40 - diff, y + 28,
                                      fill=self.color, tags=self.coords)

    def h_door(self, top: bool):
        diff = -1 if top else 1

        x = self.x * 50
        y = self.y * 25 + 12.5
        Plateau.canvas.create_polygon(x + 20, y + diff * 25,
                                      x + 20, y + diff * 17,
                                      x + 30, y + diff * 17,
                                      x + 30, y + diff * 25,
                                      x + 28, y + diff * 25,
                                      x + 28, y + diff * 18,
                                      x + 22, y + diff * 18,
                                      x + 22, y + diff * 25,
                                      fill=self.color, tags=self.coords)

    def v_door(self, left: bool):
        diff = -1 if left else 1

        x = self.x * 50
        y = self.y * 25 - 12.5
        Plateau.canvas.create_polygon(x + 25 + diff * 25, y + 20,
                                      x + 25 + diff * 17, y + 20,
                                      x + 25 + diff * 17, y + 30,
                                      x + 25 + diff * 25, y + 30,
                                      x + 25 + diff * 25, y + 28,
                                      x + 25 + diff * 18, y + 28,
                                      x + 25 + diff * 18, y + 22,
                                      x + 25 + diff * 25, y + 22,
                                      fill=self.color, tags=self.coords)

    def t_h_room(self):
        self.base_room()
        self.h_wall(top=True)
        self.h_wall(top=False)
        self.v_door(left=False)
        self.v_door(left=True)

    def reception(self):
        self.t_h_room()

        Plateau.canvas.create_text(self.x * 50 + 25, self.y * 25 + 12.5, text="R", fill=self.color, tags=self.coords)

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

    def v_corridor(self):
        x = self.x * 50 + 25
        y = self.y * 25 + 6.25
        for diff in [1, -1]:
            Plateau.canvas.create_polygon(x + diff * 5, y + 12.5,
                                          x + diff * 5, y + 00,
                                          x + diff * 3, y + 00,
                                          x + diff * 3, y + 12.5,
                                          fill=self.color, tags=self.coords)

    def h_corridor(self):
        x = self.x * 50
        y = self.y * 25 + 12.5
        for diff in [1, -1]:
            Plateau.canvas.create_polygon(x + 50, y + diff * 5,
                                          x + 00, y + diff * 5,
                                          x + 00, y + diff * 3,
                                          x + 50, y + diff * 3,
                                          fill=self.color, tags=self.coords)

    def corner_corridor(self, left: bool, top: bool):
        l = 1 if left else -1
        t = 1 if top else -1

        x = self.x * 50 + 25
        y = self.y * 25 + 12.5
        Plateau.canvas.create_polygon(x + l * 3, y + t * 25,
                                      x + l * 5, y + t * 25,
                                      x + l * 5, y + t * 5,
                                      x + l * 25, y + t * 5,
                                      x + l * 25, y + t * 3,
                                      x + l * 3, y + t * 3,
                                      fill=self.color, tags=self.coords)
        Plateau.canvas.create_polygon(x + l * -3, y + t * 25,
                                      x + l * -5, y + t * 25,
                                      x + l * -5, y + t * -5,
                                      x + l * 25, y + t * -5,
                                      x + l * 25, y + t * -3,
                                      x + l * -3, y + t * -3,
                                      fill=self.color, tags=self.coords)

    def c_bl_corridor(self):
        self.corner_corridor(top=False, left=True)

    def c_tl_corridor(self):
        self.corner_corridor(top=True, left=True)

    def c_br_corridor(self):
        self.corner_corridor(top=False, left=False)

    def c_tr_corridor(self):
        self.corner_corridor(top=True, left=False)

    def cross_section(self):
        x = self.x * 50 + 25
        y = self.y * 25 + 12.5
        for x_sign in (1, -1):
            for y_sign in (1, -1):
                Plateau.canvas.create_polygon(x + x_sign * 3, y + y_sign * 25,
                                              x + x_sign * 3, y + y_sign * 3,
                                              x + x_sign * 25, y + y_sign * 3,
                                              x + x_sign * 25, y + y_sign * 5,
                                              x + x_sign * 5, y + y_sign * 5,
                                              x + x_sign * 5, y + y_sign * 25,
                                              fill=self.color, tags=self.coords)

    def tri_b_corridor(self):
        x = self.x * 50 + 25
        y = self.y * 25 + 12.5
        Plateau.canvas.create_polygon(x + 25, y + 5,
                                      x - 25, y + 5,
                                      x - 25, y + 3,
                                      x + 25, y + 3,
                                      fill=self.color, tags=self.coords)
        for sign in [1, -1]:
            Plateau.canvas.create_polygon(x + sign * 3, y - 25,
                                          x + sign * 3, y - 3,
                                          x + sign * 25, y - 3,
                                          x + sign * 25, y - 5,
                                          x + sign * 5, y - 5,
                                          x + sign * 5, y - 25,
                                          fill=self.color, tags=self.coords)

    def porte(self):
        self.base_room()
        self.h_wall(top=True)
        self.v_wall(left=True)
        self.v_wall(left=False)
        self.h_door(top=False)

    def change_color(self, new_color):
        Plateau.canvas.itemconfig(self.coords, fill=new_color)

    def clear(self):
        Plateau.canvas.delete(self.coords)


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
        Plateau.console["text"] += "Cling cling\n"

    def effect(self):
        Affiche("Ressources/gif/majordome.gif", "Retourne donc à la Réception mon très cher Gasper !")
        Plateau.player.move(Plateau.reception.x, Plateau.reception.y)

    def __repr__(self):
        return "LandLord"


class MadScientist(Enemy):
    def signature(self):
        Plateau.console["text"] += "Mwah ah ah !\n"

    def effect(self):
        Affiche("Ressources/gif/Mad_Scientist.gif", "Tu es téléporté dans une salle aléatoire et tu perd 1 énergie")
        Plateau.player.energy -= 1
        chosen_case = Plateau.dict_case_coords[rd.choice(list(Plateau.dict_case_coords))]
        Plateau.player.move(chosen_case.x, chosen_case.y)

    def __repr__(self):
        return "MadScientist"


class Bibendum(Enemy):
    def signature(self):
        Plateau.console["text"] += "Ça sent bon par ici !\n"

    def effect(self):
        Affiche("Ressources/gif/bibendum.gif", "Vous êtes paralysés et perdez 2 énergies")
        Plateau.player.energy -= 2

    def __repr__(self):
        return "Bibbendum"


class Energy(Contenu):
    def __init__(self, amount):
        self.amount = amount

    def __repr__(self):
        return "{} pintes vertes d'énergie".format(self.amount)

    def effect(self):
        if self.amount:
            Affiche("Ressources/gif/beer.gif", "Vous avez trouver {} pintes d'ectoplasme vert".format(self.amount))
            Plateau.player.energy += self.amount
            self.amount = 0


class Affiche:
    def __init__(self, file, text):
        self.affiche = Toplevel(Plateau.root)
        self.frame = Frame(self.affiche, bg="black")
        self.frame.pack()
        self.image = PhotoImage(file=file)

        self.image_label = Label(self.frame, image=self.image)
        self.image_label.pack()
        self.label = Label(self.frame, bg="black", fg="white", text=text, font=("Helvetica", "16") )
        self.label.pack()
        Plateau.root.bind_all("<Key>", self._close)

    def _close(self, event):
        self.affiche.destroy()
        Plateau.root.bind_all("<Key>", Plateau.move)
        if Plateau.player.energy <= 0:
            Plateau.loose()


class Player:

    def __init__(self):
        self.x = Plateau.reception.x
        self.y = Plateau.reception.y
        self.energy = 3

    def move(self, x=None, y=None):
        self.x = x if x else self.x
        self.y = y if y else self.y

    @property
    def coords(self):
        return "{} {}".format(self.x, self.y)

    @property
    def surrounding_coords(self):
        return ["{} {}".format(self.x, self.y - 1),
                "{} {}".format(self.x - 1, self.y),
                "{} {}".format(self.x, self.y + 1),
                "{} {}".format(self.x + 1, self.y)]


if __name__ == "__main__":
    Plateau()
