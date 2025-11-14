#  Projet RP - Résolution du Knight's Tour par Algorithme Génétique

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![PyGame](https://img.shields.io/badge/PyGame-2.5%2B-orange)](https://pygame.org)
[![IA](https://img.shields.io/badge/Intelligence-Artificielle-green)](https://github.com/HamzaElhadjen/Projet-rp-mouvements-cavalier)

Une implémentation complète du problème du **Knight's Tour** résolu à l'aide d'un **algorithme génétique** avec interface de visualisation interactive.

##  Présentation du Problème

Le **Knight's Tour** est un problème mathématique et algorithmique où un cavalier aux échecs doit visiter chaque case d'un échiquier exactement une fois. Ce projet utilise un algorithme génétique pour trouver des solutions optimales à ce problème classique.

##  Fonctionnalités

###  Algorithme Génétique
- **Sélection par tournoi** (taille 3)
- **Croisement à point unique** (single-point crossover)
- **Mutation probabiliste** avec taux configurable
- **Population évolutive** de 50 individus

###  Mouvements du Cavalier
- Validation intelligente des 8 directions en L
- Correction automatique des mouvements invalides
- Gestion des collisions et limites de l'échiquier

###  Interface Interactive
- Visualisation temps réel avec PyGame
- Contrôles : Play/Pause, vitesse, reset
- Affichage des numéros de parcours
- Barre de progression et statistiques

##  Installation et Exécution

### Prérequis
- Python 3.8 ou supérieur
- PyGame 2.5+

### Installation
```bash
# Cloner le repository
git clone https://github.com/HamzaElhadjen/Projet-rp-mouvements-cavalier.git
cd Projet-rp-mouvements-cavalier

# Installer les dépendances
pip install pygame
