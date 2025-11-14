import pygame
import sys
import time
from constantes import *

class KnightTourVisualizer:
    def __init__(self, knight):
        self.knight = knight
        self.current_step = 0
        self.animation_speed = 500  # ms entre les étapes
        self.last_step_time = 0
        self.paused = False
        self.show_numbers = True
        self.show_path = True
        
        pygame.init()
        self.screen = pygame.display.set_mode((LARGEUR_FENETRE + 300, HAUTEUR_FENETRE))  # +300 pour le panneau latéral
        pygame.display.set_caption(" Knight's Tour - Solution Optimale")
        self.clock = pygame.time.Clock()
        
        # Charger les polices
        self.font_small = pygame.font.SysFont('Arial', 14)
        self.font_medium = pygame.font.SysFont('Arial', 18, bold=True)
        self.font_large = pygame.font.SysFont('Arial', 24, bold=True)
        
        # Couleurs modernes
        self.colors = {
            'background': (240, 240, 245),
            'panel': (50, 50, 60),
            'text': (255, 255, 255),
            'text_dark': (30, 30, 30),
            'white_square': (235, 236, 208),
            'black_square': (119, 149, 86),
            'path': (65, 105, 225),
            'knight': (220, 20, 60),
            'start': (50, 205, 50),
            'visited': (30, 144, 255),
            'button': (70, 130, 180),
            'button_hover': (100, 160, 210)
        }
        
        # Boutons
        self.buttons = {
            'play_pause': {'rect': pygame.Rect(LARGEUR_FENETRE + 50, 400, 200, 40), 'text': '⏸ Pause'},
            'reset': {'rect': pygame.Rect(LARGEUR_FENETRE + 50, 450, 200, 40), 'text': ' Recommencer'},
            'faster': {'rect': pygame.Rect(LARGEUR_FENETRE + 50, 500, 95, 35), 'text': ' +'},
            'slower': {'rect': pygame.Rect(LARGEUR_FENETRE + 155, 500, 95, 35), 'text': ' -'},
            'toggle_numbers': {'rect': pygame.Rect(LARGEUR_FENETRE + 50, 550, 200, 35), 'text': ' Numéros: ON'},
            'toggle_path': {'rect': pygame.Rect(LARGEUR_FENETRE + 50, 590, 200, 35), 'text': ' Chemin: ON'}
        }
    
    def draw_chessboard(self):
        """Dessine l'échiquier avec un style moderne"""
        for row in range(TAILLE_ECHIQUIER):
            for col in range(TAILLE_ECHIQUIER):
                color = self.colors['white_square'] if (row + col) % 2 == 0 else self.colors['black_square']
                pygame.draw.rect(self.screen, color, 
                               (col * TAILLE_CASE, row * TAILLE_CASE, 
                                TAILLE_CASE, TAILLE_CASE))
                
                # Coordonnées de la case
                coord_text = self.font_small.render(f"{chr(97+col)}{8-row}", True, self.colors['text_dark'])
                self.screen.blit(coord_text, (col * TAILLE_CASE + 2, row * TAILLE_CASE + 2))
    
    def draw_knight_path(self):
        """Dessine le chemin du cavalier avec animation"""
        if len(self.knight.path) < 2 or not self.show_path:
            return
        
        # Dessiner les lignes entre les positions (jusqu'à l'étape actuelle)
        for i in range(min(self.current_step, len(self.knight.path) - 1)):
            start_pos = self.knight.path[i]
            end_pos = self.knight.path[i + 1]
            
            start_pixel = (start_pos[1] * TAILLE_CASE + TAILLE_CASE // 2,
                         start_pos[0] * TAILLE_CASE + TAILLE_CASE // 2)
            end_pixel = (end_pos[1] * TAILLE_CASE + TAILLE_CASE // 2,
                       end_pos[0] * TAILLE_CASE + TAILLE_CASE // 2)
            
            # Gradient de couleur selon la progression
            alpha = min(255, 100 + (i * 155 // len(self.knight.path)))
            path_color = (65, 105, 225, alpha)
            
            pygame.draw.line(self.screen, path_color, start_pixel, end_pixel, 4)
        
        # Dessiner les points sur chaque case visitée (jusqu'à l'étape actuelle)
        for i in range(min(self.current_step + 1, len(self.knight.path))):
            pos = self.knight.path[i]
            pixel_pos = (pos[1] * TAILLE_CASE + TAILLE_CASE // 2,
                       pos[0] * TAILLE_CASE + TAILLE_CASE // 2)
            
            # Case de départ en vert
            if i == 0:
                pygame.draw.circle(self.screen, self.colors['start'], pixel_pos, 10)
                pygame.draw.circle(self.screen, (255, 255, 255), pixel_pos, 6)
            else:
                pygame.draw.circle(self.screen, self.colors['visited'], pixel_pos, 8)
            
            # Numéroter les cases si activé
            if self.show_numbers:
                text_color = (255, 255, 255) if (pos[0] + pos[1]) % 2 == 0 else (255, 255, 255)
                text = self.font_small.render(str(i), True, text_color)
                text_rect = text.get_rect(center=(pixel_pos[0], pixel_pos[1]))
                self.screen.blit(text, text_rect)
    
    def draw_knight(self):
        """Dessine le cavalier à sa position actuelle avec un style graphique"""
        if self.knight.path and self.current_step < len(self.knight.path):
            current_pos = self.knight.path[self.current_step]
            knight_pixel = (current_pos[1] * TAILLE_CASE + TAILLE_CASE // 2,
                          current_pos[0] * TAILLE_CASE + TAILLE_CASE // 2)
            
            # Cercle externe
            pygame.draw.circle(self.screen, self.colors['knight'], knight_pixel, 15)
            # Cercle interne
            pygame.draw.circle(self.screen, (255, 255, 255), knight_pixel, 10)
            # Symbole du cavalier
            knight_symbol = self.font_medium.render("♞", True, self.colors['knight'])
            symbol_rect = knight_symbol.get_rect(center=knight_pixel)
            self.screen.blit(knight_symbol, symbol_rect)
    
    def draw_sidebar(self):
        """Dessine le panneau latéral avec informations et contrôles"""
        # Fond du panneau
        pygame.draw.rect(self.screen, self.colors['panel'], 
                        (LARGEUR_FENETRE, 0, 300, HAUTEUR_FENETRE))
        
        # Titre
        title = self.font_large.render("♞ Knight's Tour", True, self.colors['text'])
        self.screen.blit(title, (LARGEUR_FENETRE + 50, 30))
        
        # Informations sur la solution
        info_lines = [
            f"Fitness: {self.knight.fitness}/64",
            f"Cases visitées: {len(self.knight.visited)}",
            f"Longueur du chemin: {len(self.knight.path)}",
            f"Étape actuelle: {self.current_step}/{len(self.knight.path)-1}",
            f"Vitesse: {1000//self.animation_speed}x",
            f"Statut: {'Complet' if self.knight.fitness == 64 else 'Partiel'}"
        ]
        
        for i, line in enumerate(info_lines):
            text = self.font_medium.render(line, True, self.colors['text'])
            self.screen.blit(text, (LARGEUR_FENETRE + 50, 100 + i * 30))
        
        # Barre de progression
        progress = self.current_step / max(1, len(self.knight.path) - 1)
        pygame.draw.rect(self.screen, (100, 100, 100), 
                        (LARGEUR_FENETRE + 50, 280, 200, 20), border_radius=10)
        pygame.draw.rect(self.screen, self.colors['path'], 
                        (LARGEUR_FENETRE + 50, 280, int(200 * progress), 20), border_radius=10)
        
        # Légende
        legend_y = 320
        legend_items = [
            (self.colors['start'], "Départ"),
            (self.colors['knight'], "Cavalier actuel"),
            (self.colors['visited'], "Case visitée"),
            (self.colors['path'], "Chemin parcouru")
        ]
        
        for color, text in legend_items:
            pygame.draw.rect(self.screen, color, (LARGEUR_FENETRE + 50, legend_y, 20, 20))
            legend_text = self.font_small.render(text, True, self.colors['text'])
            self.screen.blit(legend_text, (LARGEUR_FENETRE + 80, legend_y))
            legend_y += 30
        
        # Dessiner les boutons
        mouse_pos = pygame.mouse.get_pos()
        for button_id, button_data in self.buttons.items():
            button_rect = button_data['rect']
            is_hovered = button_rect.collidepoint(mouse_pos)
            
            color = self.colors['button_hover'] if is_hovered else self.colors['button']
            pygame.draw.rect(self.screen, color, button_rect, border_radius=8)
            pygame.draw.rect(self.screen, self.colors['text'], button_rect, 2, border_radius=8)
            
            text = self.font_medium.render(button_data['text'], True, self.colors['text'])
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
    
    def handle_buttons(self, mouse_pos):
        """Gère les clics sur les boutons"""
        for button_id, button_data in self.buttons.items():
            if button_data['rect'].collidepoint(mouse_pos):
                if button_id == 'play_pause':
                    self.paused = not self.paused
                    button_data['text'] = ' Play' if self.paused else '⏸ Pause'
                elif button_id == 'reset':
                    self.current_step = 0
                    self.last_step_time = time.time() * 1000
                elif button_id == 'faster':
                    self.animation_speed = max(50, self.animation_speed // 2)
                elif button_id == 'slower':
                    self.animation_speed = min(2000, self.animation_speed * 2)
                elif button_id == 'toggle_numbers':
                    self.show_numbers = not self.show_numbers
                    button_data['text'] = f" Numéros: {'ON' if self.show_numbers else 'OFF'}"
                elif button_id == 'toggle_path':
                    self.show_path = not self.show_path
                    button_data['text'] = f" Chemin: {'ON' if self.show_path else 'OFF'}"
                return True
        return False
    
    def update_animation(self):
        """Met à jour l'animation automatiquement"""
        current_time = time.time() * 1000
        
        if not self.paused and current_time - self.last_step_time > self.animation_speed:
            if self.current_step < len(self.knight.path) - 1:
                self.current_step += 1
            self.last_step_time = current_time
    
    def run(self):
        """Lance la visualisation améliorée"""
        self.last_step_time = time.time() * 1000
        running = True
        
        while running:
            current_time = time.time() * 1000
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                        self.buttons['play_pause']['text'] = ' Play' if self.paused else ' Pause'
                    elif event.key == pygame.K_RIGHT and self.paused:
                        self.current_step = min(self.current_step + 1, len(self.knight.path) - 1)
                    elif event.key == pygame.K_LEFT and self.paused:
                        self.current_step = max(self.current_step - 1, 0)
                    elif event.key == pygame.K_r:
                        self.current_step = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        self.handle_buttons(mouse_pos)
            
            # Mettre à jour l'animation
            self.update_animation()
            
            # Dessiner l'interface
            self.screen.fill(self.colors['background'])
            self.draw_chessboard()
            self.draw_knight_path()
            self.draw_knight()
            self.draw_sidebar()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

def afficher_solution(knight):
    """Fonction utilitaire pour afficher une solution"""
    visualizer = KnightTourVisualizer(knight)
    visualizer.run()