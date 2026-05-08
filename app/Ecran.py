import pygame

CHIP8_WIDTH  = 64
CHIP8_HEIGHT = 32
PIXEL_SCALE  = 10

# Couleurs style rétro cathodique
ON_PIXEL  = (139, 200, 254)   # pixel allumé
OFF_PIXEL = (5,   27,  44)    # fond


class Ecran:

    def __init__(self):
        pygame.init()

        # Fenêtre de 640×320 (64×32 pixels CHIP-8 × 10)
        self.ecrand = pygame.display.set_mode(
            (CHIP8_WIDTH * PIXEL_SCALE, CHIP8_HEIGHT * PIXEL_SCALE)
        )
        pygame.display.set_caption("CHIP-8 Emulator")

        # Buffer logique : 0 = éteint, 1 = allumé
        self.display_buffer = [0] * (CHIP8_WIDTH * CHIP8_HEIGHT)

        # Niveau d'alpha par pixel pour l'effet phosphore
        self.pixel_alpha    = [0] * (CHIP8_WIDTH * CHIP8_HEIGHT)

        # Surface réutilisable pour dessiner chaque gros pixel
        self._pixel_surf = pygame.Surface((PIXEL_SCALE, PIXEL_SCALE))
        self._pixel_surf.set_alpha(255)

    def clear(self):
        self.display_buffer = [0] * (CHIP8_WIDTH * CHIP8_HEIGHT)

    def draw_sprite(self, x, y, sprite):
        collision = False

        for row, byte in enumerate(sprite):
            for col in range(8):
                # Bit de poids fort en premier
                if byte & (0x80 >> col):
                    px  = (x + col) % CHIP8_WIDTH
                    py  = (y + row) % CHIP8_HEIGHT
                    idx = py * CHIP8_WIDTH + px

                    if self.display_buffer[idx] == 1:
                        collision = True  # XOR : 1 ⊕ 1 = 0 → collision
                    self.display_buffer[idx] ^= 1

        return collision

    def render(self):
        self.ecrand.fill(OFF_PIXEL)

        for i, state in enumerate(self.display_buffer):
            x = (i % CHIP8_WIDTH)  * PIXEL_SCALE
            y = (i // CHIP8_WIDTH) * PIXEL_SCALE

            if state == 1:
                self.pixel_alpha[i] = 255
            else:
                # Effet phosphore : fade-out progressif
                self.pixel_alpha[i] = max(0, self.pixel_alpha[i] - 25)

            if self.pixel_alpha[i] > 0:
                self._pixel_surf.fill(ON_PIXEL)
                self._pixel_surf.set_alpha(self.pixel_alpha[i])
                self.ecrand.blit(self._pixel_surf, (x, y))

        pygame.display.update()

    def quit(self):
        pygame.quit()
