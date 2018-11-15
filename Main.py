import random as rd
import os
import sys
import time


class Plateau:
    matrice = reception = porte = player = None
    list_case = []
    dict_room = {}
    dict_case = {}

    def __init__(self, basic: bool = True):
        Plateau.matrice = Plateau._gen_basic() if basic else Plateau._gen_random()
        for y in range(len(Plateau.matrice)):
            for x in range(len(Plateau.matrice[y])):
                current_case = Plateau.matrice[y][x]
                Plateau.dict_case["{} {}".format(x, y)] = Case(x, y)
                if current_case not in [" ", "O"]:
                    Plateau.list_case.append(Case(x, y))
                if current_case == "o":
                    Plateau.dict_room["{} {}".format(x, y)] = Room(x, y)
                elif current_case == "x":
                    Plateau.reception = Room(x, y)
                elif current_case == "O":
                    Plateau.porte = Room(x, y)

        total_pinte = 5
        liste_pinte = []
        while total_pinte != 0:
            max_pinte_per_room = 3 if total_pinte >= 3 else total_pinte
            new_amount = rd.randint(1, max_pinte_per_room)
            liste_pinte.append(new_amount)
            total_pinte -= new_amount

        filled_rooms = rd.sample(list(Plateau.dict_room), 5 + len(liste_pinte))
        Plateau.dict_room[filled_rooms[0]].contenu = LandLord()
        Plateau.dict_room[filled_rooms[1]].contenu = MadScientist()
        for enemy_room in filled_rooms[2:5]:
            Plateau.dict_room[enemy_room].contenu = Bibbendum()

        n = 0
        for pinte_room in filled_rooms[5:]:
            Plateau.dict_room[pinte_room].contenu = Energy(liste_pinte[n])
            n += 1

        # for room in Plateau.list_room:
        #     print(room.x, room.y, room.contenu)

        Plateau.player = Player()
        self.turn()

    @staticmethod
    def _gen_basic():
        return [[" ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", "r", "⏤", "˥", " ", "O", " ", " "],
                [" ", " ", "|", " ", "|", " ", "|", " ", " "],
                [" ", "o", "+", "o", "+", "o", "+", "o", " "],
                [" ", "|", "|", " ", "|", " ", "|", "|", " "],
                [" ", "o", "+", "o", "+", "o", "+", "o", " "],
                [" ", "|", "|", " ", "|", " ", "|", "|", " "],
                [" ", "o", "+", "o", "+", "o", "⏊", "o", " "],
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
        possible_movements = []
        keys = {}
        haut = Plateau.matrice[y - 1][x]
        gauche = Plateau.matrice[y][x - 1]
        bas = Plateau.matrice[y + 1][x]
        droite = Plateau.matrice[y][x + 1]
        if haut != " ":
            possible_movements.append("haut : z")
            keys["z"] = (x, y - 1)
            if haut == "o":
                Plateau.dict_room["{} {}".format(x, y - 1)].contenu.signature()

        if gauche != " ":
            possible_movements.append("gauche : q")
            keys["q"] = (x - 1, y)
            if gauche == "o":
                Plateau.dict_room["{} {}".format(x - 1, y)].contenu.signature()

        if bas != " ":
            possible_movements.append("bas : s")
            keys["s"] = (x, y + 1)
            if bas == "o":
                Plateau.dict_room["{} {}".format(x, y + 1)].contenu.signature()

        if droite != " ":
            possible_movements.append("droite : d")
            keys["d"] = (x + 1, y)
            if droite == "o":
                Plateau.dict_room["{} {}".format(x + 1, y)].contenu.signature()

        for movement in possible_movements:
            print(movement)
        order = input()

        if order in keys:
            Plateau.player.move(keys[order][0], keys[order][1])
            if Plateau.player.coords in Plateau.dict_room:
                Room.door_animation()
                Plateau.dict_room[Plateau.player.coords].contenu.effect()
                if Plateau.player.energy <= 0:
                    self.loose()
                Room.door_animation()
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
              ""
              , sep="\n")
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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coords = "{} {}".format(x, y)

    def is_room(self):
        return True if self.coords in Plateau.dict_room else False

    def has_enemy(self):
        return True if self.is_room() and isinstance(Plateau.dict_room[self.coords].contenu, Enemy) else False


