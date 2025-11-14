import random
from knight import Knight
from constantes import *

class Population:
    def __init__(self, population_size):
        self.population_size = population_size
        self.generation = 1
        self.knights = [Knight() for _ in range(population_size)]
    
    def check_population(self):
        """Vérifie la validité des mouvements de tous les cavaliers"""
        for knight in self.knights:
            knight.check_moves()
    
    def evaluate(self):
        """Évalue la fitness de tous les cavaliers et retourne le meilleur"""
        best_fitness = 0
        best_knight = None
        
        for knight in self.knights:
            fitness = knight.evaluate_fitness()
            if fitness > best_fitness:
                best_fitness = fitness
                best_knight = knight
        
        return best_fitness, best_knight
    
    def tournament_selection(self, tournament_size):
        """Sélection par tournoi"""
        participants = random.sample(self.knights, tournament_size)
        participants.sort(key=lambda x: x.fitness, reverse=True)
        return participants[0], participants[1]  # Retourne les 2 meilleurs
    
    def create_new_generation(self):
        """Crée une nouvelle génération"""
        new_knights = []
        
        while len(new_knights) < self.population_size:
            # Sélection des parents
            parent1, parent2 = self.tournament_selection(TAILLE_TOURNOI)
            
            # Croisement
            child1_chromosome, child2_chromosome = parent1.chromosome.crossover(parent2.chromosome)
            
            # Mutation
            child1_chromosome.mutation()
            child2_chromosome.mutation()
            
            # Création des nouveaux cavaliers
            child1 = Knight(child1_chromosome)
            child2 = Knight(child2_chromosome)
            
            new_knights.extend([child1, child2])
        
        # Ajuster la taille si nécessaire
        self.knights = new_knights[:self.population_size]
        self.generation += 1
    
    def get_average_fitness(self):
        """Calcule la fitness moyenne de la population"""
        total_fitness = sum(knight.fitness for knight in self.knights)
        return total_fitness / self.population_size
    
    def __str__(self):
        avg_fitness = self.get_average_fitness()
        best_fitness, _ = self.evaluate()
        return f"Population(generation={self.generation}, avg_fitness={avg_fitness:.2f}, best_fitness={best_fitness})"