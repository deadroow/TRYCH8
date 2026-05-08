import pygame
 
# Correspondance touches clavier -> touches CHIP-8 (0x0 à 0xF)
TOUCHES = {
    pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
    pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
    pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
    pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF,
}
 
 
class DetectionTouche:
 
    def __init__(self):
        # Etat de chaque touche CHIP-8 : True = enfoncée, False = relachée
        self.etat = {i: False for i in range(16)}
 
    def mise_a_jour(self, event):
        # A appeler pour chaque event pygame dans la boucle principale
        if event.type == pygame.KEYDOWN and event.key in TOUCHES:
            self.etat[TOUCHES[event.key]] = True
 
        elif event.type == pygame.KEYUP and event.key in TOUCHES:
            self.etat[TOUCHES[event.key]] = False
 
    def est_enfoncee(self, touche):
        # Retourne True si la touche CHIP-8 (0x0-0xF) est enfoncée
        return self.etat.get(touche, False)
 
    def attendre_touche(self):
        # Bloque jusqu'à ce que le joueur appuie sur une touche
        # Retourne le numéro de la touche CHIP-8 pressée
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.KEYDOWN and event.key in TOUCHES:
                    return TOUCHES[event.key]
