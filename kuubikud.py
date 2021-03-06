# -*- encoding: utf-8 -*-
import random
import time
import pygame
# määra 800 * 800 ekraani suuruseks.
screen_width, screen_height = 1500, 1500
pygame.init()
pygame.display.set_caption('Kuubikud')
screen = pygame.display.set_mode((1500, 1500))
BASICFONT = pygame.font.Font(None, 30)
# 30x30 kuubikud
MUST, VALGE, SININE, PUNANE = (0, 0, 0), (255, 255, 255), (0, 128, 255), (255,0,0)
TEXTCOLOR = VALGE
kuubikud = pygame.sprite.Group()
class Kuubik(pygame.sprite.Sprite):
    def __init__(self, width=30, height=30, x=0, y=0, color=VALGE):
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
    global highScore
    highScore = 0
    kuvaTekstEkraanil("Avoid the cubes")
    while True:
        mangi()
        kuvaTekstEkraanil("|Game over|Score:" + str(hetkeSkoor) + "|Level:" + str(level) + "|")
        if (hetkeSkoor > highScore):
            highScore = hetkeSkoor
        kuubikud.empty()
        screen.fill(MUST)
        pygame.display.update()
def mangi():
    global hetkeSkoor, level
    eelmineAeg = int(round(time.time()))
    hetkeSkoor = 0
    level = 0
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
        # aknast väljumiseks ja pausiks
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_p:
                    kuvaTekstEkraanil("Pause")
            if event.type == pygame.MOUSEMOTION: x, y = pygame.mouse.get_pos()
            for kuubik in kuubikud:
                if kuubik.rect.collidepoint(x, y): done = True
        screen.fill(MUST)
        pygame.draw.rect(screen, SININE,
                         pygame.Rect(pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1] - 10, 20, 20))
        kuubikud.draw(screen)  # Group.draw kasutab each .image and .rect to draw
        # Skoor
        if (int(round(time.time())) - eelmineAeg > 10):
            eelmineAeg = int(round(time.time()))
            hetkeSkoor += 10
            if(hetkeSkoor % 20 == 0):
                airspeed_velocity += 1
                chance_to_appear += 0.1
                level += 1
        joonistaSkoorjaLevel(hetkeSkoor, level)
        # Pygame'i init
        pygame.display.flip()
        pygame.display.update()
def joonistaSkoorjaLevel(skoor, level):
    # Joonistab skoori
    skoorSurf = BASICFONT.render('Score: %s' % skoor, True, TEXTCOLOR)
    screen.blit(skoorSurf, (10, 10))
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    screen.blit(levelSurf, (10, 30))
    skoorSurf = BASICFONT.render('Highscore: %s' % highScore, True, TEXTCOLOR)
    screen.blit(skoorSurf, (10, 50))
def kuvaTekstEkraanil(text):
    # Tekst ekraanile
    kirjaSurface, kirjaRect = looTekstiObjekt(text, BASICFONT, PUNANE)
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
