import random as rd


class Plateau:
    matrice = reception = porte = player = None
    dict_room_coords = {}
    dict_case_coords = {}

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

        for enemy_room in list_filled_room_coords[2:5]:
            Plateau.dict_room_coords[enemy_room].contenu = Bibendum()

        n = 0
        for pinte_room in list_filled_room_coords[5:]:
            Plateau.dict_room_coords[pinte_room].contenu = Energy(liste_pinte[n])
            n += 1

        Plateau.player = Player()
        self.turn()

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
                      "      ┃ ┃      \n" +
                      "      ┋ ┋      \n",

                 "⏊": "      ┋ ┋      \n" +
                      "      ┃ ┃      \n" +
                      "┯━━━━━┛ ┗━━━━━┯\n" +
                      "┷━━━━━━━━━━━━━┷\n" +
                      "               \n" +
                      "               \n",
                 }

    def __init__(self, x, y, symbole):
        self.x = x
        self.y = y
        self.coords = "{} {}".format(x, y)
        self.type = symbole

    def __repr__(self):
        return Case.dict_repr[self.type]


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
        print("Cling Cling !")

    def effect(self):
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
        Plateau.player.move(Plateau.reception.x, Plateau.reception.y)

    def __repr__(self):
        return "LandLord"


class MadScientist(Enemy):
    def signature(self):
        print("Mwah ah ah ah !")

    def effect(self):
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
        Plateau.player.energy -= 1
        chosen_case = Plateau.dict_case_coords[rd.choice(list(Plateau.dict_case_coords))]
        Plateau.player.move(chosen_case.x, chosen_case.y)

        print("Le bougre en a profiter pour vous subtiliser une pinte d'énergie ...")
        input()

    def __repr__(self):
        return "MadScientist"


class Bibendum(Enemy):
    def signature(self):
        print("Ça sent bon par ici !")

    def effect(self):
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
        Plateau.player.energy -= 2

    def __repr__(self):
        return "Bibbendum"


class Energy(Contenu):
    def __init__(self, amount):
        self.amount = amount

    def __repr__(self):
        return "{} pintes vertes d'énergie".format(self.amount)

    def effect(self):
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
