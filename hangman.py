import pygame
import math
import random

# Setup display
pygame.init()
WIDTH, HEIGHT = 1000, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# Load background image
background_image = pygame.image.load("bg.jpeg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Button variables
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

# Fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 30)  # Decreased font size for hint
DASH_FONT = pygame.font.SysFont('comicsans', 60)
font_path = "MidnightUnionRegular-3zxKM.ttf"
TITLE_FONT = pygame.font.Font(font_path, 60)
HINT_FONT = pygame.font.SysFont('comicsans', 20)

# Load images
images = [pygame.image.load(f"hangman{i}.png") for i in range(7)]

# Game variables
hangman_status = 0
words_and_hints = {"RUST": "A programming language focused on performance and safety.",
                   "JAVA": "A popular object-oriented programming language.",
                   "PYTHON": "A high-level programming language known for its readability.",
                   "PYGAME": "A set of Python modules designed for writing video games.",
                   "HANGMAN": "The game you're playing now!",
                   "JAYESH": "The developer of this Hangman game.",
                   "GUITAR": "A musical instrument with strings typically played by strumming or plucking.",
                   "CAT": "A small domesticated carnivorous mammal with soft fur, a short snout, and retractile claws.",
                    "BEACH": "A sandy or pebbly shore, especially by the ocean."}
word = random.choice(list(words_and_hints.keys()))
guessed = []

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

# Quit button variables
QUIT_BUTTON_SIZE = 40
QUIT_BUTTON_POS = (10, 10)

def draw_counts_screen(winning_count, losing_count):
    win.fill(WHITE)

    # Display winning and losing counts
    win_count_text = WORD_FONT.render(f"Winning Count: {winning_count}", 1, BLACK)
    win.blit(win_count_text, (WIDTH/2 - win_count_text.get_width()/2, HEIGHT/2 - 50))

    lose_count_text = WORD_FONT.render(f"Losing Count: {losing_count}", 1, BLACK)
    win.blit(lose_count_text, (WIDTH/2 - lose_count_text.get_width()/2, HEIGHT/2 + 50))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return


def draw():
    # Draw background image
    win.blit(background_image, (0, 0))

    # Draw title
    text = TITLE_FONT.render("HANGMAN GAME", 1, WHITE)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    # Draw quit button
    pygame.draw.rect(win, RED, (QUIT_BUTTON_POS[0], QUIT_BUTTON_POS[1], QUIT_BUTTON_SIZE, QUIT_BUTTON_SIZE))
    quit_text = LETTER_FONT.render("X", 1, WHITE)
    win.blit(quit_text, (QUIT_BUTTON_POS[0] + QUIT_BUTTON_SIZE / 2 - quit_text.get_width() / 2,
                         QUIT_BUTTON_POS[1] + QUIT_BUTTON_SIZE / 2 - quit_text.get_height() / 2))

    # Draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = DASH_FONT.render(display_word, 1, WHITE)
    win.blit(text, (400, 200))

    # Draw hint at the bottom
    hint_text = HINT_FONT.render("Hint: " + words_and_hints[word], 1, WHITE)
    win.blit(hint_text, (WIDTH/2 - hint_text.get_width()/2, HEIGHT - 50))

    # Draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, WHITE, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, WHITE)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    win.blit(images[hangman_status], (150, 100))

    pygame.display.update()

    # Handle quit button click event
    mouse_pos = pygame.mouse.get_pos()
    if QUIT_BUTTON_POS[0] < mouse_pos[0] < QUIT_BUTTON_POS[0] + QUIT_BUTTON_SIZE \
            and QUIT_BUTTON_POS[1] < mouse_pos[1] < QUIT_BUTTON_POS[1] + QUIT_BUTTON_SIZE:
        if pygame.mouse.get_pressed()[0]:
            return True
    return False


def display_message(message, colour):
    pygame.time.delay(1000)
    win.fill(colour)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)


def reset_letters():
    global letters
    global startx
    global starty
    letters = []
    startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    starty = 400
    A = 65
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])


def main():
    global hangman_status
    global word
    global guessed

    FPS = 60
    clock = pygame.time.Clock()
    winning_count = 0
    losing_count = 0

    while True:
        hangman_status = 0
        word = random.choice(list(words_and_hints.keys()))
        guessed = []
        reset_letters()

        run = True
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_x, m_y = pygame.mouse.get_pos()
                    if QUIT_BUTTON_POS[0] < m_x < QUIT_BUTTON_POS[0] + QUIT_BUTTON_SIZE \
                            and QUIT_BUTTON_POS[1] < m_y < QUIT_BUTTON_POS[1] + QUIT_BUTTON_SIZE:
                        if draw_counts_screen(winning_count, losing_count):
                            pygame.quit()
                            return
                    for letter in letters:
                        x, y, ltr, visible = letter
                        if visible:
                            dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                            if dis < RADIUS:
                                letter[3] = False
                                guessed.append(ltr)
                                if ltr not in word:
                                    hangman_status += 1

            quit_clicked = draw()

            won = True
            for letter in word:
                if letter not in guessed:
                    won = False
                    break

            if won:
                winning_count += 1
                display_message("You WON!", GREEN)
                break

            if hangman_status == 6:
                losing_count += 1
                display_message("You LOST!", RED)
                break


if __name__ == "__main__":
    main()
