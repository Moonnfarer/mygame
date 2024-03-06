

import pygame
import random
pygame.init()




#Window - Skapa ett fönster samt sätta storlek 
screen_storlek = (1000, 600)
screen = pygame.display.set_mode((screen_storlek))

clock = pygame.time.Clock()
 


# Class för text - Här anger vi färg, typsnitt och koordinater, samt en funktion som ritar ut den på skärmen. 
class Text:
    def __init__(self,txt,color,x,y,size):
        self.txt = txt
        self.x = x
        self.y = y
        self.color = color
        self.font = pygame.font.SysFont('Arial',size)
        self.text = self.font.render(self.txt,True,(color))
        self.rect = self.text.get_rect()
        self.rect.center = self.x,self.y

    def draw(self, screen):
        screen.blit(self.text,self.rect)
        self.text = self.font.render(self.txt,True,(self.color))

#Class för vår spelare - består av rect, bild samt angivelse av koordinater och liv 
class Player:
    def __init__(self,x,y, w,h):
        self.image = pygame.image.load('player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (w,h))
        self.rect = pygame.rect.Rect((x, y, w, h))
        self.w = w
        self.h = h

        self.hp = 5

#Class för fiender - består av en rect, bild samt angivelse för liv. 
# Varje fiende har även en separat rektangel som visar hur mycket liv den har kvar. Denna förflyttar sig tillsammans med fienden enligt nästa funktion. 
class Enemy:
    def __init__(self,x,y, w,h):
        self.image = pygame.image.load('fiende.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (w,h))
        self.rect = pygame.rect.Rect((x, y, w, h))

        self.hp = 10
        self.currenthp = self.hp
        self.hpbar = pygame.rect.Rect(x,y-10,50,5)


#Funktion för hur fienden + healthbar rör sig - Rör sig enbart på X-axeln i ett rakt led. 
    def move(self,screen):
        self.rect.x -= 1
        size = (self.currenthp/self.hp)*50
        color = (0,255,0)
        if self.currenthp > (self.hp/3)*2:
            color = (0,255,0)
        elif self.currenthp > self.hp/2:
            color = (255,255,0)
        else:
            color = (255,0,0)
        self.hpbar = pygame.rect.Rect(self.rect.x,self.rect.y-10,size,5)
        pygame.draw.rect(screen, color, self.hpbar)



#Bakgrund - laddas in som bild 
bakgrund = pygame.transform.scale(pygame.image.load("bakgrund.png"), screen_storlek)



#Class för skott - består av en rect, bild samt angivelse av koordinater och hastighet. 
class Bullet:
    def __init__(self,x,y):
        self.image = pygame.image.load('skott.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(8,8))
        self.rect = pygame.rect.Rect(x,y,8,8)
        self.speed = 10

# Funktion för restart - Funktionen anger att listor med fiender och skott ska vara tomma och sedan sätter vi vilkor för pause och skott till falska 
def restart():
    bullet = []
    enemies = []
    spelare = Player(50,200,50,50)
    skjut = False
    timer = 0
    Paused = False
    pause = False

    return bullet, enemies, spelare, skjut, timer, Paused, pause



#Fiende-koordinater
fiende_x = 1050
fiende_w, fiende_h = 50, 50
vel = 2

#Spelet inleds med att alla parametrar återställs  
bullet, enemies, spelare, skjut, timer, Paused, pause = restart()

#Objekt för textruta som anger liv - 
health = Text('',(255,255,255),100,100,75)



#LOOP ________________
run = True
while run: 

#Vår game-loop bygger på vilkoret if not paused inuti en while-loop 
#Först rista bakrunden samt vår liv på skärmen. 
    if not Paused:
        screen.blit(bakgrund, (0, 0))
        health.draw(screen)
        health.txt = f'HP: {spelare.hp}'


# timer som appendar en fieende varje gång timern når 200, som sedan flyttas ut på skärmen och rör sig med hjälp av def move
        timer += 1
        if timer >= 200:
            timer = 0
            enemies.append(Enemy(fiende_x,random.randint(210,550),fiende_w,fiende_h))

# Kolla om fienden har rört sig utanför skärmen, isåfall minska spelarens hp och ta bort fienden från listan enemies      
        for e in enemies:
            e.move(screen)
            screen.blit(e.image,e.rect)
            if e.rect.x < 0-spelare.w:
                spelare.hp -= 1
                enemies.remove(e)

# Loopa genom alla kulor i listan bullet
            for b in bullet:
                if b.rect.colliderect(e.rect):
                    bullet.remove(b)
                    e.currenthp -= 1
                    if e.currenthp <= 0:
                        e.currenthp = 0
                        enemies.remove(e)

# Loop för alla kullor i listan bullet (Ett skott appendas i listan varje gång man trycker på mellanslag)
# ritar ut och förflyttar kulan längs X-axeln  samt tar bort den så fort den är utanför skärmen.      
        for b in bullet:
            b.rect.x += b.speed
            screen.blit(b.image,b.rect)
            if b.rect.x > 1000:
                bullet.remove(b)

        screen.blit(spelare.image,spelare.rect)


# Kollar om spelarens hp(liv) är mindre eller lika med 0, isåfall sätt spelarens hp till 0 och skriv ut att spelaren förlorat
    if spelare.hp <= 0:
        spelare.hp = 0
        bullet, enemies, spelare, skjut, timer, Paused, pause = restart()
        print('Du förlorade!')

# // Sätter en begränsning på hur många gånger koden får uppdateras per sekund med hjälp av en clock-objektet
# / Kolla om eventet är av typen QUIT, isåfall sätt run till False och avsluta spelet
    clock.tick(100)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False 



# Hur vi styr vår spelare
    keys = pygame.key.get_pressed()

# med RETURN kalla vi på funktionen restart() och återställer timer, spelare(kordinater), skott, fiende osv. 
    if keys[pygame.K_RETURN]:
        bullet, enemies, spelare, skjut, timer, Paused, pause = restart()

# Klickar vi på ESCAPE så ändras paus till True, vilket bryter mot vilkoret i vår gameloop. 
    if keys[pygame.K_ESCAPE] and not pause:
        pause = True
        Paused = not Paused

#Klicka vi på ESCAPE igen så ändras variabeln pause till False igen.
    if not keys[pygame.K_ESCAPE]:
        pause = False

#Nedan knappar styr hur vår gubbe rör sig genom att vårt x- och y-värde ökar/minskar      
# Här sätter vi även ett vilkor som begränsar hur långt på X- och Y-axeln vi kan gå. Om vi går utanför X-0 eller X-1000  och Y-0 eller Y-&00 så stannar vi upp. 
    if not Paused:
        if keys[pygame.K_LEFT]:
            if spelare.rect.x >= 0:
                spelare.rect.x -= vel
        if keys[pygame.K_RIGHT]:
            if spelare.rect.x <= 1000-spelare.w:
                spelare.rect.x += vel
        if keys[pygame.K_UP]:
            if spelare.rect.y >= 180:
                spelare.rect.y -= vel
        if keys[pygame.K_DOWN]:
            if spelare.rect.y <= 600-spelare.h:
                spelare.rect.y += vel

#Klickar man på mellanslag appendar vi ett skott till listan bullet, som ritas ut på skärmed med spelarens koordinater. 
        if keys[pygame.K_SPACE] and not skjut:
            bullet.append(Bullet(spelare.rect.x+25,spelare.rect.y+25))
            skjut = True
        if not keys[pygame.K_SPACE]:
            skjut = False

   
    

    

    pygame.display.update()








