import pygame
import sys
import os
import subprocess
import time
import tkinter as tk
from tkinter import filedialog

# ====== CONFIGURATION ======
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WIDTH, HEIGHT = 900, 600

# Couleurs
NOIR         = (0,   0,   0)
BLANC        = (255, 255, 255)
GRIS_FOND    = (18,  18,  28)
GRIS_PANEL   = (30,  30,  45)
GRIS_BORD    = (60,  60,  90)
VERT         = (57,  255, 130)
VERT_SURVOL  = (100, 255, 160)
ROUGE        = (220, 60,  60)
ROUGE_SURVOL = (255, 90,  90)
BLEU         = (60,  130, 220)
BLEU_SURVOL  = (90,  160, 255)
JAUNE        = (255, 220, 60)
TEXTE_INFO   = (180, 180, 220)

# Presets resolution
PRESETS_TAILLE  = ["Petit (512x256)", "Moyen (1024x512)", "Grand (1280x640)"]
PRESETS_VALEURS = [(512, 256), (1024, 512), (1280, 640)]

# Palette unique
PALETTES = [
    {"nom": "Classique (Noir/Vert)", "on": (57, 255, 130), "off": (18, 18, 28)},
]

# Chemin vers l'emulateur chip8 (a adapter)
EMULATEUR_PATH = os.path.join(BASE_DIR, "chip8.py")

# ====== Etat global ======
state = {
    "rom_path":    None,
    "rom_name":    "",
    "preset_idx":  1,
    "palette_idx": 0,
    "page":        "main",
}

# Etat temporaire pour les parametres (applique seulement sur "Appliquer")
settings_tmp = {
    "preset_idx":  state["preset_idx"],
    "palette_idx": state["palette_idx"],
}

# ====== Pygame init ======
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chip-8 Launcher")
clock = pygame.time.Clock()

# ====== Polices ======
font_titre   = pygame.font.SysFont("Consolas", 28, bold=True)
font_normal  = pygame.font.SysFont("Consolas", 20)
font_small   = pygame.font.SysFont("Consolas", 16)
font_clavier = pygame.font.SysFont("Consolas", 32, bold=True)

# ====== Tkinter cache ======
root = tk.Tk()
root.withdraw()

# ====== Utilitaires dessin ======
def draw_rect_fill(surf, color, rect, radius=8):
    pygame.draw.rect(surf, color, rect, border_radius=radius)

def draw_rect_outline(surf, color, rect, width=2, radius=8):
    pygame.draw.rect(surf, color, rect, width, border_radius=radius)

def draw_button(surf, rect, text, font, color_bg, color_text, color_border, hover=False, radius=10):
    alpha_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    r, g, b = color_bg
    pygame.draw.rect(alpha_surf, (r, g, b, 210 if hover else 170),
                     (0, 0, rect.width, rect.height), border_radius=radius)
    surf.blit(alpha_surf, rect.topleft)
    pygame.draw.rect(surf, color_border, rect, 2, border_radius=radius)
    label = font.render(text, True, color_text)
    lrect = label.get_rect(center=rect.center)
    surf.blit(label, lrect)

def draw_text_center(surf, text, font, color, cx, cy):
    label = font.render(text, True, color)
    surf.blit(label, label.get_rect(center=(cx, cy)))

def draw_text_left(surf, text, font, color, x, y):
    label = font.render(text, True, color)
    surf.blit(label, (x, y))

def draw_gear(surf, cx, cy, rayon, color, epaisseur=3, dents=10):
    import math
    r_ext  = rayon
    r_int  = rayon * 0.65
    r_trou = rayon * 0.28
    n = dents * 2
    pts = []
    for i in range(n):
        angle = math.pi * 2 * i / n - math.pi / 2
        r = r_ext if (i % 2 == 0) else r_int
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    pygame.draw.polygon(surf, color, pts, epaisseur)
    pygame.draw.circle(surf, color, (cx, cy), int(r_trou), epaisseur)

# ====== Selection de ROM ======
def choisir_rom():
    path = filedialog.askopenfilename(
        title="Choisir une ROM Chip-8",
        filetypes=[("ROMs Chip-8", "*.ch8 *.rom *.chip8 *.bin"), ("Tous les fichiers", "*.*")]
    )
    if path:
        state["rom_path"] = path
        state["rom_name"] = os.path.basename(path)

