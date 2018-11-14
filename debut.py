class Initialisation():
    def map(self):
        "Cette fonction sert à délimiter la zone de jeu"
        print("quelle largeur de jeu voulez-vous?")
        largeur=[]
        largeur.append(int(input()))
        print("quelle hauteur voulez-vous?")
        hauteur=[]
        hauteur.append(int(input()))
        taille=[]
        taille.append([largeur,"*",hauteur])
        return taille

    def personnage(self):
        "Cette fonction définit les caracteristiques du personnage"
        health_points=int(3)
        trousseau="il me semble entendre un bruit de clé"
        rire="un fou rire dans un chateau ?"
        odeur="la suffocation est proche"
        gauche=[]       ## je pensais mettre en binaire, si utilisateur veut qu'il aille à gauche, gauche prend 1,et le reste 0 etc
        droite=[]
        avancer=[]
        recule=[]
        deplacer={"gauche":gauche,"droite":droite,"devant":avancer,"derriere":recule}
        message={"maître du chateau":trousseau,"savant_fou":rire,"3 bidules":odeur}
        dico_gaspard={"health_points":health_points,"deplacer":deplacer,"lire":message}
        return dico_gaspard


### main ###
self=Initialisation()
taille=self.map()
print("le jeu se déroulera sur une plateforme possédant",taille,"cases")
dico_gaspard=self.personnage()
#print(dico_gaspard)
