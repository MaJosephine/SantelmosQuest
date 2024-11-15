from pygame.locals import *
import pygame, sys
from Bugtong import Bugtong
import random
pygame.init()

# Main game interface
mainClock = pygame.time.Clock()
pygame.display.set_caption("Santelmo's Quest")
win = pygame.display.set_mode((400, 672))
font = pygame.font.Font(None, 50)
mainfont = pygame.font.Font(None, 30)
bg = pygame.image.load('background2.jpg')

# Main menu text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Main menu logs
log_1 = pygame.image.load('log.png')
log_1 = pygame.transform.scale(log_1, (300, 50))
log_2 = pygame.image.load('log.png')
log_2 = pygame.transform.scale(log_2, (300, 50))
log_3 = pygame.image.load('log.png')
log_3 = pygame.transform.scale(log_3, (300, 50))


# riddles (from Bugtong python file)
question_index = Bugtong.riddles.index(random.choice(Bugtong.riddles))
question = Bugtong.riddles[question_index]
answer = Bugtong.answers[question_index]
Font = pygame.font.SysFont('bahnschrift', 15)


#Sprites
s1 = pygame.image.load('s1.png')
s1 = pygame.transform.scale(s1, (50, 50))
s2 = pygame.image.load('s2.png')
s2 =  pygame.transform.scale(s2, (50, 50))
s3 = pygame.image.load('s3.png')
s3 = pygame.transform.scale(s3, (50, 50))
s4 = pygame.image.load('s4.png')
s4 = pygame.transform.scale(s4, (50, 50))
s5 = pygame.image.load('s5.png ')
s5 = pygame.transform.scale(s5, (50, 50))
s6 = pygame.image.load('s6.png')
s6 = pygame.transform.scale(s6, (50, 50))
s7 = pygame.image.load('s7.png')
s7 = pygame.transform.scale(s7, (50, 50))
s8 = pygame.image.load('s8.png')
s8 = pygame.transform.scale(s8, (50, 50))

char = pygame.image.load('s1.png')
char = pygame.transform.scale(char, (50, 50))

jumpUp = [s1, s2, s3, s4, s5, s6, s7, s8]


# Log class
class Logs:
    def __init__(self, log_x, log_y, log_w, log_h, image):
        self.log_x = log_x
        self.log_y = log_y
        self.log_w = log_w
        self.log_h = log_h
        self.image = image
        self.log = pygame.image.load(image)
        self.log = pygame.transform.scale(self.log, (self.log_w, self.log_h))

log0 = Logs(-100, 498, 100, 30, 'log.png')
log1 = Logs(-100, 436, 100, 30, 'log.png')
log2 = Logs(-100, 374, 100, 30, 'log.png')
log3 = Logs(-100, 312, 100, 30, 'log.png')
log4 = Logs(-100, 250, 100, 30, 'log.png')

LOGS = [log0.log, log1.log, log2.log, log3.log, log4.log]
LOGS_X = [log0.log_x, log1.log_x, log2.log_x, log3.log_x, log4.log_x]
LOGS_Y = [log0.log_y, log1.log_y, log2.log_y, log3.log_y, log4.log_y]

logCount = 7
MovingLog = False
log_status = 0


# Input Box
color_inactive = pygame.Color('white')
color_active = pygame.Color('black')
color = color_inactive
inputfont = pygame.font.Font(None, 25)
text = ''

