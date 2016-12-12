# -*- encoding: utf-8 -*-

import random
import time
import pygame

# create a screen of size say 800 * 800.
screen_width, screen_height = 1500, 1500
pygame.init()
pygame.display.set_caption('Kuubikud')
screen = pygame.display.set_mode((1500, 1500))
BASICFONT = pygame.font.Font(None, 30)
# On the screen rectangles of a fixed size of 30*30...
BLACK, WHITE, SININE = (0, 0, 0), (255, 255, 255), (0, 128, 255)
TEXTCOLOR = WHITE

kuubikud = pygame.sprite.Group()


class Kuubik(pygame.sprite.Sprite):
    def __init__(self, width=30, height=30, x=0, y=0, color=WHITE):
        super(Kuubik, self).__init__()  # Py 2.7
        # sprite.Group.draw() jaoks
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x_piksel = x
        self.y_piksel = y

    # piksel vajalik, et konstantselt x-teljel edasi (tegelikult tagasi) liikuda
    @property
    def x_piksel(self):
        return self._x_piksel

    @x_piksel.setter
    def x_piksel(self, uus_x):
        self._x_piksel = uus_x
        self.rect.x = int(round(uus_x))

    @property
    def y_piksel(self):
        return self._y_piksel

    @y_piksel.setter
    def y_piksel(self, uus_y):
        self._y_piksel = uus_y
        self.rect.y = int(round(uus_y))


def main():
    kuvaTekstEkraanil("Avoid the cubes")
    while True:
        mangi()
        kuvaTekstEkraanil("Game over")
        kuubikud.empty()
        screen.fill(BLACK)
        pygame.display.update()


def mangi():
    eelmineAeg = int(round(time.time()))
    hetkeSkoor = 0
    chance_to_appear = 0.1
    airspeed_velocity = 5
    clock = pygame.time.Clock()
    done = False
    while not done:
        isPressed()
        clock.tick(60)

        # kuubikud tekivad paremalt
        if random.random() < chance_to_appear:
            kuubik = Kuubik(x=screen_width, y=random.randrange(screen_height))
            kuubikud.add(kuubik)
        # konstantse kiirusega
        for kuubik in kuubikud:
            kuubik.x_piksel -= float(airspeed_velocity)

        # vasaku seinaga kokkupuutel kuubikud kaovad
        for kuubik in kuubikud:
            if kuubik.x_piksel <= 0:
                kuubikud.remove(kuubik)
        # aknast väljumiseks
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION: x, y = pygame.mouse.get_pos()
            for kuubik in kuubikud:
                if kuubik.rect.collidepoint(x, y): done = True
        screen.fill(BLACK)
        pygame.draw.rect(screen, SININE,
                         pygame.Rect(pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1] - 10, 20, 20))
        kuubikud.draw(screen)  # Group.draw kasutab each .image and .rect to draw
        # Skoor
        if (int(round(time.time())) - eelmineAeg > 10):
            eelmineAeg = int(round(time.time()))
            hetkeSkoor += 10
        joonistaSkoor(hetkeSkoor)

        # Pygame'i init
        pygame.display.flip()
        pygame.display.update()



def joonistaSkoor(skoor):
    # Joonistab skoori
    skoorSurf = BASICFONT.render('Skoor: %s' % skoor, True, TEXTCOLOR)
    screen.blit(skoorSurf, (10, 10))

def kuvaTekstEkraanil(text):
    # Tekst ekraanile
    kirjaSurface, kirjaRect = looTekstiObjekt(text, BASICFONT, TEXTCOLOR)
    kirjaRect.center = (int(screen_width / 2) - 3, int(screen_height / 2) - 3)
    screen.blit(kirjaSurface, kirjaRect)

    # Press any key
    nupuVajutusSurf, nupuVajutusRect = looTekstiObjekt('Press any key to begin', BASICFONT, TEXTCOLOR)
    nupuVajutusRect.center = (int(screen_width / 2), int(screen_height / 2) + 100) #Paigutus
    screen.blit(nupuVajutusSurf, nupuVajutusRect)

    while kontrolliNupuvajutust() == None:
        pygame.display.update()

def isPressed():
    for event in pygame.event.get(pygame.QUIT): # saad kõik QUIT sündmused
        pygame.quit()
    for event in pygame.event.get(pygame.KEYUP):
        if event.key == pygame.K_ESCAPE:
            pygame.quit()

def kontrolliNupuvajutust():
    # Otsib keyup sündmusi
    kontrolliSeiskumist()
    for event in pygame.event.get(pygame.KEYUP):
        if event.type == pygame.KEYDOWN:
            continue
        return event.key
    return None

def kontrolliSeiskumist():
    for event in pygame.event.get(pygame.QUIT): # kõik quit sündmused
        pygame.quit() # lõpetab töö kui eksisteerivad
    for event in pygame.event.get(pygame.KEYUP): # keyup sündmused
        if event.key == pygame.K_ESCAPE:
            pygame.quit() # Esc nupp
        pygame.event.post(event) # paned sündmused tagasi, et ei tekiks lõputut tsüklit

def looTekstiObjekt(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

if __name__ == '__main__':
    main()
