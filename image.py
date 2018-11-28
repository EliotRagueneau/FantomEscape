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
def effect():
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

def LandLord():
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

def MadScientist():
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


def  Bibendum():
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
