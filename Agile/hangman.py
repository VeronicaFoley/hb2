#---------------------------------------#
# Computer-based Hangman is a simple word-guessing-game where player attempts to discover a secret word by guessing one letter at a time.
# Each time the player guesses a letter which doesn't appear in the word, the hangman picture is drawn further. 
# Player must discover the word before the man is hanged.
# Read more about game rule: https://en.wikipedia.org/wiki/Hangman_(game)
#---------------------------------------#

#-----------------------------------------------------------------
# Import libraries/modules for the program
# Use "pygame" library to create GUI, game loop, draw shapes/images on screen
# This is third party module/library that you can download from Intenet
import pygame
# Use "random" library to select randomly the guess word to display
import random

#-----------------------------------------------------------------
# Initialize pygame
pygame.init()
# Create a GUI window
winHeight = 480
winWidth = 700
win = pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption("Hangman - by Daniel")

#-----------------------------------------------------------------
# Create some global variables/constants for the game:
# Declare colors "constants" for the game: background color, text color, key (button) background color
BLACK = (0,0, 0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHT_BLUE = (102,255,255)

# Declare "fonts" used to display guess word, display letters (in fact they are buttons), and display outcome when game is over.
btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)

# Declare "variable" to store the guess word
word = ''

# Declare an array to store all buttons (letters) on keypad - 26 characters
buttons = []

# Declare an array of guessed letters
guessed = []

# Declare an array storing all 7 hangman images
hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'),
               pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'),
               pygame.image.load('hangman6.png')]

# Declare a variable to track the number of wrong guesses
limbs = 0

#-----------------------------------------------------------------
# Function 1: redraw the game window 
def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    win.fill(GREEN)
    # Redraw all buttons (on keypad)
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2)
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    
    win.blit(label1,(winWidth/2 - length/2, 400))

    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))
    pygame.display.update()

#-----------------------------------------------------------------
# Function 2:
def randomWord():
    file = open('words.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)

    return f[i][:-1]

#-----------------------------------------------------------------
# Function 3:
def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False

#-----------------------------------------------------------------
# Function 4: 
def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord
            

#-----------------------------------------------------------------
# Function 5:
def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None


#-----------------------------------------------------------------
# Function 6:
def end(winner=False):
    global limbs
    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'
    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(GREEN)

    if winner == True:
        label = lost_font.render(winTxt, 1, BLACK)
    else:
        label = lost_font.render(lostTxt, 1, BLACK)

    wordTxt = lost_font.render(word.upper(), 1, BLACK)
    wordWas = lost_font.render('The phrase was: ', 1, BLACK)

    win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, 295))
    win.blit(wordWas, (winWidth/2 - wordWas.get_width()/2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()

#-----------------------------------------------------------------
# Function 7:    
def reset():
    global limbs
    global guessed
    global buttons
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    word = randomWord()

#-----------------------------------------------------------------
#MAINLINE
#-----------------------------------------------------------------
    
# Setup buttons
increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([LIGHT_BLUE, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

word = randomWord()
inPlay = True

while inPlay:
    redraw_game_window()
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1])
            if letter != None:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        end()
                else:
                    print(spacedOut(word, guessed))
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)

pygame.quit()
# always quit pygame when done!
