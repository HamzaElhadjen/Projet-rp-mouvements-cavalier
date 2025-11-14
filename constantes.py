# Taille de l'échiquier
TAILLE_ECHIQUIER = 8
CASE_DEPART = (0, 0)

# Directions possibles du cavalier (mouvements en L)
DIRECTIONS = [
    (-2, 1),   # 1: haut-droite
    (-1, 2),   # 2: droite-haut
    (1, 2),    # 3: droite-bas
    (2, 1),    # 4: bas-droite
    (2, -1),   # 5: bas-gauche
    (1, -2),   # 6: gauche-bas
    (-1, -2),  # 7: gauche-haut
    (-2, -1)   # 8: haut-gauche
]

# Paramètres de l'algorithme génétique
TAILLE_POPULATION = 50
TAILLE_TOURNOI = 3
TAUX_MUTATION = 0.1
NB_GENES = 63

# Constantes de fitness
FITNESS_MAX = 64
FITNESS_MIN = 0

# Constantes de mouvement
CYCLE_AVANT = 1
CYCLE_ARRIERE = -1

# Seuils d'arrêt
MAX_GENERATIONS = 1000
FITNESS_CIBLE = 64

# Couleurs pour l'interface
COULEUR_CASE_BLANCHE = (255, 255, 255)
COULEUR_CASE_NOIRE = (200, 200, 200)
COULEUR_CAVALIER = (255, 0, 0)
COULEUR_CHEMIN = (0, 0, 255)
COULEUR_DEPART = (0, 255, 0)

# Dimensions de l'interface
TAILLE_CASE = 60
LARGEUR_FENETRE = TAILLE_ECHIQUIER * TAILLE_CASE
HAUTEUR_FENETRE = TAILLE_ECHIQUIER * TAILLE_CASE