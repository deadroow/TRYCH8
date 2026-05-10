import pygame
import sys
import os
import subprocess
import tkinter as tk
from tkinter import filedialog

# ====== CHEMINS ======
DOSSIER_MENU     = os.path.dirname(os.path.abspath(__file__))
DOSSIER_RACINE   = os.path.dirname(os.path.dirname(DOSSIER_MENU))
CHEMIN_EMULATEUR = os.path.join(DOSSIER_RACINE, "main.py")

# ====== TAILLE FENETRE ======
LARGEUR, HAUTEUR = 900, 600

# ====== PALETTE CHIP-8 (noir/vert phosphore, style terminal retro) ======
NOIR           = (0,   0,   0)
BLANC          = (255, 255, 255)
FOND           = (10,  12,  10)
PANNEAU        = (18,  22,  18)
BORDURE        = (40,  80,  40)
VERT_PRIMAIRE  = (0,   255, 80)
VERT_SURVOL    = (80,  255, 140)
ROUGE          = (200, 40,  40)
ROUGE_SURVOL   = (255, 70,  70)
TEXTE_NORMAL   = (160, 220, 160)
JAUNE          = (200, 200, 0)

# ====== ETAT DE L'APPLICATION ======
etat = {
    "chemin_rom":     None,
    "nom_rom":        "",
    "page":           "principale",
}

# ====== INIT PYGAME ======
pygame.init()

# ====== Musique ======
MUSIC_PATH = os.path.join(DOSSIER_MENU, "Chip-8_Mix.mp3")
if os.path.exists(MUSIC_PATH):
    pygame.mixer.music.load(MUSIC_PATH)
    pygame.mixer.music.play(-1)

fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("CHIP-8 Launcher")
horloge = pygame.time.Clock()

# ====== POLICES ======
police_titre   = pygame.font.SysFont("Consolas", 28, bold=True)
police_normale = pygame.font.SysFont("Consolas", 20)
police_petite  = pygame.font.SysFont("Consolas", 16)
police_clavier = pygame.font.SysFont("Consolas", 32, bold=True)

# ====== TKINTER (explorateur de fichiers) ======
fenetre_tk = tk.Tk()
fenetre_tk.withdraw()

# ====== FONCTIONS DE DESSIN ======

def dessiner_fond_rect(surf, couleur, rect, rayon=8):
    pygame.draw.rect(surf, couleur, rect, border_radius=rayon)

def dessiner_contour_rect(surf, couleur, rect, epaisseur=2, rayon=8):
    pygame.draw.rect(surf, couleur, rect, epaisseur, border_radius=rayon)

def dessiner_bouton(surf, rect, texte, police, couleur_fond, couleur_texte, couleur_bord, survol=False, rayon=10):
    surface_alpha = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    r, g, b = couleur_fond
    pygame.draw.rect(surface_alpha, (r, g, b, 220 if survol else 180),
                     (0, 0, rect.width, rect.height), border_radius=rayon)
    surf.blit(surface_alpha, rect.topleft)
    pygame.draw.rect(surf, couleur_bord, rect, 2, border_radius=rayon)
    label = police.render(texte, True, couleur_texte)
    surf.blit(label, label.get_rect(center=rect.center))

def dessiner_texte_centre(surf, texte, police, couleur, cx, cy):
    label = police.render(texte, True, couleur)
    surf.blit(label, label.get_rect(center=(cx, cy)))

def dessiner_texte_gauche(surf, texte, police, couleur, x, y):
    label = police.render(texte, True, couleur)
    surf.blit(label, (x, y))

# ====== SELECTION DE ROM ======

def choisir_rom():
    chemin = filedialog.askopenfilename(
        title="Choisir une ROM Chip-8",
        filetypes=[("ROMs Chip-8", "*.ch8 *.rom *.chip8 *.bin"), ("Tous les fichiers", "*.*")]
    )
    if chemin:
        etat["chemin_rom"] = chemin
        etat["nom_rom"]    = os.path.basename(chemin)

# ====== LANCEMENT DE L'EMULATEUR ======

def lancer_rom():
    if not etat["chemin_rom"]:
        return False
    if not os.path.isfile(CHEMIN_EMULATEUR):
        print(f"Erreur : main.py introuvable à '{CHEMIN_EMULATEUR}'")
        return False

    commande  = [sys.executable, CHEMIN_EMULATEUR, etat["chemin_rom"]]
    processus = subprocess.Popen(commande, cwd=DOSSIER_RACINE)
    pygame.display.iconify()
    processus.wait()
    # Restaure la fenêtre du launcher après fermeture de l'émulateur
    pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("CHIP-8 Launcher")
    return True