class Contenu:
    def effect(self):
        input()
        print('',
              '',
              '               .-----.                                _.----"""""""----._',
              '          _.---//-"""-\\\\---._            .------.___  (                   )',
              '         (   (/        `-\'   )          (        ___|-|`"""---..___..---""|',
              '        _|`"--._________.--"\'|_          `---\'"""     |                   |',
              '       (_|                   |_)                      |                   |',
              '       `--)                 (--\'          ________    |                   |',
              '         |                   |   _.--"""""        """"----._              |',
              '         |                   |  (_                         _)--.----------------.',
              '         |                   |   \`""---...________...----\'/__/___             ||',
              "         `-.__           __.-'    \___                  __/ ""-----\"\"\"\"\"\"\"-----`''",
              '              `""-----""\'              ""`-----------'"",
              '',
              sep='\n')
        input()

    def signature(self):
        pass


class Room(Case):
    def __init__(self, x, y, contenu=Contenu()):
        super(Room, self).__init__(x, y)
        self.contenu = contenu

    @staticmethod
    def door_animation():
        print(" ______________",
              "|\ ___________ /|",
              "| |  _ _ _ _  | |",
              "| | | | | | | | |",
              "| | |-+-+-+-| | |",
              "| | |-+-+=+%| | |",
              "| | |_|_|_|_| | |",
              "| |    ___    | |",
              "| |   [___] ()| |",
              "| |         ||| |",
              "| |         ()| |",
              "| |           | |",
              "| |           | |",
              "| |           | |",
              "|_|___________|_|", sep="\n")
        input()
        print(" ______________",
              "|\ ___________ /|",
              "| |  /|,| |   | |",
              "| | |,x,| |   | |",
              "| | |,x,' |   | |",
              "| | |,x   ,   | |",
              "| | |/    |   | |",
              "| |    /] ,   | |",
              "| |   [/ ()   | |",
              "| |       |   | |",
              "| |       |   | |",
              "| |       |   | |",
              "| |      ,'   | |",
              "| |   ,'      | |",
              "|_|,'_________|_|\n", sep="\n")


class Enemy(Contenu):
    pass


class LandLord(Enemy):
    def signature(self):
        print("Cling Cling !")

    def effect(self):
        input()
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
        input()
        print(
            "                           __              []",
            "                           ||              []",
            "                           ||              []",
            "                           ||              []",
            "                        __ ||              []",
            "                        || ||              []",
            "                      .-||-||-.            []  /\\",
            "                     _\_______/_===========[]=(-o)",
            "                      )\_____/(            []  \/",
            "                     /     ||  \           []",
            "                    /      ||   \          []",
            "                   /       ||    \         []",
            "                  /~~~~~~~~~~~~~~~\        []",
            "                 /         ::      \       []",
            "                (          ::       )      []",
            "                 `-----------------'       []",
            "                         )                 []",
            "                       (   )               []",
            "                         )( . (            []",
            "                      .) @@)   )           []",
            "                   ` ) @@(@@)@             []",
            "                     (@@(@@)@              []",
            "                      @(@.@)@@             []",
            "                    ` (@{__}@)`            []",
            "                        :__;               []",
            "    ___                  {}+               []",
            "   ( = )             .---'`---.            []",
            "    | |_            /          \   ________[]____",
            "____| |_|==========(____________)_/______________\\",
            "Oh non ! Un scientifique fou se tient devant vous !!!",
            sep="\n")

        input()
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
        input()
        print("                 (0B",
              "                (000B",
              "              (0000000B              ",
              "             (000000000B              ",
              "              (0000000B              ",
              "             (000000000B              ",
              "              (0000000B              ",
              "               (00 (0B              ",
              "              (00   (0B              ",
              "             (00     (0B              ",
              "            (00       (0B              ",
              "            (00       (0B              ",
              "          (0000       (000B              ",
              "         (OOOO0       (OOOOB              ",
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
        input()
        print(
            "           _",
            "        ,-'  `-._",
            "       |=========|",
            "       (         )",
            "        | !!    |",
            "        | !!    |",
            "        |       |",
            "        |       | hjw",
            "        `======='",
            sep="\n")
        print("Vous avez trouver {} pintes d'ectoplasme vert".format(self.amount))
        Plateau.player.energy += self.amount
        self.amount = 0
        input()


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
    print(Player().x)

print("",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "", sep="\n")

print('',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '',
      '', sep='\n')
