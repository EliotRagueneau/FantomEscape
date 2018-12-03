#!/usr/bin/env python3
import random as rd
from typing import *

import illustration


class Game:
    """Classe regroupant l'ensemble des fonctionnalités du jeu"""

    matrice = reception = porte = player = None
    dict_room_coords = {}
    dict_case_coords = {}

    def __init__(self, basic: bool = True, difficulty: float = 0):
        """ Cette fonction initialise le plateau le jeu; 0 > difficulty > 1
            Elle permet également de choisir la generation basique ou random """

        print("\nContrôles:",
              "\tz ou 8 ==> Aller en haut",
              "\tq ou 4 ==> Aller à gauche ",
              "\ts ou 2 ==> Aller en bas ",
              "\td ou 6 ==> Aller à droite \n",
              sep="\n")

        Game.matrice = Game._gen_basic() if basic else Game._gen_random()  # Récupère la matrice de jeu

        # Récupération des informations contenus dans la matrice #

        for y in range(len(Game.matrice)):  # Pour chaque coordonnées sur la matrice
            for x in range(len(Game.matrice[0])):

                current_case = Game.matrice[y][x]  # On récupère la case de la matrice définie par ses coordonnées

                if current_case != " ":
                    Game.dict_case_coords[(x, y)] = Case(x, y, current_case)  # Case accessible au joueur

                    if current_case in ["┏", "⍈", "┏", "┣", "┗", "┓", "┫", "┛"]:
                        Game.dict_room_coords[(x, y)] = Room(x, y, current_case)  # Salle

                    elif current_case == "x":  # Si la case correspond à la réception
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

        # Détermination du nombre de monstres vis à vis de la difficulté donnée #

        if not difficulty:  # Si l'utilisateur ne précise pas la difficulté
            n_monster = 5  # 5 monstres de base
        elif difficulty < 1:
            n_monster = int(difficulty * (len(Game.dict_room_coords) - len(liste_pinte)))
        else:  # 1 ou plus ==> Que des monstres et des pintes
            n_monster = len(Game.dict_room_coords) - len(liste_pinte)

        # Choix aléatoire des salles contenant quelque chose parmi toutes les salles possibles#

        list_filled_room_coords = rd.sample(list(Game.dict_room_coords), n_monster + len(liste_pinte))

        # Remplissage de ces salles #
        n_pinte = 0  # Pointeur de pinte dans liste_pinte
        for i in range(len(list_filled_room_coords)):
            if i == 0:  # Un seul LandLord
                Game.dict_room_coords[list_filled_room_coords[i]].contenu = LandLord()
            elif i < 0.4 * n_monster:  # 40% du reste des monstres serons des Mad Scientist
                Game.dict_room_coords[list_filled_room_coords[i]].contenu = MadScientist()
            elif i < n_monster:  # Le reste des monstres seront des Bibendum
                Game.dict_room_coords[list_filled_room_coords[i]].contenu = Bibendum()
            else:  # Hors monstre ==> Énergie définis par liste_pinte
                Game.dict_room_coords[list_filled_room_coords[i]].contenu = Energy(liste_pinte[n_pinte])
                n_pinte += 1

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
        x, y = Game.player.coords

        print("Vous avez {} d'énergies\n".format(Game.player.energy))
        possible_order = {}  # Initialise le dictionnaire contenant les mouvements possibles du joueur à chaque tour

        contour = {(x, y - 1): ("z", "8"),
                   (x - 1, y): ("q", "4"),
                   (x, y + 1): ("s", "2"),
                   (x + 1, y): ("d", "6")}

        for contour_coords in contour:
            if contour_coords in Game.dict_case_coords:  # Si ce qui se trouve autour du joueur est une case
                for order in contour[contour_coords]:  # Alors le joueur peut s'y déplacer via différends ordres
                    possible_order[order] = contour_coords  # Ordres que l'on stocke dans le dictionnaire keys

                if contour_coords in Game.dict_room_coords:  # Et si c'est une salle
                    Game.dict_room_coords[contour_coords].contenu.signature()  # On exécute la signature de son contenu

        print(Game.dict_case_coords[Game.player.coords])  # Affiche la salle où se trouve le joueur

        order = input()  # Récupère l'ordre de mouvement du joueur

        if order in possible_order:  # Si l'ordre du joueur se trouve bien dans les possibilités définies plus tôt
            Game.player.move(possible_order[order])  # Le joueur se déplace vers la direction souhaitée

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
        self.coords = (x, y)
        self.type = symbole

    def __repr__(self):
        """Affiche la salle selon son type"""
        return Case.dict_repr[self.type]


class Contenu:
    """Classe mère de tous ce que peut contenir une salle"""

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
        self.amount = amount

    def effect(self):
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
        Game.player.move(Game.reception.coords)


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
        Game.player.move(chosen_case.coords)

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
        self.coords = Game.reception.coords
        self.energy = 3

    def move(self, coords: Tuple[int]):
        """Permet au joueur de bouger au nouvelles coordonnées x y données"""
        self.coords = coords


if __name__ == "__main__":
    game = Game(difficulty=0.5)
