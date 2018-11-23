import random as rd


class Game:
    """Classe regroupant l'ensemble des fonctionnalités du jeu
        Contrôles:
            z  ==> Aller en haut
            q  ==> Aller à gauche
            s  ==> Aller en bas
            d  ==> Aller à droite"""

    matrice = reception = porte = player = None
    dict_room_coords = {}
    dict_case_coords = {}

    def __init__(self, basic: bool = True):
        """ Cette fonction initialise le plateau le jeu
            Elle permet également de choisir la generation basique ou random """

        Game.matrice = Game._gen_basic() if basic else Game._gen_random()
        for y in range(len(Game.matrice)):
            for x in range(len(Game.matrice[y])):
                current_case = Game.matrice[y][x]
                if current_case != " ":
                    Game.dict_case_coords["{} {}".format(x, y)] = Case(x, y, current_case)

                if current_case in ["┏", "⍈", "┏", "┣", "┗", "┓", "┫", "┛"]:
                    Game.dict_room_coords["{} {}".format(x, y)] = Room(x, y, current_case)

                if current_case == "x":
                    Game.reception = Room(x, y, current_case)

                elif current_case == "O":
                    Game.porte = Room(x, y, current_case)

        total_pinte = 5
        liste_pinte = []
        while total_pinte != 0:
            new_amount = rd.randint(1, 3 if total_pinte >= 3 else total_pinte)
            liste_pinte.append(new_amount)
            total_pinte -= new_amount

        list_filled_room_coords = rd.sample(list(Game.dict_room_coords), 5 + len(liste_pinte))

        Game.dict_room_coords[list_filled_room_coords[0]].contenu = LandLord()

        Game.dict_room_coords[list_filled_room_coords[1]].contenu = MadScientist()

        for enemy_room in list_filled_room_coords[2:5]:
            Game.dict_room_coords[enemy_room].contenu = Bibendum()

        n = 0
        for pinte_room in list_filled_room_coords[5:]:
            Game.dict_room_coords[pinte_room].contenu = Energy(liste_pinte[n])
            n += 1

        Game.player = Player()
        self.turn()

    @staticmethod
    def _gen_basic():
        """Génère la matrice map basique telle que montrée dans le sujet"""

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
    def _gen_random():
        """ Génère la matrice map aléatoirement """
        pass

    def __repr__(self):
        """Permet d'afficher correctement la matrice"""
        return "\n".join(["".join(line) for line in Game.matrice])

    def turn(self):
        """Définit le déroulement de chaque tour du jeu"""
        # Récupération des coordonnées du joueur
        x = Game.player.x
        y = Game.player.y

        keys = {}  # Initialise le dictionnaire contenant les mouvements possibles du joueur à chaque tour

        contour = {"z": {"coords": "{} {}".format(x, y - 1), "tuple": (x, y - 1)},
                   "q": {"coords": "{} {}".format(x - 1, y), "tuple": (x - 1, y)},
                   "s": {"coords": "{} {}".format(x, y + 1), "tuple": (x, y + 1)},
                   "d": {"coords": "{} {}".format(x + 1, y), "tuple": (x + 1, y)}
                   }

        for key in contour:  # key est ici les différentes input possibles
            if contour[key]["coords"] in Game.dict_case_coords:  # Si se qui se trouve autour du joueur est une case
                keys[key] = contour[key]["tuple"]  # Alors le joueur peut s'y déplacer
                if contour[key]["coords"] in Game.dict_room_coords:  # Et si c'est une salle
                    Game.dict_room_coords[contour[key]["coords"]].contenu.signature()  # On éxécute la signature de son contenu

        print(Game.dict_case_coords[Game.player.coords])  # Affiche la salle où se trouve le joueur
        order = input()

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
        print("                                                   .-')                 ",
              "                                                  /   |                 ",
              "                                                .' /  F                 ",
              "       /                                       /  / //)                 ",
              "      /(                                     .< .'.''|                 ",
              "     /_ `-._                              .')' ).'.'')                 ",
              "     ' `-._ `-.                         .'.'.'/.''.'/-                 ",
              "           `-._`-.__        .--.      .'-'/..'`).'.' /                 ",
              "               `. / `.   _.':-::\   .' ' ).'.'/.' .''_         .')                 ",
              "                 >- /_`.)::` -.)|--'.'-'--.'.'-..''  /       .' /                 ",
              "                 |:|  `.>    )   ))'.'/-'/.-'.-'' _.'   _.-') .'                 ",
              "                 /:|   `..:'       )_.>_.>_.-'_.-' `..-'.-')-'_                 ",
              "                /::)___.-::::-.   ))__> <_.-'  _.--'_.-'_.-'_.'                 ",
              "               /:' .::::::::\     ))-. .> __<-'  )_>_.-'--'.'                 ",
              "               `::...         )  ))-.<_>__\____.-'---'_.-'--.                 ",
              "                 `-:::::       ) ))-'__>-'____<__)--' `----'                 ",
              "                     `-::): ..    )-->._\-----'__________>                 ",
              "                       )    ::   >_>_`._ `--.->_____.--'                 ",
              "                       |   :.\"\"  )\_ ___>----'-----'                 ",
              "                       J:      \)\)`-`-.__`-.`--'                 ",
              "                        >-\"\"\"\"-.\))\ \`-\`.__)-'                 ",
              "                        / /\|`. :\/`--\_\`-'                 ",
              "                        ).:: `::::`.                 ",
              "                       /.::: ::'    `.                 ",
              "                      (.:-::.:::' .-._)                    ___                 ",
              "                        | :`-' \ /  `-.____              .' .(                 ",
              "                        |::  (:   `,`.`.  :`._______   .'  :: \                 ",
              "                        |:    \: ::  `  `---.:::::  `./  .:'  .)                 ",
              "                        J:     :: `:  \   -::::::::' `:::' .::/                 ",
              "                         \  |  \:: ::  `-.    -.  `:..:::::::'                 ",
              "                         ) .    :::`::   _ `.  -. `::.-.__.'-.                 ",
              "                         |:: \  `::  `.:.     `-.  `.`::::::' )                 ",
              "                         |:|:\   \::  \ :.`.`:     `._ -::::-')                 ",
              "                         |::      \:: ` \`::  \ `.`    `:::::(                 ",
              "                         |::. \ \   ::    ` \  :\   \ .-._\"\"- \                 ",
              "                          \\\\  :|   \\\\::\   \ : \: \  `. `::::::)                 ",
              "                           \\\\ \:\    \ ::  \ :. \: |   -:::.---<                 ",
              "                            \  \  \   :.::. | |  |:  \    :::::/                 ",
              "                             \     \  `::\:: |    :  \       -'                 ",
              "                              L       \ `:-.<: |  |:  `:..  < )                 ",
              "                              || \   \   `.: `:    `:  `-:::.'                 ",
              "                              ) : \    `    :\ :|. \::\  ._)                 ",
              "                              | :|  :\ `:  \ :\ :<  `:::.|(                 ",
              "                              /::   ::: ::  :\::::\   `:.'                 ",
              "                              |::J :|::  :\  :\::-.\   (                 ",
              "                              /    ):::| ):.):::|  \_. |                 ",
              "                             |:.- :::::: :::::::/  `::/                 ",
              "                             |:::::::-:::::::::'                 ",
              "                            J:::::::  \::/ `-'                 ",
              "                            |::::::|   \"\"                 ",
              "                            `:::::'                 ",
              "                              `-'                 ",
              sep="\n")
        print("Félicitations, vous êtes arrivés à la porte du Paradis !")
        input()
        exit()

    @staticmethod
    def loose():
        """ Cette fonction affiche cette illustration quand le joueur perd """
        print("                   _.-, ",
              "              _ .-'  / .._",
              "           .-:'/ - - \:::::-.",
              "         .::: '  e e  ' '-::::.",
              "        ::::'(    ^    )_.::::::",
              "       ::::.' '.  o   '.::::'.'/_",
              "   .  :::.'       -  .::::'_   _.:",
              " .-''---' .'|      .::::'   '''::::",
              "'. ..-:::'  |    .::::'        ::::",
              " '.' ::::    \ .::::'          ::::",
              "      ::::   .::::'           ::::",
              "       ::::.::::'._          ::::",
              "        ::::::' /  '-      .::::",
              "         '::::-/__    __.-::::'",
              "           '-::::::::::::::-'",
              "               '''::::'''",
              sep="\n")
        print("Tu n'as plus d'énergie et tu errera désormais à jamais dans les limbes")
        input()
        exit()


