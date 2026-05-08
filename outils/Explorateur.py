from gooey import Gooey, GooeyParser
import subprocess
import sys
import os


# Gooey transforme le code en une interface graphique pour être user-friendly
@Gooey(
    program_name="Emulateur Chip8 - Launcher",
    program_description="Sélectionnez un fichier ROM .ch8 pour lancer l'émulation",
    progress_regex=r"^progress: (?P<current>\d+)/(?P<total>\d+)$",
    progress_expr="current / total * 100"
)
def chemin():
    # Parser Gooey pour gérer les arguments utilisateur
    parser = GooeyParser(description="Sélectionnez le fichier Chip8 que vous voulez exécuter")

    # Argument qui force la sélection seulement aux fichiers .ch8 via l'explorateur de fichiers
    parser.add_argument(
        'Filename',
        help="Fichier .ch8",
        widget='FileChooser',
        gooey_options=dict(wildcard="Fichier Chip8 (*.ch8)|*.ch8")
    )

    # Récupère les arguments fournis par l'utilisateur via l'interface
    args = parser.parse_args()

    # Stocke le chemin du fichier sélectionné
    fichier = args.Filename

    # Vérifie que le fichier existe
    if not os.path.isfile(fichier):
        print(f"Erreur : le fichier '{fichier}' n'existe pas.")
        sys.exit(1)

    print(f"Fichier sélectionné : {fichier}")

    # Construire le chemin d'accès au fichier Menu.py situé dans le même dossier
    emulatorPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Menu.py")

    # Vérifie que Menu.py existe
    if not os.path.isfile(emulatorPath):
        print(f"Erreur : Menu.py introuvable à '{emulatorPath}'")
        sys.exit(1)

    print("Lancement de l'émulateur...")

    # Lancer Menu.py avec le fichier ROM en argument
    try:
        subprocess.run([sys.executable, emulatorPath, fichier], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de l'émulateur : {e}")