class InputBox:
    def __init__(self, text_x, text_y, w, h, text='' ):
        self.rect = pygame.Rect(text_x, text_y, w, h)
        self.color = color_inactive
        self.text = text
        self.txt_surface = inputfont.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable
                self.active = not self.active
            else:
                self.active = False
            # Change the color of the input box.
            self.color = color_active if self.active else color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    output = self.text
                    self.text = ''
                    self.txt_surface = inputfont.render(self.text, True, self.color)
                    return output
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = inputfont.render(self.text, True, self.color)

    def update(self):
        # Resize the box if text is too long.
        wid = max(200, self.txt_surface.get_width()+10)
        self.rect.w = wid

    def draw(self, win):
        # Blit the text.
        win.blit(self.txt_surface,(self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(win, self.color, self.rect, 2)


# Player class
class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 7

    def draw(self, win):
        if self.isJump:
            win.blit(jumpUp[self.jumpCount // 3], (self.x, self.y))
        else:
            win.blit(char, (self.x, self.y))


# Drawing Game interface
def redrawGameWindow():
    win.blit(bg, (0,0))
    for x in range(5):
        win.blit(LOGS[x], (LOGS_X[x], LOGS_Y[x]))
    # win.blit(LOGS[log_status], (LOGS_X[log_status], LOGS_Y[log_status]))
    # win.blit(log0.log, (log0.log_x, log0.log_y))
    # win.blit(log1.log, (log1.log_x, log1.log_y))
    # win.blit(log2.log, (log2.log_x, log2.log_y))
    # win.blit(log3.log, (log3.log_x, log3.log_y))
    # win.blit(log4.log, (log4.log_x, log4.log_y))
    show_riddle = Font.render(question, True, (0,0,0))
    win.blit(show_riddle, (10, 590))
    win.blit(inputBox.txt_surface,(inputBox.rect.x+5, inputBox.rect.y+5))
    pygame.draw.rect(win, color, inputBox.rect, 2)
    santelmo.draw(win)
    inputBox.update()
    inputBox.draw(win)
    pygame.display.update()


# Instantiation
santelmo = Player(170, 535, 50, 50)
inputBox = InputBox(100, 620, 200, 25)


# Main menu loop
def Santelmos_Quest():
    click = False
    while True:
        win.blit(bg, (0, 0))
        draw_text("Santelmo's Quest", font, (200, 0, 0), win, 50, 240)
        draw_text("Start!", mainfont, (0, 0, 0), win, 175, 282)
        draw_text("Instructions", mainfont, (0, 0, 0), win, 145, 352)
        draw_text("Credits", mainfont, (0, 0, 0), win, 165, 422)
        mx, my = pygame.mouse.get_pos()

        button_1 = win.blit(log_1, (50, 300))
        button_2 = win.blit(log_2, (50, 370))
        button_3 = win.blit(log_3, (50, 440))

        if button_1.collidepoint((mx, my)):
            if click:
                Game()
        if button_2.collidepoint((mx, my)):
            if click:
                How_To_Play()
        if button_3.collidepoint((mx, my)):
            if click:
                Credits()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(24)

# Game loop
def Game():
    clock = pygame.time.Clock()
    run = True
    log_status = 0
    text = ''
    MovingLog = False
    while run:
        clock.tick(24)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            try:
                text = inputBox.handle_event(event).lower()
                if text in answer:
                    show_riddle = question
            except:
                pass

        # keys = pygame.key.get_pressed()
        MovingLog = False
        if text == answer:
            MovingLog = True
            if MovingLog:
                if LOGS_X[log_status] <= 138:
                    LOGS_X[log_status] += 5
                    if LOGS_X[log_status] == 135:
                        santelmo.isJump = True

            if santelmo.isJump:
                if santelmo.jumpCount >= -3:
                    neg = 1
                    if santelmo.jumpCount < 0:
                        neg = -1
                    santelmo.y -= (santelmo.jumpCount ** 2) * 0.5 * neg
                    santelmo.jumpCount -= 1
                    MovingLog = False
                else:
                    santelmo.isJump = False
                    MovingLog = False
                    santelmo.jumpCount = 7
                    log_status += 1
                    text = ''
                    print(log_status)


                    # Please generate new riddle here or create a new function to be called

                # logCount = 7
                # log_status += 1

        redrawGameWindow()

# Instructions loop
def How_To_Play():
    running = True
    while running:
        win.blit(bg, (0, 0))

        draw_text('How To Play', font, (255, 255, 255), win, 100, 250)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    running = False

        pygame.display.update()
        mainClock.tick(24)

# Credits loop
def Credits():
    running = True
    while running:
        win.blit(bg, (0, 0))

        draw_text('Credits', font, (255, 255, 255), win, 135, 250)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    running = False

        pygame.display.update()
        mainClock.tick(24)


Santelmos_Quest()
