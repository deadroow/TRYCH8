import pygame
def drawScreen(self):
        # Couleurs : bleu clair pour les pixels allumés, bleu très foncé pour le fond
        # Ça donne un style rétro sympa
        onPixel = (139, 200, 254)
        offPixel = (5, 27, 44)

        # On remplit tout l'écran avec la couleur de fond
        self.screen.fill(offPixel)

        # Surface de 10x10 pixels pour dessiner chaque "gros pixel"
        pixel_surface = pygame.Surface((10, 10))
        pixel_surface.set_alpha(255)

        for i in range(len(self.display_buffer)):
            # Conversion index linéaire -> coordonnées (x, y) sur l'écran agrandi
            x = (i % 64) * 10
            y = (i // 64) * 10

            if self.display_buffer[i] == 1:
                # Pixel allumé : alpha à fond
                self.pixel_alpha[i] = 255
            else:
                # Pixel éteint : on diminue l'alpha progressivement
                # Ça fait un effet de phosphore comme les vieux écrans cathodiques
                # Le pixel ne disparaît pas d'un coup, il fade out
                self.pixel_alpha[i] = max(0, self.pixel_alpha[i] - 25)

            # On dessine le pixel seulement s'il a encore un peu de transparence
            if self.pixel_alpha[i] > 0:
                pixel_surface.fill(onPixel)
                pixel_surface.set_alpha(self.pixel_alpha[i])
                self.screen.blit(pixel_surface, (x, y))

        pygame.display.update()