import random as rd
import illustration


class Game:
    """Classe regroupant l'ensemble des fonctionnalités du jeu
        Contrôles:
            z  ==> Aller en haut
            q  ==> Aller à gauche
            s  ==> Aller en bas
            d  ==> Aller à droite """

    matrice = reception = porte = player = None
    dict_room_coords = {}
    dict_case_coords = {}

    def __init__(self, basic: bool = True):
        """ Cette fonction initialise le plateau le jeu
            Elle permet également de choisir la generation basique ou random """

        print(" \n Contrôles: \n \t z ou 8 ==> Aller en haut \n \t q ou 4 ==> Aller à gauche \n \t s ou 2 ==> Aller en bas \n \t d ou 6 ==> Aller à droite \n ")

        Game.matrice = Game._gen_basic() if basic else Game._gen_random()  # Récupère la matrice de jeu

        # Récupération des informations contenus dans la matrice #

        for y in range(len(Game.matrice)):  # Pour chaque coordonnées sur la matrice
            for x in range(len(Game.matrice[y])):

                current_case = Game.matrice[y][x]  # On récupère la case de la matrice définie par ses coordonnées

                if current_case != " ":  # Si la case n'est pas vide
                    Game.dict_case_coords["{} {}".format(x, y)] = Case(x, y, current_case)  # Alors c'est une case

                if current_case in ["┏", "⍈", "┏", "┣", "┗", "┓", "┫", "┛"]:  # Si la case fait partie de cette liste
                    Game.dict_room_coords["{} {}".format(x, y)] = Room(x, y, current_case)  # Alors c'est une salle

                if current_case == "x":  # Si la case correspond à la réception
                    Game.reception = Room(x, y, current_case)  # On sauvegarde sa position

                elif current_case == "O":  # Si la case est la porte du paradis
                    Game.porte = Room(x, y, current_case)  # On sauvegarde sa position

        # Distribution des pintes d'énergies #

        total_pinte = 5
        liste_pinte = []
        while total_pinte != 0:
            new_amount = rd.randint(1, 3 if total_pinte >= 3 else total_pinte)  # Entre 1 et 3 pintes par salle maximum
            liste_pinte.append(new_amount)
            total_pinte -= new_amount

        # Choix aléatoire des salles contenant quelque chose #

        list_filled_room_coords = rd.sample(list(Game.dict_room_coords), 5 + len(liste_pinte))

        Game.dict_room_coords[list_filled_room_coords[0]].contenu = LandLord()

        Game.dict_room_coords[list_filled_room_coords[1]].contenu = MadScientist()

        for enemy_room in list_filled_room_coords[2:5]:  # Localisation des 3 Bibendum
            Game.dict_room_coords[enemy_room].contenu = Bibendum()

        n = 0
        for pinte_room in list_filled_room_coords[5:]:
            Game.dict_room_coords[pinte_room].contenu = Energy(liste_pinte[n])
            n += 1

        # Fin de l'initialisation #
        Game.player = Player()  # Placage du joueur à la réception
        self.turn()  # Premier tour de jeu

    @staticmethod
    def _gen_basic():
        """Génère la matrice map basique telle que montrée dans le sujet"""

        return [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", "⌜", "─", "⌝", " ", "O", " ", " ", " "],
                [" ", " ", " ", "|", " ", "|", " ", "|", " ", " ", " "],
                [" ", "┏", "─", "+", "⍈", "+", "⍈", "+", "─", "┓", " "],
                [" ", "┊", " ", "|", " ", "|", " ", "|", " ", "┊", " "],
                [" ", "┣", "─", "+", "⍈", "+", "⍈", "+", "─", "┫", " "],
                [" ", "┊", " ", "|", " ", "|", " ", "|", " ", "┊", " "],
                [" ", "┗", "─", "+", "⍈", "+", "⍈", "⊥", "─", "┛", " "],
                [" ", " ", " ", "|", " ", "|", " ", " ", " ", " ", " "],
                [" ", " ", " ", "⌞", "x", "⌟", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]

    @staticmethod
    def _gen_random():
        """ Génère la matrice map aléatoirement """
        pass

    def turn(self):
        """Définit le déroulement de chaque tour du jeu"""
        # Récupération des coordonnées du joueur
        x = Game.player.x
        y = Game.player.y

        keys = {}  # Initialise le dictionnaire contenant les mouvements possibles du joueur à chaque tour

        contour = {"{} {}".format(x, y - 1): {"new_coords": (x, y - 1), "order": ("z", "8")},
                   "{} {}".format(x - 1, y): {"new_coords": (x - 1, y), "order": ("q", "4")},
                   "{} {}".format(x, y + 1): {"new_coords": (x, y + 1), "order": ("s", "2")},
                   "{} {}".format(x + 1, y): {"new_coords": (x + 1, y), "order": ("d", "6")}
                   }

        for contour_coords in contour:

            if contour_coords in Game.dict_case_coords:  # Si ce qui se trouve autour du joueur est une case
                for order in contour[contour_coords]["order"]:
                    keys[order] = contour[contour_coords]["new_coords"]  # Alors le joueur peut s'y déplacer

                if contour_coords in Game.dict_room_coords:  # Et si c'est une salle
                    Game.dict_room_coords[contour_coords].contenu.signature()  # On exécute la signature de son contenu

        print(Game.dict_case_coords[Game.player.coords])  # Affiche la salle où se trouve le joueur

        order = input()  # Récupère l'ordre de mouvement du joueur

        if order in keys:  # Si l'ordre du joueur se trouve bien dans les possibilités définies plus tôt
            Game.player.move(keys[order][0], keys[order][1])  # Le joueur se déplace vers la direction souhaitée

            if Game.player.coords in Game.dict_room_coords:  # Si le joueur arrive dans une salle
                Game.dict_room_coords[Game.player.coords].contenu.effect()  # On execute l'effet de la salle

                if Game.player.energy <= 0:  # Si l'énergie du joueur est tombée sous 0
                    self.loose()  # Le joueur perd

            if Game.player.coords == Game.porte.coords:  # Si le joueur est arrivé à la porte du paradis
                self.win()  # Le joueur gagne

            self.turn()  # Si le joueur ne gagne ni ne perd, alors il commence un nouveau tour

        else:  # Si l'ordre donnée par le joueur ne fait pas parti des possibilités
            print("Tu ne peut pas aller par là")
            self.turn()  # Le joueur recommence son tour

    @staticmethod  # Fonction n'ayant pas besoin de l'instance de l'objet pour fonctionner
    def win():
        """ Cette fonction affiche cette illustration quand le joueur gagne """
        illustration.win()
        print("Félicitations, vous êtes arrivés à la porte du Paradis !")
        input()
        exit()

    @staticmethod
    def loose():
        """ Cette fonction affiche cette illustration quand le joueur perd """
        illustration.loose()
        print("Tu n'as plus d'énergie et tu errera désormais à jamais dans les limbes")
        input()
        exit()


class Case:
    """ Cette classe permet au joueur de visualiser sur la console la salle ou il se situe """
    dict_repr = illustration.get_case_repr()

    def __init__(self, x, y, symbole):
        """Initialise chaque instance de case par ses coordonnées et son type définit par la matrice"""
        self.x = x
        self.y = y
        self.coords = "{} {}".format(x, y)
        self.type = symbole

    def __repr__(self):
        """Affiche la salle selon son type"""
        return Case.dict_repr[self.type]


class Contenu:
    """Classe mère de tous ce que peut contenir une salle"""

    def __repr__(self):
        return "Salle vide"

    def effect(self):
        """Effet invoqué quand le joueur se trouve dans la pièce contenant l'énergie"""
        pass

    def signature(self):
        """Signature de l'ennemi invoqué quand le joueur se trouve autour de la pièce contenant l'ennemi
            Permet ici de ne rien faire quand le contenu n'est pas spéciale"""
        pass


class Room(Case):
    """Classe spécialisant les cases en pièces par la définition d'un contenu"""

    def __init__(self, x, y, symbole, contenu=Contenu()):
        super(Room, self).__init__(x, y, symbole)
        self.contenu = contenu


class Energy(Contenu):
    """Classe définissant l'effet des salles contenant de l'énergie"""

    def __init__(self, amount):
        """Initialise le contenue en énergie par le nombre d'énergie qu'elle contient"""
        self.amount = amount

    def effect(self):
        """Effet invoqué quand le joueur se trouve dans la pièce contenant l'énergie"""
        illustration.energy()
        print("Vous avez trouver {} pintes d'ectoplasme vert".format(self.amount))
        Game.player.energy += self.amount
        self.amount = 0


class Enemy(Contenu):
    """Classe définissant les ennemis comme un contenu de salle"""
    pass


class LandLord(Enemy):
    """Classe d'ennemie: Le Maître du Chateau"""

    def signature(self):
        """Signature du Maître du Chateau perçue quand le joueur se trouve autour de la pièce le contenant"""
        print("Cling Cling !")

    def effect(self):
        """Effet invoqué quand le joueur se trouve dans la pièce contenant le Maître du Chateau"""
        illustration.land_lord()
        input()
        Game.player.move(Game.reception.x, Game.reception.y)


class MadScientist(Enemy):
    """Classe d'ennemie: Le Scientifique Fou"""

    def signature(self):
        """Signature du Scientifique Fou perçue quand le joueur se trouve autour de la pièce le contenant"""
        print("Mwah ah ah ah !")

    def effect(self):
        """Effet invoqué quand le joueur se trouve dans la pièce contenant le Scientifique Fou"""
        illustration.mad_scientist()
        print("Dans sa fureur, il vous téléporte dans une salle aléatoire !")
        Game.player.energy -= 1
        chosen_case = Game.dict_case_coords[rd.choice(list(Game.dict_case_coords))]
        Game.player.move(chosen_case.x, chosen_case.y)

        print("Le bougre en a profiter pour vous subtiliser une pinte d'énergie ...")
        input()


class Bibendum(Enemy):
    """Classe d'ennemi: Bibendum"""

    def signature(self):
        """Signature du Bibendum perçue quand le joueur se trouve autour de la pièce le contenant"""
        print("Ça sent bon par ici !")

    def effect(self):
        """Effet invoqué quand le joueur se trouve dans la pièce contenant le Bibendum"""
        illustration.bibendum()
        input()
        input()
        input()
        print("vous perdez 2 d'énergie")
        Game.player.energy -= 2


class Player:

    def __init__(self):
        """Initialise la position du joueur"""
        self.x = Game.reception.x
        self.y = Game.reception.y
        self.coords = "{} {}".format(self.x, self.y)
        self.energy = 3

    def move(self, x, y):
        """Permet au joueur de bouger au nouvelles coordonnées x y données"""
        self.x = x
        self.y = y
        self.coords = "{} {}".format(self.x, self.y)


if __name__ == "__main__":
    game = Game()
