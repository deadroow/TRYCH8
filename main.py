import sys
from app.Ecran import Ecran
from app.chip8 import chip_8
from app.DetectionTouche import DetectionTouche
from app.ROM.chargerROM import ROM
import pygame

def main():
    rom_path = sys.argv[1] if len(sys.argv) > 1 else None

    if not rom_path:
        print("Usage : python main.py <chemin_vers_rom.ch8>")
        sys.exit(1)

    # Init des composants
    ecran      = Ecran()
    clavier    = DetectionTouche()
    cpu        = chip_8(clavier=clavier)   # clavier injecté dans le CPU
    rom_loader = ROM()

    # Charge la ROM dans la mémoire du CPU
    rom_loader.load.__func__(cpu, path=rom_path)

    clock = pygame.time.Clock()
    running = True

    while running:
        # Gestion des événements pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            clavier.mise_a_jour(event)

        # Synchronise l'état du clavier dans le CPU
        cpu.etat_touche = [clavier.est_enfoncee(i) for i in range(16)]

        # Exécute plusieurs cycles CPU par frame (vitesse ~700 instructions/sec)
        for _ in range(10):
            cpu.cycle()

        # Décrémente les timers (60 Hz)
        if cpu.delay_timer > 0:
            cpu.delay_timer -= 1
        if cpu.sound_timer > 0:
            cpu.sound_timer -= 1

        # Copie le buffer du CPU vers l'écran et affiche
        ecran.display_buffer = cpu.ecran[:]
        ecran.render()

        clock.tick(60)

    ecran.quit()

if __name__ == "__main__":
    main()

