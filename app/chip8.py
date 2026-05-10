
import outils.Couleur as Couleur
from random import randint

sprite=[
    0xF0, 0x90, 0x90, 0x90, 0xF0, 0x20, 0x60, 0x20, 0x20, 0x70, # 0 et 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0, 0xF0, 0x10, 0xF0, 0x10, 0xF0, # 2 et 3
    0x90, 0x90, 0xF0, 0x10, 0x10, 0xF0, 0x80, 0xF0, 0x10, 0xF0, # 4 et 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0, 0xF0, 0x10, 0x20, 0x40, 0x40, # 6 et 7
    0xF0, 0x90, 0xF0, 0x90, 0xF0, 0xF0, 0x90, 0xF0, 0x10, 0xF0, # 8 et 9
    0xF0, 0x90, 0xF0, 0x90, 0x90, 0xE0, 0x90, 0xE0, 0x90, 0xE0, # A et B
    0xF0, 0x80, 0x80, 0x80, 0xF0, 0xE0, 0x90, 0x90, 0x90, 0xE0, # C et D
    0xF0, 0x80, 0xF0, 0x80, 0xF0, 0xF0, 0x80, 0xF0, 0x80, 0x80  # E et F
]

class chip_8:
    def __init__(self, clavier=None):
        self.v=[0]*16
        self.memoir=[0]*4096
        self.pc=0x200
        self.I=0
        self.stack=[0]*64
        self.SP=0
        self.ecran=[0]*(64*32)
        self.delay_timer=0
        self.sound_timer=0
        self.etat_touche=[False]*16
        self.clavier=clavier
        

        for i in range(len(sprite)):
            self.memoir[i]=sprite[i]

        
    def cycle (self):
        opcode=(self.memoir[self.pc]<<8) | self.memoir[self.pc+1]
        t=(opcode&0xF000)>>12
        x=(opcode&0x0F00)>>8
        y=(opcode&0x00F0)>>4
        N=(opcode&0x000F)
        NN=(opcode&0x00FF)
        NNN=(opcode&0x0FFF)


        match t: # trouve la commande a exécuter

            case 0x0: # reset le tab
                if NN==0xE0:
                    self.ecran=[0]*(64*32)
                elif NN==0xEE: #sort d'une sous routine
                    self.SP-=1
                    self.pc=self.stack[self.SP]
                    return


            case 0x1:
                self.pc=NNN
                return


            case 0x2: # régle pc a l'adresse NNN et sauvegarde son ancien adresse dans stack incrémente SP
                if self.SP < len(self.stack):
                    self.stack[self.SP]=self.pc+2
                    self.SP+=1
                self.pc=NNN
                return



            case 0x3:# si vx == NN saute instruction
                if self.v[x]==NN:
                    self.pc+=2


            case 0x4:# si vx diff de NN saute instruction
                if self.v[x]!=NN:
                    self.pc+=2


            case 0x5: #si vx == vy saute instruction 
                if self.v[x]==self.v[y]:
                    self.pc+=2


            case 0x6: # donne la valeur NN a V[x]
                self.v[x]=NN


            case 0x7: # rajoute NN a vx et mettre un modulo 256 sur vx
                self.v[x]=(self.v[x]+NN) & 0xFF


            case 0x8:
                match N:

                    case 0x0:# stock vy dans vx
                        self.v[x]=self.v[y]
        
                    case 0x1:# vx stocke le or de vx et vy 
                        self.v[x]=self.v[x]|self.v[y]
                    
                    case 0x2: # result and vx et vy sauv dans vx
                        self.v[x]=self.v[x] & self.v[y]
                    
                    case 0x3: # vx= vx xor vy
                        self.v[x]=self.v[x] ^self.v[y]
                    
                    case 0x4: # ADD Vx, Vy
                        somme = self.v[x] + self.v[y]   
                        # 1. On vérifie s'il y a un dépassement (> 255)
                        if somme > 0xFF:
                            retenue = 1
                        else:
                            retenue = 0
                        # 2. On applique le résultat sur 8 bits
                        self.v[x] = somme & 0xFF
                        # 3. On met à jour VF à la toute fin
                        self.v[0xF] = retenue
                    
                    case 0x5: # vx=vx-vy
                        if self.v[x]<self.v[y]:
                            s=0
                        else:
                            s=1
                        self.v[x]=(self.v[x]-self.v[y])&0xFF
                        self.v[0xF]=s

                    case 0x6: # si dernier bit de vx == 1 alors vf=1 sinon vf=0 dans tout les cas apres div vx//2 décalage a droite
                        self.v[0xF]=self.v[x]&0x01
                        self.v[x]=self.v[x]>>1
                    
                    case 0x7: # vy - vx
                        if self.v[y]>self.v[x]:
                            self.v[0xF]=1
                        else:
                            self.v[0xF]=0
                        self.v[x]=(self.v[y]-self.v[x])&0xFF
                    
                    case 0xE:# décalage a gauche
                        self.v[0xF]=(self.v[x]&0x80)>>7
                        self.v[x]= (self.v[x]<<1) & 0xFF

                    case _:
                        print("texte({hex(opcode)}, rouge)")


            case 0x9: # saute instruction si x!=y
                if self.v[x]!=self.v[y]:
                    self.pc+=2


            case 0xA: # change l'addresse I par NNN
                
                self.I=NNN

            case 0xB: # jump a l'addresse nnn+vo
                self.pc=NNN+self.v[0]
                return


            case 0xC:
                self.v[x]=(randint(0,255)& NN)

            case 0xD: # dessin
                x_pos = self.v[x] % 64
                y_pos = self.v[y] % 32
                self.v[0xF] = 0

                for row in range(N):
                    byte = self.memoir[self.I + row]
                    for col in range(8):
                        if byte & (0x80 >> col):
                            px = (x_pos + col) % 64
                            py = (y_pos + row) % 32
                            idx = py * 64 + px
                            if self.ecran[idx] == 1:
                                self.v[0xF] = 1  # collision
                            self.ecran[idx] ^= 1

            case 0xE:
                match NN:
                    case 0x9E: # skip next if key Vx is pressed
                        if self.etat_touche[self.v[x]]:
                            self.pc+=2

                    case 0xA1: # skip next if key Vx is NOT pressed
                        if not self.etat_touche[self.v[x]]:
                            self.pc+=2

                    case _:
                        print("texte({hex(opcode)}, rouge)")


            case 0xF:
                match NN:
                    case 0x07:
                        self.v[x]=self.delay_timer

                    case 0x0A:
                        if self.clavier:
                            touche = self.clavier.attendre_touche()
                            if touche is None:
                                return
                            self.v[x] = touche
                        else:
                            return
                    
                    case 0x15:
                        self.delay_timer=self.v[x]

                    case 0x18:
                        self.sound_timer=self.v[x]
                    
                    case 0x1E: # I = I+ v[x]
                        self.I+=self.v[x]
                    
                    case 0x29:
                        self.I=(5*(self.v[x])) & 0x0FFF
                    
                    case 0x33:
                        #i= centaine i+1 = dizaine i+2 = unité
                        self.memoir[self.I]=self.v[x]//100
                        self.memoir[self.I+1]=(self.v[x]%100)//10
                        self.memoir[self.I+2]=self.v[x]%10

                    case 0x55:
                        i = 0
                        while i <= x:
                            self.memoir[self.I + i] = self.v[i]
                            i += 1
                    
                    case 0x65:
                        i = 0
                        while i <= x:
                            self.v[i] = self.memoir[self.I + i]
                            i += 1
                    
                    case _:
                        print("texte({hex(opcode)}, rouge)")
            case _:
                print("texte({hex(opcode)}, rouge)")
        self.pc+=2
