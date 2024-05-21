import pygame
from pygame.locals import *
from WordCardModel import WordCardModel
from WordCardView import WordCardView
import pyttsx3
import subprocess

class WordCardController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 650))
        pygame.display.set_caption("Word Cards")

        self.model = WordCardModel()
        self.view = WordCardView(self.screen)
        self.current_card_index = 0
        self.wordcards = self.model.fetch_wordcards()
        self.engine = pyttsx3.init()
        self.running = True
        self.showing_meaning = False  # 뜻을 보여주는지 여부를 추적하는 변수
        self.selected_levels = []  # 선택된 단계를 추적하는 리스트

    def display_word(self):
        if self.wordcards:
            current_wordcard = self.wordcards[self.current_card_index]
            self.view.display_word(current_wordcard.word)
        else:
            self.view.display_no_wordcards()

    def show_meaning(self):
        if self.wordcards:
            current_wordcard = self.wordcards[self.current_card_index]
            self.view.display_word_and_meaning(current_wordcard.word, current_wordcard.mean)
            self.showing_meaning = True

    def show_previous_card(self):
        self.current_card_index = (self.current_card_index - 1) % len(self.wordcards)
        self.showing_meaning = False
        self.display_word()

    def show_next_card(self):
        self.current_card_index = (self.current_card_index + 1) % len(self.wordcards)
        self.showing_meaning = False
        self.display_word()

    def play_word_pronunciation(self):
        if self.wordcards:
            current_wordcard = self.wordcards[self.current_card_index]
            self.engine.say(current_wordcard.word)
            self.engine.runAndWait()

    def toggle_image(self):
        self.view.toggle_image()
        self.display_word()

    def filter_wordcards(self):
        self.wordcards = self.model.fetch_wordcards(self.selected_levels)
        self.current_card_index = 0
        self.display_word()

    def go_to_home(self):
        pygame.quit()
        subprocess.run(["python", "home.py"])

    def run(self):
        self.display_word()
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.show_previous_card()
                    elif event.key == K_RIGHT:
                        self.show_next_card()
                    elif event.key == K_SPACE:
                        self.show_meaning()
                elif event.type == MOUSEBUTTONDOWN:
                    if 520 <= event.pos[0] <= 570 and 520 <= event.pos[1] <= 570:
                        self.show_previous_card()
                    elif 620 <= event.pos[0] <= 670 and 520 <= event.pos[1] <= 570:
                        self.show_next_card()
                    elif 700 <= event.pos[0] <= 750 and 100 <= event.pos[1] <= 150:
                        self.play_word_pronunciation()
                    elif 600 <= event.pos[0] <= 650 and 100 <= event.pos[1] <= 150:
                        self.toggle_image()
                    elif 50 <= event.pos[0] <= 100 and 50 <= event.pos[1] <= 100:
                        self.go_to_home()
                    elif 100 <= event.pos[0] <= 700 and 100 <= event.pos[1] <= 500:
                        if not self.showing_meaning:
                            self.show_meaning()
        pygame.quit()

if __name__ == "__main__":
    controller = WordCardController()
    controller.run()