# ====== PAGE PRINCIPALE ======

def afficher_page_principale(pos_souris):
    fenetre.fill(FOND)

    dessiner_texte_centre(fenetre, "CHIP-8  LAUNCHER", police_titre, VERT_PRIMAIRE, LARGEUR // 2, 38)
    pygame.draw.line(fenetre, BORDURE, (60, 60), (LARGEUR - 60, 60), 1)

    # Bouton "Clavier" — affiche le mapping clavier Chip-8
    btn_clavier = pygame.Rect(20, 14, 130, 36)
    survol = btn_clavier.collidepoint(pos_souris)
    dessiner_bouton(fenetre, btn_clavier, "Clavier", police_petite,
                    PANNEAU, VERT_SURVOL if survol else TEXTE_NORMAL, BORDURE, survol, rayon=8)

    # Bouton "Selectionner une ROM" — ouvre l'explorateur de fichiers
    btn_rom = pygame.Rect(LARGEUR - 250, 82, 230, 56)
    survol  = btn_rom.collidepoint(pos_souris)
    dessiner_bouton(fenetre, btn_rom, "Selectionner une ROM", police_petite,
                    PANNEAU, VERT_SURVOL if survol else TEXTE_NORMAL, BORDURE, survol, rayon=8)

    # Panneau d'information sur la ROM sélectionnée
    panneau_info = pygame.Rect(60, 160, LARGEUR - 120, 120)
    dessiner_fond_rect(fenetre, PANNEAU, panneau_info, rayon=10)
    dessiner_contour_rect(fenetre, BORDURE, panneau_info, 2, rayon=10)
    dessiner_texte_gauche(fenetre, "Information", police_normale, TEXTE_NORMAL,
                          panneau_info.x + 16, panneau_info.y + 12)
    pygame.draw.line(fenetre, BORDURE,
                     (panneau_info.x + 10, panneau_info.y + 38),
                     (panneau_info.right - 10, panneau_info.y + 38), 1)

    if etat["chemin_rom"]:
        chemin_affiche = etat["chemin_rom"]
        if len(chemin_affiche) > 68:
            chemin_affiche = chemin_affiche[:68] + "..."
        dessiner_texte_gauche(fenetre, "Fichier : " + etat["nom_rom"], police_petite, BLANC,
                              panneau_info.x + 16, panneau_info.y + 48)
        dessiner_texte_gauche(fenetre, "Chemin  : " + chemin_affiche, police_petite, TEXTE_NORMAL,
                              panneau_info.x + 16, panneau_info.y + 70)

    else:
        dessiner_texte_centre(fenetre, "Aucune ROM chargee - cliquez sur ROM pour en selectionner une.",
                              police_petite, TEXTE_NORMAL, panneau_info.centerx, panneau_info.y + 70)

    # Bouton START — grisé si aucune ROM n'est chargée
    btn_start = pygame.Rect(0, 0, 360, 80)
    btn_start.center = (LARGEUR // 2, 375)
    survol    = btn_start.collidepoint(pos_souris)
    rom_prete = etat["chemin_rom"] is not None
    couleur_fond  = VERT_SURVOL   if (rom_prete and survol) else VERT_PRIMAIRE if rom_prete else PANNEAU
    couleur_bord  = VERT_SURVOL   if rom_prete else BORDURE
    couleur_texte = NOIR          if rom_prete else TEXTE_NORMAL
    dessiner_bouton(fenetre, btn_start, "START", police_titre,
                    couleur_fond, couleur_texte, couleur_bord, survol, rayon=14)

    # Bouton "Quitter"
    btn_quitter = pygame.Rect(20, HAUTEUR - 50, 110, 34)
    survol = btn_quitter.collidepoint(pos_souris)
    dessiner_bouton(fenetre, btn_quitter, "Quitter", police_petite,
                    ROUGE if not survol else ROUGE_SURVOL, BLANC, ROUGE_SURVOL, survol, rayon=8)

    return {
        "clavier":   btn_clavier,
        "rom":       btn_rom,
        "start":     btn_start,
        "quitter":   btn_quitter,
    }

# ====== PAGE CLAVIER ======

# Correspondance touche Chip-8 -> touche clavier PC
MAPPING_CLAVIER = [
    ("1","1"), ("2","2"), ("3","3"), ("C","4"),
    ("4","Q"), ("5","W"), ("6","E"), ("D","R"),
    ("7","A"), ("8","S"), ("9","D"), ("E","F"),
    ("A","Z"), ("0","X"), ("B","C"), ("F","V"),
]

def afficher_page_clavier(pos_souris):
    fenetre.fill(FOND)
    dessiner_texte_centre(fenetre, "Clavier Hexadecimal Chip-8", police_titre, VERT_PRIMAIRE, LARGEUR // 2, 38)
    pygame.draw.line(fenetre, BORDURE, (60, 60), (LARGEUR - 60, 60), 1)
    dessiner_texte_centre(fenetre, "Touche Chip-8   ->   Touche clavier PC",
                          police_petite, TEXTE_NORMAL, LARGEUR // 2, 80)

    cell_l, cell_h    = 150, 70
    grille_largeur    = 4 * cell_l + 3 * 10
    grille_x          = (LARGEUR - grille_largeur) // 2
    grille_y          = 110

    for i, (touche_chip8, touche_pc) in enumerate(MAPPING_CLAVIER):
        col   = i % 4
        ligne = i // 4
        x = grille_x + col   * (cell_l + 10)
        y = grille_y + ligne * (cell_h + 10)
        rect = pygame.Rect(x, y, cell_l, cell_h)
        dessiner_fond_rect(fenetre, PANNEAU, rect, rayon=10)
        dessiner_contour_rect(fenetre, BORDURE, rect, 2, rayon=10)
        dessiner_texte_centre(fenetre, touche_chip8, police_clavier, VERT_PRIMAIRE, x + cell_l // 3,          y + cell_h // 2)
        dessiner_texte_centre(fenetre, "->",          police_normale, BORDURE,       x + cell_l // 2,          y + cell_h // 2)
        dessiner_texte_centre(fenetre, touche_pc,     police_clavier, JAUNE,         x + cell_l * 2 // 3 + 10, y + cell_h // 2)

    btn_retour = pygame.Rect(20, HAUTEUR - 50, 120, 34)
    survol = btn_retour.collidepoint(pos_souris)
    dessiner_bouton(fenetre, btn_retour, "<- Retour", police_petite,
                    PANNEAU, VERT_SURVOL if survol else TEXTE_NORMAL, BORDURE, survol, rayon=8)
    return {"retour": btn_retour}

# ====== BOUCLE PRINCIPALE ======

en_cours      = True
msg_erreur    = ""
timer_erreur  = 0
boutons_cache = {}

while en_cours:
    LARGEUR, HAUTEUR = fenetre.get_size()
    pos_souris = pygame.mouse.get_pos()
    dt = horloge.tick(60)

    if timer_erreur > 0:
        timer_erreur -= dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clic = event.pos

            if etat["page"] == "principale":
                if boutons_cache.get("clavier") and boutons_cache["clavier"].collidepoint(clic):
                    etat["page"] = "clavier"

                elif boutons_cache.get("rom") and boutons_cache["rom"].collidepoint(clic):
                    choisir_rom()

                elif boutons_cache.get("start") and boutons_cache["start"].collidepoint(clic):
                    if etat["chemin_rom"]:
                        if not lancer_rom():
                            msg_erreur   = "Emulateur introuvable : " + CHEMIN_EMULATEUR
                            timer_erreur = 3000
                    else:
                        msg_erreur   = "Veuillez selectionner une ROM d'abord."
                        timer_erreur = 2000

                elif boutons_cache.get("quitter") and boutons_cache["quitter"].collidepoint(clic):
                    en_cours = False

            elif etat["page"] == "clavier":
                if boutons_cache.get("retour") and boutons_cache["retour"].collidepoint(clic):
                    etat["page"]  = "principale"
                    boutons_cache = {}

    # Rendu selon la page active
    if etat["page"] == "principale":
        boutons_cache = afficher_page_principale(pos_souris)
    elif etat["page"] == "clavier":
        boutons_cache = afficher_page_clavier(pos_souris)
    # Bandeau d'erreur flottant en bas de l'écran
    if timer_erreur > 0:
        surf_erreur = pygame.Surface((580, 40), pygame.SRCALPHA)
        pygame.draw.rect(surf_erreur, (160, 20, 20, 210), (0, 0, 580, 40), border_radius=8)
        fenetre.blit(surf_erreur, (LARGEUR // 2 - 290, HAUTEUR - 100))
        dessiner_texte_centre(fenetre, msg_erreur, police_petite, BLANC, LARGEUR // 2, HAUTEUR - 80)

    pygame.display.flip()

pygame.quit()
fenetre_tk.destroy()
sys.exit()