class Case:
    """ Cette classe permet au joueur de visualiser sur la console la salle ou il se situe """
    dict_repr = {"⍈": "               \n" +
                      "  ┏━━━━━━━━━┓  \n" +
                      " ┯┛         ┗┯ \n" +
                      " ┷┓         ┏┷ \n" +
                      "  ┗━━━━━━━━━┛  \n" +
                      "               \n",

                 "x": "               \n" +
                      "  ┏━━━━━━━━━┓  \n" +
                      " ┯┛         ┗┯ \n" +
                      " ┷┓         ┏┷ \n" +
                      "  ┗━━━━━━━━━┛  \n" +
                      "               \n",

                 "┏": "               \n" +
                      "  ┏━━━━━━━━━┓  \n" +
                      "  ┃         ┗┯ \n" +
                      "  ┃         ┏┷ \n" +
                      "  ┗━━━┓ ┏━━━┛  \n" +
                      "      ┠─┨      \n",

                 "┣": "      ┠─┨      \n" +
                      "  ┏━━━┛ ┗━━━┓  \n" +
                      "  ┃         ┗┯ \n" +
                      "  ┃         ┏┷ \n" +
                      "  ┗━━━┓ ┏━━━┛  \n" +
                      "      ┠─┨      \n",

                 "┗": "      ┠─┨      \n" +
                      "  ┏━━━┛ ┗━━━┓  \n" +
                      "  ┃         ┗┯ \n" +
                      "  ┃         ┏┷ \n" +
                      "  ┗━━━━━━━━━┛  \n" +
                      "               \n",

                 "┓": "               \n" +
                      "  ┏━━━━━━━━━┓  \n" +
                      " ┯┛         ┃  \n" +
                      " ┷┓         ┃  \n" +
                      "  ┗━━━┓ ┏━━━┛  \n" +
                      "      ┠─┨      \n",

                 "┫": "      ┠─┨      \n" +
                      "  ┏━━━┛ ┗━━━┓  \n" +
                      " ┯┛         ┃  \n" +
                      " ┷┓         ┃  \n" +
                      "  ┗━━━┓ ┏━━━┛  \n" +
                      "      ┠─┨      \n",

                 "┛": "      ┠─┨      \n" +
                      "  ┏━━━┛ ┗━━━┓  \n" +
                      " ┯┛         ┃  \n" +
                      " ┷┓         ┃  \n" +
                      "  ┗━━━━━━━━━┛  \n" +
                      "               \n",

                 "┊": "      ┠─┨      \n" +
                      "      ┃ ┃      \n" +
                      "      ┃ ┃      \n" +
                      "      ┃ ┃      \n" +
                      "      ┃ ┃      \n" +
                      "      ┠─┨      \n",

                 "|": "      ┋ ┋      \n" +
                      "      ┃ ┃      \n" +
                      "      ┃ ┃      \n" +
                      "      ┃ ┃      \n" +
                      "      ┃ ┃      \n" +
                      "      ┋ ┋      \n",

                 "⎿": "      ┋ ┋      \n" +
                      "      ┃ ┃      \n" +
                      "      ┃ ┗━━━━━┯\n" +
                      "      ┗━━━━━━━┷\n" +
                      "               \n" +
                      "               \n",

                 "⏌": "      ┋ ┋      \n" +
                      "      ┃ ┃      \n" +
                      "┯━━━━━┛ ┃      \n" +
                      "┷━━━━━━━┛      \n" +
                      "               \n" +
                      "               \n",

                 "+": "      ┋ ┋      \n" +
                      "      ┃ ┃      \n" +
                      "┯━━━━━┛ ┗━━━━━┯\n" +
                      "┷━━━━━┓ ┏━━━━━┷\n" +
                      "      ┃ ┃      \n" +
                      "      ┋ ┋      \n",

                 "⎾": "               \n" +
                      "               \n" +
                      "      ┏━━━━━━━┉\n" +
                      "      ┃ ┏━━━━━┉\n" +
                      "      ┃ ┃      \n" +
                      "      ┋ ┋      \n",

                 "⏤": "               \n" +
                      "               \n" +
                      "┉━━━━━━━━━━━━━┉\n" +
                      "┉━━━━━━━━━━━━━┉\n" +
                      "               \n" +
                      "               \n",

                 "⏋": "               \n" +
                      "               \n" +
                      "┉━━━━━━━┓      \n" +
                      "┉━━━━━┓ ┃      \n" +
                      "      ┃o┃      \n" +
                      "      ┋ ┋      \n",

                 "⏊": "      ┋ ┋      \n" +
                      "      ┃ ┃      \n" +
                      "┯━━━━━┛o┗━━━━━┯\n" +
                      "┷━━━━━━━━━━━━━┷\n" +
                      "               \n" +
                      "               \n",
                 }

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

    def __repr__(self):
        return "{} pintes vertes d'énergie".format(self.amount)

    def effect(self):
        """Effet invoqué quand le joueur se trouve dans la pièce contenant l'énergie"""
        print(
            "           _",
            "        ,-'  `-._",
            "       |=========|",
            "       (         )",
            "        | !!    |",
            "        | !!    |",
            "        |       |",
            "        |       |",
            "        `======='",
            sep="\n")
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
        print("                               _________",
              "                              [_________]",
              "                      ,,,,,      _|//",
              "                     , , ;;      ( /",
              "                    <    D        =o",
              "                    |.   /       /\|",
              "                _____|><|_______/o /",
              "               / '==| :: |=='  <  /",
              "              /  \  <    >  /____/",
              "             /  _/\ | :: | /",
              "              \  ||_|____|/",
              "               |o| |  x  |",
              "               ( \ / _'_ \\",
              "               ////   |   \\",
              "                 |    |    |",
              "                 |    |    |",
              "                 |    |    |",
              "                 \ _  |  _ /",
              "                  \   |   /",
              "                   \  |  /",
              "                    |_|_|",
              "                   /o | o\\",
              "                  /o _|_ o\\",
              "                 (__/   \__) ",
              "Retourne donc à la Réception mon très cher Gasper !",
              sep="\n")
        input()
        Game.player.move(Game.reception.x, Game.reception.y)

    def __repr__(self):
        return "LandLord"


