import pygame

CHIP8_LARGEUR = 64
CHIP8_HAUTEUR = 32

PIXEL_ALLUME = (139, 200, 254)
PIXEL_ETEINT = (5,   27,  44)


class Ecran:

    def __init__(self, largeur_fenetre=640, hauteur_fenetre=320):
        # Ne pas appeler pygame.init() ici — c'est fait dans main.py

        echelle_x    = largeur_fenetre // CHIP8_LARGEUR
        echelle_y    = hauteur_fenetre // CHIP8_HAUTEUR
        self.echelle = min(echelle_x, echelle_y)

        self.fenetre = pygame.display.set_mode(
            (CHIP8_LARGEUR * self.echelle, CHIP8_HAUTEUR * self.echelle)
        )
        pygame.display.set_caption("CHIP-8 Emulator")

        # Buffer logique : 0 = éteint, 1 = allumé
        self.display_buffer = [0] * (CHIP8_LARGEUR * CHIP8_HAUTEUR)
        self.pixel_alpha    = [0] * (CHIP8_LARGEUR * CHIP8_HAUTEUR)

        # Surface réutilisable pour dessiner chaque gros pixel
        self._pixel_surf    = pygame.Surface((self.echelle, self.echelle))
        self._pixel_surf.set_alpha(255)

    def clear(self):
        self.display_buffer = [0] * (CHIP8_LARGEUR * CHIP8_HAUTEUR)

    def render(self):
        self.fenetre.fill(PIXEL_ETEINT)

        for i, allume in enumerate(self.display_buffer):
            x = (i % CHIP8_LARGEUR)  * self.echelle
            y = (i // CHIP8_LARGEUR) * self.echelle

            if allume:
                self.pixel_alpha[i] = 255
            else:
                # Effet phosphore : fade-out progressif quand le pixel s'éteint
                self.pixel_alpha[i] = max(0, self.pixel_alpha[i] - 25)

            if self.pixel_alpha[i] > 0:
                self._pixel_surf.fill(PIXEL_ALLUME)
                self._pixel_surf.set_alpha(self.pixel_alpha[i])
                self.fenetre.blit(self._pixel_surf, (x, y))

        pygame.display.update()

    def quit(self):
        pygame.quit()
