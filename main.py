from population import Population
from interface import afficher_solution
from constantes import *

def main():
    print(" Démarrage de la résolution du Knight's Tour par Algorithme Génétique")
    print(f" Taille de la population: {TAILLE_POPULATION}")
    print(f" Fitness cible: {FITNESS_CIBLE}")
    print("=" * 50)
    
    # Créer la population initiale
    population = Population(TAILLE_POPULATION)
    
    generation_count = 0
    
    while generation_count < MAX_GENERATIONS:
        # Vérifier la validité de la population actuelle
        population.check_population()
        
        # Évaluer la génération actuelle
        max_fitness, best_knight = population.evaluate()
        
        # Afficher les statistiques
        if generation_count % 10 == 0:
            avg_fitness = population.get_average_fitness()
            print(f"Génération {generation_count:3d} | Fitness max: {max_fitness:2d} | Fitness moyenne: {avg_fitness:5.2f}")
        
        # Vérifier la condition d'arrêt
        if max_fitness == FITNESS_CIBLE:
            print("\n SOLUTION TROUVÉE ")
            print(f" Génération: {generation_count}")
            print(f" Fitness: {max_fitness}")
            print(f" Cases visitées: {len(best_knight.visited)}")
            break
        
        # Générer la nouvelle population
        population.create_new_generation()
        generation_count += 1
    else:
        print(f"\n Arrêt après {MAX_GENERATIONS} générations")
        _, best_knight = population.evaluate()
    
    # Afficher la meilleure solution
    print("\n  Lancement de la visualisation...")
    afficher_solution(best_knight)

if __name__ == "__main__":
    main()