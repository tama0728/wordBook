import pygame
import mysql.connector
import sys
import random
from config import config

conn = mysql.connector.connect(**config)
cursor = conn.cursor()


def fetch_word():
    cursor.execute("SELECT word, mean FROM words WHERE lv=1")
    return cursor.fetchall()


def display_question(screen, font, meaning):
    screen.fill((255, 255, 255))

    meaning_text = font.render(meaning, True, (0, 0, 0))
    meaning_rect = meaning_text.get_rect(center=(400, 200))
    screen.blit(meaning_text, meaning_rect)

    pygame.display.flip()


def ask_questions(screen, font):
    word_list = fetch_word()
    correct_answers = 0
    total_questions = 10

    print("Welcome to the vocabulary test!")
    print("Type in the English word for the given meaning.")

    for i in range(total_questions):
        word_info = random.choice(word_list)
        word = word_info[0]
        meaning = word_info[1]

        display_question(screen, font, meaning)

        user_input = ''
        while not user_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN:
                        user_input = ''
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.key == pygame.K_SPACE:
                        user_input += ' '
                    elif event.unicode.isalpha():
                        user_input += event.unicode

        if user_input.lower() == word.lower():
            correct_answers += 1

    print(f"\nTest completed! You got {correct_answers} out of {total_questions} correct.")


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Vocabulary Test")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    ask_questions(screen, font)