import random
from constantes import *
from chromosome import Chromosome

class Knight:
    def __init__(self, chromosome=None):
        self.chromosome = chromosome if chromosome else Chromosome()
        self.position = CASE_DEPART
        self.path = [CASE_DEPART]
        self.fitness = 0
        self.visited = set([CASE_DEPART])
    
    def move_forward(self, direction):
        """Déplace le cavalier dans la direction spécifiée"""
        dx, dy = DIRECTIONS[direction - 1]  # -1 car les directions sont indexées à 0
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy
        return (new_x, new_y)
    
    def move_backward(self, direction):
        """Annule le mouvement dans la direction spécifiée"""
        dx, dy = DIRECTIONS[direction - 1]
        new_x = self.position[0] - dx
        new_y = self.position[1] - dy
        return (new_x, new_y)
    
    def is_valid_position(self, position):
        """Vérifie si la position est dans l'échiquier"""
        x, y = position
        return 0 <= x < TAILLE_ECHIQUIER and 0 <= y < TAILLE_ECHIQUIER
    
    def check_moves(self):
        """Vérifie et corrige les mouvements du chromosome"""
        # Réinitialiser la position et le chemin
        self.position = CASE_DEPART
        self.path = [CASE_DEPART]
        self.visited = set([CASE_DEPART])
        
        # Choisir aléatoirement le sens du cycle
        cycle_direction = random.choice([CYCLE_AVANT, CYCLE_ARRIERE])
        
        for i in range(len(self.chromosome.genes)):
            original_direction = self.chromosome.genes[i]
            current_direction = original_direction
            move_applied = False
            
            # Essayer les 8 directions possibles
            for attempt in range(8):
                new_position = self.move_forward(current_direction)
                
                if (self.is_valid_position(new_position) and 
                    new_position not in self.visited):
                    
                    # Mouvement valide
                    self.position = new_position
                    self.path.append(new_position)
                    self.visited.add(new_position)
                    self.chromosome.genes[i] = current_direction
                    move_applied = True
                    break
                
                # Essayer la direction suivante selon le cycle
                if cycle_direction == CYCLE_AVANT:
                    current_direction = (current_direction % 8) + 1
                else:
                    current_direction = ((current_direction - 2) % 8) + 1
            
            # Si aucun mouvement valide n'a été trouvé, garder le dernier mouvement
            if not move_applied:
                new_position = self.move_forward(self.chromosome.genes[i])
                if self.is_valid_position(new_position):
                    self.position = new_position
                    self.path.append(new_position)
                    self.visited.add(new_position)
    
    def evaluate_fitness(self):
        """Évalue la fitness du cavalier"""
        self.fitness = len(self.visited)
        return self.fitness
    
    def __str__(self):
        return f"Knight(fitness={self.fitness}, path_length={len(self.path)})"