# Constantes pour les couleurs ANSI dans le terminal
NOIR = "\033[0;30m"
ROUGE = "\033[0;31m"
VERT = "\033[0;32m"
MARRON = "\033[0;33m"
BLEU = "\033[0;34m"
VIOLET = "\033[0;35m"
CYAN = "\033[0;36m"
JAUNE = "\033[1;33m"

NO_COLOR="\033[0m"




def texte(msg, color="info"): 
    """ Retourne un message coloré pour le terminal. """
    match(color):
        
        case 'noir': return f'{NOIR}{msg}{NO_COLOR}'
        case 'rouge': return f'{ROUGE}{msg}{NO_COLOR}'
        case 'vert': return f'{VERT}{msg}{NO_COLOR}'        
        case 'marron': return f'{MARRON}{msg}{NO_COLOR}'        
        case 'bleu': return f'{BLUE}{msg}{NO_COLOR}'        
        case 'violet': return f'{VIOLET}{msg}{NO_COLOR}'
        case 'cyan': return f'{CYAN}{msg}{NO_COLOR}'
        case 'jaune': return f'{JAUNE}{msg}{NO_COLOR}'

        case _: return f'{msg}' # Pas de couleur par défaut.