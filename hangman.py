import pygame
import math
import random

# setup display
pygame.init()
WIDTH, HEIGHT = 1000, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# Load background image
background_image = pygame.image.load("bg.jpeg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


# button variables
RADIUS = 30
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 30)  # Decreased font size for hint
DASH_FONT = pygame.font.SysFont('comicsans', 60)
font_path = "MidnightUnionRegular-3zxKM.ttf" 
TITLE_FONT = pygame.font.Font(font_path, 60)

# load images.
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# game variables
hangman_status = 0
words_and_hints = {"RUST": "A programming language focused on performance and safety.",
                   "JAVA": "A popular object-oriented programming language.",
                   "PYTHON": "A high-level programming language known for its readability.",
                   "PYGAME": "A set of Python modules designed for writing video games.",
                   "HANGMAN": "The game you're playing now!",
                   "JAYESH": "The developer of this Hangman game."}
word = random.choice(list(words_and_hints.keys()))
guessed = []

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)


def draw():
    # Draw background image
    win.blit(background_image, (0, 0))

    # draw title
    text = TITLE_FONT.render("HANGMAN GAME", 1, WHITE)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = DASH_FONT.render(display_word, 1, WHITE)
    win.blit(text, (400, 200))

    # draw hint at the bottom
    hint_text = WORD_FONT.render("Hint: " + words_and_hints[word], 1, WHITE)
    win.blit(hint_text, (WIDTH/2 - hint_text.get_width()/2, HEIGHT - 50))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, WHITE, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, WHITE)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message, colour):
    pygame.time.delay(1000)
    win.fill(colour)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    global hangman_status

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message("You WON!", GREEN)
            break

        if hangman_status == 6:
            display_message("You LOST!", RED)
            break


main()

pygame.quit()