class MadScientist(Enemy):
    """Classe d'ennemie: Le Scientifique Fou"""
    def signature(self):
        """Signature du Scientifique Fou perçue quand le joueur se trouve autour de la pièce le contenant"""
        print("Mwah ah ah ah !")

    def effect(self):
        """Effet invoqué quand le joueur se trouve dans la pièce contenant le Scientifique Fou"""
        print(
            "                                            . ",
            "                        .   \\ \\ / \\ \\|   \\ | / /  ,",
            "                      \\  \\  | | |  |/ \\  | | |/  /  | .",
            "                    \\  |  \\ \\ | \\ / | | / / / | |   /_/  /",
            "                \\_ \\ \\ \\  |  |\\ | | | / | | | / _/,-'/_,-' /",
            "            _   _ \\ \\|  \\_\\_  \\| \\ \\\\ | |/ / / / _/ _/,---'  /",
            "             \\___\\ \\_ \\__ \\ \\ | \\ \\ | / // | / // _/_/__/ __/_",
            "           __  _ \\_  \\   \\  |  \\ \\  |/ |/  | | / / / /___/ _/ _/",
            "         _   \\___  \\                                 /  _____/",
            "          \\_ \\__ \\    -------.___    -----._______     / _/  __/",
            "            \\__ \\    _____       -----              __  / __/",
            "               \\               _______   ------'         /",
            "            __ |     ___________         ___________     | __",
            "           /  `| ,-' ___________ '.   ,' ___________ `-. |'  \\",
            "           | /` (_,-' _______   `./   \\,'   _______ `-._) '\\ |",
            "           | |     ,-'   `._,`-.         ,-'   `._,`-.     | |",
            "           | |.  ,' `.          `.     ,' `.          `.  :| |",
            "           | \\   `.   `-._____,-,'     `.   `-._____,-,'   / |",
            "            \\  '   `-._______,-'  :   :  `-._______,-'    ' / ",
            "             \\_.                  |   |                  ._/",
            "               |                  |   |                  |",
            "                \\                /     \\                /",
            "                 \\              /       \\              /",
            "                  \\            |         |            /",
            "                   |           \\,--._,--./           |",
            "                   |       _,.--'''`-'''`--.._       |",
            "--.  ,---.  ,---.  |     ,' __,-----------.__ `.     ,---.  ,---.  ,---.  ,---.",
            "-- \\(     \\(  -- \\_|____/_,'\\/|  |  |  |  |\\/`._\\__ / --  )/     )/ --  )/,--, )",
            ".--.\\\\  -- \\\\ .--.\\           `-.|__|__|,-'        /,--, // --  //,--, /(/__/ /",
            " \\__\\)\\ .--.\\\\ \\__\\)                              (/__/ //,--, /(/__/ /  `---'",
            "`---'  \\ \\__\\)`---'                                `---'(/__/ /  `---'",
            "        `---'                                            `---'",
            sep="\n")
        print("Dans sa fureur, il vous téléporte dans une salle aléatoire !")
        Game.player.energy -= 1
        chosen_case = Game.dict_case_coords[rd.choice(list(Game.dict_case_coords))]
        Game.player.move(chosen_case.x, chosen_case.y)

        print("Le bougre en a profiter pour vous subtiliser une pinte d'énergie ...")
        input()

    def __repr__(self):
        return "MadScientist"