# ====== Lancer la ROM ======
def lancer_rom():
    if not state["rom_path"] or not os.path.exists(EMULATEUR_PATH):
        return False
    w, h = PRESETS_VALEURS[state["preset_idx"]]
    pal   = PALETTES[state["palette_idx"]]
    on_s  = f"{pal['on'][0]},{pal['on'][1]},{pal['on'][2]}"
    off_s = f"{pal['off'][0]},{pal['off'][1]},{pal['off'][2]}"
    cmd = [sys.executable, EMULATEUR_PATH, state["rom_path"],
           "--width", str(w), "--height", str(h),
           "--color-on", on_s, "--color-off", off_s]
    process = subprocess.Popen(cmd, cwd=os.path.dirname(EMULATEUR_PATH))
    time.sleep(0.15)
    pygame.display.iconify()
    process.wait()
    pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chip-8 Launcher")
    return True


# ====== PAGE PRINCIPALE ======
def draw_main(mouse_pos):
    screen.fill(GRIS_FOND)

    draw_text_center(screen, "CHIP-8  LAUNCHER", font_titre, VERT, WIDTH // 2, 38)
    pygame.draw.line(screen, GRIS_BORD, (60, 60), (WIDTH - 60, 60), 1)

    # Bouton Clavier (haut gauche)
    btn_clavier = pygame.Rect(20, 14, 130, 36)
    hov = btn_clavier.collidepoint(mouse_pos)
    draw_button(screen, btn_clavier, "Clavier", font_small,
                BLEU if not hov else BLEU_SURVOL, BLANC, BLEU_SURVOL, hov, radius=8)

    # Zone ROM (haut droite)
    if state["rom_path"]:
        panel_rom = pygame.Rect(WIDTH - 360, 80, 200, 60)
        draw_rect_fill(screen, GRIS_PANEL, panel_rom, radius=8)
        draw_rect_outline(screen, GRIS_BORD, panel_rom, 2, radius=8)
        nom = state["rom_name"]
        while nom and font_normal.size(nom)[0] > panel_rom.width - 16:
            nom = nom[:-1]
        if nom != state["rom_name"]:
            nom += "..."
        draw_text_left(screen, nom, font_normal, VERT, panel_rom.x + 8, panel_rom.y + 18)

    btn_rom = pygame.Rect(WIDTH - 250, 82, 230, 56)
    hov = btn_rom.collidepoint(mouse_pos)
    draw_button(screen, btn_rom, "Selectionner une ROM", font_small,
                BLEU if not hov else BLEU_SURVOL, BLANC, BLEU_SURVOL, hov, radius=8)

    # Panel Information
    panel_info = pygame.Rect(60, 160, WIDTH - 120, 120)
    draw_rect_fill(screen, GRIS_PANEL, panel_info, radius=10)
    draw_rect_outline(screen, GRIS_BORD, panel_info, 2, radius=10)
    draw_text_left(screen, "Information", font_normal, TEXTE_INFO,
                   panel_info.x + 16, panel_info.y + 12)
    pygame.draw.line(screen, GRIS_BORD,
                     (panel_info.x + 10, panel_info.y + 38),
                     (panel_info.right - 10, panel_info.y + 38), 1)

    if state["rom_path"]:
        chemin = state["rom_path"]
        if len(chemin) > 68:
            chemin = chemin[:68] + "..."
        w, h = PRESETS_VALEURS[state["preset_idx"]]
        draw_text_left(screen, "Fichier : " + state["rom_name"], font_small, BLANC,
                       panel_info.x + 16, panel_info.y + 48)
        draw_text_left(screen, "Chemin  : " + chemin, font_small, TEXTE_INFO,
                       panel_info.x + 16, panel_info.y + 70)
        draw_text_left(screen, "Resol.  : " + str(w) + "x" + str(h) +
                       "   |   Palette : " + PALETTES[state["palette_idx"]]["nom"],
                       font_small, TEXTE_INFO, panel_info.x + 16, panel_info.y + 96)
    else:
        draw_text_center(screen, "Aucune ROM chargee - cliquez sur ROM pour en selectionner une.",
                         font_small, TEXTE_INFO, panel_info.centerx, panel_info.y + 70)

    # Bouton Start
    btn_start = pygame.Rect(0, 0, 360, 80)
    btn_start.center = (WIDTH // 2, 375)
    hov    = btn_start.collidepoint(mouse_pos)
    active = state["rom_path"] is not None
    col_bg   = VERT if (active and not hov) else VERT_SURVOL if (active and hov) else GRIS_BORD
    col_bord = VERT_SURVOL if active else GRIS_BORD
    col_txt  = NOIR if active else TEXTE_INFO
    draw_button(screen, btn_start, "START", font_titre, col_bg, col_txt, col_bord, hov, radius=14)

    # Engrenage (bas droite)
    gear_cx, gear_cy = WIDTH - 55, HEIGHT - 55
    gear_rect = pygame.Rect(gear_cx - 30, gear_cy - 30, 60, 60)
    draw_gear(screen, gear_cx, gear_cy, 25, JAUNE if gear_rect.collidepoint(mouse_pos) else GRIS_BORD)

    # Bouton Quitter (bas gauche)
    btn_quit = pygame.Rect(20, HEIGHT - 50, 110, 34)
    hov = btn_quit.collidepoint(mouse_pos)
    draw_button(screen, btn_quit, "Quitter", font_small,
                ROUGE if not hov else ROUGE_SURVOL, BLANC, ROUGE_SURVOL, hov, radius=8)

    return {
        "clavier": btn_clavier,
        "rom":     btn_rom,
        "start":   btn_start,
        "gear":    gear_rect,
        "quit":    btn_quit,
    }


# ====== PAGE CLAVIER ======
CHIP8_KEYS = [
    ("1","1"), ("2","2"), ("3","3"), ("C","4"),
    ("4","Q"), ("5","W"), ("6","E"), ("D","R"),
    ("7","A"), ("8","S"), ("9","D"), ("E","F"),
    ("A","Z"), ("0","X"), ("B","C"), ("F","V"),
]

def draw_clavier(mouse_pos):
    screen.fill(GRIS_FOND)
    draw_text_center(screen, "Clavier Hexadecimal Chip-8", font_titre, VERT, WIDTH // 2, 38)
    pygame.draw.line(screen, GRIS_BORD, (60, 60), (WIDTH - 60, 60), 1)
    draw_text_center(screen, "Touche Chip-8   ->   Touche clavier PC",
                     font_small, TEXTE_INFO, WIDTH // 2, 80)

    cell_w, cell_h = 150, 70
    grid_w = 4 * cell_w + 3 * 10
    grid_x = (WIDTH - grid_w) // 2
    grid_y = 110

    for i, (chip_key, pc_key) in enumerate(CHIP8_KEYS):
        col = i % 4
        row = i // 4
        x = grid_x + col * (cell_w + 10)
        y = grid_y + row * (cell_h + 10)
        rect = pygame.Rect(x, y, cell_w, cell_h)
        draw_rect_fill(screen, GRIS_PANEL, rect, radius=10)
        draw_rect_outline(screen, GRIS_BORD, rect, 2, radius=10)
        draw_text_center(screen, chip_key, font_clavier, VERT,     x + cell_w // 3,          y + cell_h // 2)
        draw_text_center(screen, "->",     font_normal,  GRIS_BORD, x + cell_w // 2,          y + cell_h // 2)
        draw_text_center(screen, pc_key,   font_clavier, JAUNE,    x + cell_w * 2 // 3 + 10, y + cell_h // 2)

    btn_retour = pygame.Rect(20, HEIGHT - 50, 120, 34)
    hov = btn_retour.collidepoint(mouse_pos)
    draw_button(screen, btn_retour, "<- Retour", font_small,
                BLEU if not hov else BLEU_SURVOL, BLANC, BLEU_SURVOL, hov, radius=8)
    return {"retour": btn_retour}


# ====== PAGE PARAMETRES ======
def draw_settings(mouse_pos):
    screen.fill(GRIS_FOND)
    draw_text_center(screen, "Parametres", font_titre, JAUNE, WIDTH // 2, 38)
    pygame.draw.line(screen, GRIS_BORD, (60, 60), (WIDTH - 60, 60), 1)

    btns = {}

    # Resolution
    draw_text_left(screen, "Resolution de la fenetre :", font_normal, TEXTE_INFO, 80, 90)
    for i, label in enumerate(PRESETS_TAILLE):
        r = pygame.Rect(80 + i * 230, 118, 210, 44)
        hov      = r.collidepoint(mouse_pos)
        selected = (i == settings_tmp["preset_idx"])
        bg   = VERT        if selected else GRIS_PANEL
        bord = VERT_SURVOL if selected else (BLEU_SURVOL if hov else GRIS_BORD)
        tcol = NOIR        if selected else (BLANC if hov else TEXTE_INFO)
        draw_button(screen, r, label, font_small, bg, tcol, bord, hov, radius=8)
        btns["preset_" + str(i)] = r

    # Bouton Appliquer (centre bas)
    btn_appliquer = pygame.Rect(0, 0, 180, 42)
    btn_appliquer.center = (WIDTH // 2, HEIGHT - 55)
    hov = btn_appliquer.collidepoint(mouse_pos)
    draw_button(screen, btn_appliquer, "Appliquer", font_normal,
                VERT if not hov else VERT_SURVOL, NOIR, VERT_SURVOL, hov, radius=8)
    btns["appliquer"] = btn_appliquer

    # Bouton Retour (bas gauche)
    btn_retour = pygame.Rect(20, HEIGHT - 50, 120, 34)
    hov = btn_retour.collidepoint(mouse_pos)
    draw_button(screen, btn_retour, "<- Retour", font_small,
                BLEU if not hov else BLEU_SURVOL, BLANC, BLEU_SURVOL, hov, radius=8)
    btns["retour"] = btn_retour

    return btns


# ====== BOUCLE PRINCIPALE ======
running     = True
error_msg   = ""
error_timer = 0
cached_btns = {}

while running:
    WIDTH, HEIGHT = screen.get_size()
    mouse_pos = pygame.mouse.get_pos()
    dt = clock.tick(60)

    if error_timer > 0:
        error_timer -= dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            if state["page"] == "main":
                if cached_btns.get("clavier") and cached_btns["clavier"].collidepoint(pos):
                    state["page"] = "clavier"
                elif cached_btns.get("rom") and cached_btns["rom"].collidepoint(pos):
                    choisir_rom()
                elif cached_btns.get("start") and cached_btns["start"].collidepoint(pos):
                    if state["rom_path"]:
                        if not lancer_rom():
                            error_msg   = "Emulateur introuvable : " + EMULATEUR_PATH
                            error_timer = 3000
                    else:
                        error_msg   = "Veuillez selectionner une ROM d'abord."
                        error_timer = 2000
                elif cached_btns.get("gear") and cached_btns["gear"].collidepoint(pos):
                    settings_tmp["preset_idx"]  = state["preset_idx"]
                    settings_tmp["palette_idx"] = state["palette_idx"]
                    state["page"] = "settings"
                    cached_btns = {}
                elif cached_btns.get("quit") and cached_btns["quit"].collidepoint(pos):
                    running = False

            elif state["page"] == "clavier":
                if cached_btns.get("retour") and cached_btns["retour"].collidepoint(pos):
                    state["page"] = "main"
                    cached_btns = {}

            elif state["page"] == "settings":
                handled = False
                if cached_btns.get("appliquer") and cached_btns["appliquer"].collidepoint(pos):
                    state["preset_idx"]  = settings_tmp["preset_idx"]
                    state["palette_idx"] = settings_tmp["palette_idx"]
                    state["page"] = "main"
                    cached_btns = {}
                    handled = True
                    # Redimensionne la fenetre du launcher
                    new_w, new_h = PRESETS_VALEURS[state["preset_idx"]]
                    screen = pygame.display.set_mode((new_w, new_h))
                elif cached_btns.get("retour") and cached_btns["retour"].collidepoint(pos):
                    state["page"] = "main"
                    cached_btns = {}
                    handled = True
                if not handled:
                    for i in range(len(PRESETS_TAILLE)):
                        key = "preset_" + str(i)
                        if cached_btns.get(key) and cached_btns[key].collidepoint(pos):
                            settings_tmp["preset_idx"] = i
                    for i in range(len(PALETTES)):
                        key = "palette_" + str(i)
                        if cached_btns.get(key) and cached_btns[key].collidepoint(pos):
                            settings_tmp["palette_idx"] = i

    # Rendu
    if state["page"] == "main":
        cached_btns = draw_main(mouse_pos)
    elif state["page"] == "clavier":
        cached_btns = draw_clavier(mouse_pos)
    elif state["page"] == "settings":
        cached_btns = draw_settings(mouse_pos)

    # Message d'erreur flottant
    if error_timer > 0:
        err_surf = pygame.Surface((580, 40), pygame.SRCALPHA)
        pygame.draw.rect(err_surf, (180, 30, 30, 210), (0, 0, 580, 40), border_radius=8)
        screen.blit(err_surf, (WIDTH // 2 - 290, HEIGHT - 100))
        draw_text_center(screen, error_msg, font_small, BLANC, WIDTH // 2, HEIGHT - 80)

    pygame.display.flip()

pygame.quit()
root.destroy()
sys.exit()