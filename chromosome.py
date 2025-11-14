import random
from constantes import *

class Chromosome:
    def __init__(self, genes=None):
        if genes is None:
            self.genes = [random.randint(1, 8) for _ in range(NB_GENES)]
        else:
            self.genes = genes.copy()
    
    def crossover(self, partner):
        # Croisement à un point
        point_croisement = random.randint(1, NB_GENES - 2)
        
        genes_enfant1 = self.genes[:point_croisement] + partner.genes[point_croisement:]
        genes_enfant2 = partner.genes[:point_croisement] + self.genes[point_croisement:]
        
        return Chromosome(genes_enfant1), Chromosome(genes_enfant2)
    
    def mutation(self):
        for i in range(len(self.genes)):
            if random.random() < TAUX_MUTATION:
                self.genes[i] = random.randint(1, 8)
    
    def __str__(self):
        return f"Chromosome({self.genes[:5]}...)"  # Affiche seulement les 5 premiers gènes