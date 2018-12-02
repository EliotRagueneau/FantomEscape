import random as rd
from main_graphics import *


def _gen_random():
    """ Cette fonction permet de creer la map de facon aleatoire """
    matrice_ori = Game._gen_basic() # Importation de la matrice d'origine
    liste_cases = []
    for ligne in matrice_ori: # Parcours de la matrice original
        for case in ligne:
            if case not in liste_cases:
                liste_cases.append(case) # Ajout des elements de la matrice original dans liste_cases

    mm_haut = MarkovModel(liste_cases) # Création chaîne de markov
    mm_droite = MarkovModel(liste_cases)
    mm_gauche = MarkovModel(liste_cases)

    for y in range(len(matrice_ori) - 1, 0, -1): #
        for x in range(len(matrice_ori[0])):
            mm_haut[matrice_ori[y][x]][matrice_ori[y - 1][x]] += 1

    for y in range(len(matrice_ori)):
        for x_d in range(len(matrice_ori[0]) - 1):
            mm_droite[matrice_ori[y][x_d]][matrice_ori[y][x_d + 1]] += 1
        for x_l in range(len(matrice_ori[0]) - 1, 0, -1):
            mm_gauche[matrice_ori[y][x_l]][matrice_ori[y][x_l - 1]] += 1

    matrice = [["x"]]
    for _ in range(6):

        for ligne in matrice:
            weights = mm_gauche[ligne[0]].values() # Ajout d'un poids a chaque element du dictionnaire
            ligne.insert(0, rd.choices(liste_cases, weights=weights)[0]) # insert un element de list_case en position 0
            weights = mm_droite[ligne[-1]].values()
            ligne.append(rd.choices(liste_cases, weights=weights)[0])

        new_top_line = []
        for x in matrice[0]:
            weights = mm_haut[x].values()
            new_top_line.append(rd.choices(liste_cases, weights=weights)[0])
        matrice.insert(0, new_top_line)

        for line in matrice: # Affichage des lignes de la matrice
            print(line)
        print()


class MarkovModel(dict):
    def __init__(self, liste_etats):
        self.liste_etats = liste_etats
        super(MarkovModel, self).__init__({key: {key: 0 for key in liste_etats} for key in liste_etats})

    def normalize(self, case):
        """Pas besoin en fait avec rd.choices"""
        normalized = self[case].values()
        total = sum(normalized)
        normalized = [x / total for x in normalized]

    def __repr__(self):
        out = ""
        for origine in self:
            out += "{} --> {}\n".format(origine, self[origine])
        return out
