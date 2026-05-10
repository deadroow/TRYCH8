import sys
import pygame
from app.Ecran import Ecran
from app.chip8 import chip_8
from app.DetectionTouche import DetectionTouche
from app.ROM.chargerROM import ROM

RESOLUTIONS = {
    "moyen": (1024, 512),
    "grand": (1280, 640),
}

def main():
    if len(sys.argv) < 2:
        print("Usage : python main.py <chemin_rom.ch8> [moyen|grand]")
        sys.exit(1)

    chemin_rom       = sys.argv[1]
    choix_taille     = sys.argv[2] if len(sys.argv) > 2 else "moyen"
    largeur, hauteur = RESOLUTIONS.get(choix_taille, (1024, 512))

    # Un seul pygame.init() pour tout le processus
    pygame.init()

    ecran      = Ecran(largeur_fenetre=largeur, hauteur_fenetre=hauteur)
    clavier    = DetectionTouche()
    cpu        = chip_8(clavier=clavier)
    rom_loader = ROM()

    rom_loader.load.__func__(cpu, path=chemin_rom)

    horloge  = pygame.time.Clock()
    en_cours = True

    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            clavier.mise_a_jour(event)

        cpu.etat_touche = [clavier.est_enfoncee(i) for i in range(16)]

        for _ in range(12):
            cpu.cycle()

        if cpu.delay_timer > 0:
            cpu.delay_timer -= 1
        if cpu.sound_timer > 0:
            cpu.sound_timer -= 1

        ecran.display_buffer = cpu.ecran[:]
        ecran.render()

        horloge.tick(60)

    ecran.quit()

if __name__ == "__main__":
    main()