class Bibendum(Enemy):
    """Classe d'ennemi: Bibendum"""
    def signature(self):
        """Signature du Bibendum perçue quand le joueur se trouve autour de la pièce le contenant"""
        print("Ça sent bon par ici !")

    def effect(self):
        """Effet invoqué quand le joueur se trouve dans la pièce contenant le Bibendum"""
        print("     ,...._                          _,.._",
              "    (  \ \\\"b_.._                  _,d8P\"\"Y8o.",
              "    `8\ \ \ 8P\"8                 ,8\"  _    _Yb.",
              "     8 \ \ `8. 8.                8' ,'\"'.,'\".l8",
              "     Y  `__,9' Yb               ,8o.[(#)][(#]'Yo",
              "     `Y.       l8.             jP'   '\"' `'\"' '8b",
              "       `8b.    8\"\"b            ll      ----    8P",
              "       ,dP\"._  \"  88b.         '8b.          ,d8._",
              "       l8[ `\"    ,P `88888bod88888K.        .9\"\"\"\"'Yo._",
              "       `8bo____,o\"   8 `8K\"Yb.                       YP\"b.",
              "        Y8.\"\"\"\"'    ,P  `8.  Yb                    _,db. Yb",
              "         Y8b.     ,d\"    8l   8o...___     ____,,,o\"' `Ybl8",
              "          `88oooo\"\"     ,8'   l[`\"\"Y88888888P\"\"''      `8d8b.",
              "           `Yb._      ,d8P    d'                       ,8P Y8",
              "             `Y8boooodP\"     dP                      _,8b   8'",
              "                `Y8bo.____,od8o._                _,odP  Yb d8",
              "                   `\"\"Y8P\"\"'  `\"\"\"Yoooo,,,,,,oooo\"\"\"'   dP\"\"Yb",
              "                      `Yb.          `\"\"\"\"\"\"\"\"'         ,8'   8b",
              "                       ,8oo.                         _,P'   ,PYb.",
              "                       l8 `\"oo._                  _,o88b ,o8P  `8b",
              "                       '8b   `\"\"ooo,,,,,,,,,,,ooodP\"  8P\"\"'     JP",
              "                      ,d^Yb_       `\"\"\"\"\"\"\"\"\"\"'      d8b._    ,d8b",
              "                      lP  `Yb._                  _,,888\"\"8boo\"' `\"bo.",
              "                      'b    `\"\"8boo,,,,,,,,,,,ood8P' 88    ,8P.  `o 8b",
              "                     ,d8.       `\"\"\"\"\"\"\"\"7T\"\"\"''    dP'    `Y',\"oo\" Y8",
              "                     8P`Yo_             ,d'      _,d88      `Y./o8ooP'",
              "                     8'  `\"8.__      _,d8boooooo\"\"' 88        `\"",
              "                     8b     `\"\"ooooo\"\"'8'          d8'",
              "                    ,d8b             ,88._     _,d8P",
              "                  ,d88 `Yb.        ,d8' `\"\"8888\"' 8'",
              "                 d8P`8.  `\"\"oooood88\"\"8.        _,8b",
              "                 8l  \"b.         d88. `\"8o,,,,,o\"' 8",
              "                 Yl   `\"o,,___,od8'`8.   `\"\"\"\"'   ,P",
              "                ,d8.     `\"\"\"\"\"' 8  d8o.       _,dP",
              "               ,8' Yo.         ,d'  8l \"Yoooooo\"\"8",
              "               '8.  `\"o,,,,,,od\"'   Yb.         d8",
              "                Yb.         ,8'      `8b.____,d8\"",
              "                 `8b.__  _,d8'       ,o8\"\"\"\"\"\"b",
              "                ,dP `\"\"\"8\"\"'         l8'   \"\"\"8b.",
              "               ,8\" \"\"\" dP            '8.    \"\"\"`\"8b.",
              "              dP' `\"\"\" 8b             `\"b.        `Yb",
              "             d         `8               `8b       ,l8",
              "             8         ,8                `8bo,,,d88P'",
              "             `8o.__  _,d8'                  `\"\"\"\"'",
              "               `\"88888\"'",
              "",
              "Vous êtes paralysés !!!",
              sep="\n")

        input()
        input()
        input()
        print("vous perdez 2 d'énergie")
        Game.player.energy -= 2

    def __repr__(self):
        return "Bibbendum"


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
    print(Game())
