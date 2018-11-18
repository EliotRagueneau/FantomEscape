import random

# -*- coding: utf-8 -*-

# choix=""
# matrice_random=11*[10*[" "]]
# for j in range (9):
#     l1="⎾","⏤","⏋","O","|","+","⍈","┓","┊","┫","┣","⏊","┛","┗","⎿","⏌"," "
#     for i in range (9):
#         choix=rd.choice(l1)
#         matrice_random[j][i]=choix
#     print(matrice_random[i])
# for j in range(9):
#
# for ligne in matrice_random:
#     print(ligne)

#
# # matrix=[[" "] * 11] + [[" "]
# matrice=[]
# for x in range(11):
#     for y in range(11):
#         matrice.append([y][x])
#     # for x in random.choice(["⎾","⏤","⏋","O","|","+","⍈","┓","┊","┫","┣","⏊","┛","┗","⎿","⏌"," "])] + [" "]:
#     #     for _ in range(9)]:
#     #         [[" "] * 11]

# matrice=[[" "] * 11] + [[" "] + [x for _ in range(11) for x in random.choice(["┏", "⍈", "┏", "┣", "┗", "┓", "┫", "┛"])] + [" "] for _ in range(9)] + [[" "] * 11]

# nouvelle_liste=[]
# for i in range(9):
#     for j in range(11):
#         liste_random=random.choice(["⎾","⏤","⏋","O","|","+","⍈","┓","┊","┫","┣","⏊","┛","┗","⎿","⏌"," "])
#         for sous_liste in liste_random:
#             for element_sous_liste in sous_liste :
#                 nouvelle_liste.append(element_sous_liste)
#
# print(nouvelle_liste)


## +  = intersection
## trait = couloir
## carre = chambre
## x = point de depart
## 0 = arrivé

## maintenant dire a cote d'une chambre on peut avoir ca ou ca etc


matrice = [[" "] * 11] + \
          [[" "] + [x for _ in range(11) for x in random.choice(
              ["⎾", "⏤", "⏋", "O", "|", "+", "⍈", "┓", "┊", "┫", "┣", "⏊", "┛", "┗", "⎿", "⏌", " ", "x"])
                    ]
           + [" "] for _ in range(9)] + \
          [[" "] * 11]

chambre = ["⍈"]
# chambre_random=["+","⏤", "⍈","┓","┫","┛","┗","┣","┏"]
chambre_without_corner = ["+", "⏤", "⍈"]
chambre
depart = ["x"]
depart_random = ["⎿", "⏌"]
arrive = ["O"]
arrive_random = ["|"]
choix = []
choix2 = []
choix3 = []
new_line_chambre = []
new_line_depart = []
new_line_arrive = []
for line in matrice:
    for i in range(0, len(line) - 1):
        if line[i] == chambre[0]:
            # print("chambre")
            choix = random.choice(chambre_without_corner)
            new_line_chambre.append(choix)
        elif line[i] == depart[0]:
            # print("depart")
            choix2 = random.choice(depart_random)
            new_line_depart.append(choix2)
        elif line[i] == arrive[0]:
            # print("arrive")
            choix3 = random.choice(arrive_random)
            new_line_arrive.append(choix3)
        else:
            pass
            # print("je suis dans le vide")
    # print(line)
print('new_line_chambre', new_line_chambre)
print('new_line_depart', new_line_depart)
print('new_line_arrive', new_line_arrive)

matrice_random = [[" "] * 11] + [
    [" "] + [x for _ in range(11) for x in random.choice([new_line_depart, new_line_chambre, new_line_arrive])] + [" "]
    for _ in range(9)] + [[" "] * 11]
for line in matrice_random:
    print(line)

### sequence = [1, 2, 3]
### print([str(nombre) for nombre in sequence])
### ['1', '2', '3']
## peut s'ecrire comme ca:

# sequence = [1, 2, 3]
# new_seq=[]
# for nombre in sequence:
#     new_seq.append(str(nombre))
# print(new_seq)
