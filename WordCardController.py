import pygame
from pygame.locals import *
from WordCardModel import WordCardModel
from WordCardView import WordCardView
import pyttsx3
from Popup import Popup
from UserController import UserController

class WordCardController:
    def __init__(self, username):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 650))
        pygame.display.set_caption("Word Cards")

        self.username = username
        self.model = WordCardModel()
        self.view = WordCardView(self.screen)
        self.current_card_index = 0
        self.wordcards = self.model.fetch_wordcards(filter_levels=['1', '2', '3'], username=username)
        self.engine = pyttsx3.init()
        self.running = True
        self.showing_meaning = False
        self.selected_levels = ['1', '2', '3']
        self.show_favorites_only = False
        self.popup = Popup()

        self.display_word()  # 초기 단어카드 표시

    def display_word(self):
        if self.wordcards:
            current_wordcard = self.wordcards[self.current_card_index]
            self.view.display_word(current_wordcard.word, self.current_card_index, len(self.wordcards), current_wordcard.is_favorite)
        else:
            self.view.display_no_wordcards()

    def show_meaning(self):
        self.showing_meaning = not self.showing_meaning
        if self.showing_meaning:
            if self.wordcards:
                current_wordcard = self.wordcards[self.current_card_index]
                self.view.display_meaning(current_wordcard.word, current_wordcard.mean, self.current_card_index, len(self.wordcards), current_wordcard.is_favorite)
        else:
            self.display_word()

    def show_previous_card(self):
        if self.current_card_index == 0:
            self.popup.show("첫 페이지입니다.")
        else:
            self.current_card_index = (self.current_card_index - 1) % len(self.wordcards)
            self.showing_meaning = False
            self.display_word()

    def show_next_card(self):
        if self.current_card_index == len(self.wordcards) - 1:
            self.popup.show("마지막 페이지입니다.")
        else:
            self.current_card_index = (self.current_card_index + 1) % len(self.wordcards)
            self.showing_meaning = False
            self.display_word()

    def show_previous_ten_cards(self):
        if self.current_card_index == 0:
            self.popup.show("첫 페이지입니다.")
        else:
            self.current_card_index = max(0, self.current_card_index - 10)
            self.showing_meaning = False
            self.display_word()

    def show_next_ten_cards(self):
        if self.current_card_index >= len(self.wordcards) - 10:
            self.popup.show("마지막 페이지입니다.")
        else:
            self.current_card_index = min(len(self.wordcards) - 1, self.current_card_index + 10)
            self.showing_meaning = False
            self.display_word()

    def play_word_pronunciation(self):
        if self.wordcards:
            current_wordcard = self.wordcards[self.current_card_index]
            self.engine.say(current_wordcard.word)
            self.engine.runAndWait()

    def toggle_favorite(self):
        current_wordcard = self.wordcards[self.current_card_index]
        if current_wordcard.is_favorite:
            self.model.remove_from_favorite(self.username, current_wordcard.word)
            current_wordcard.is_favorite = False
        else:
            self.model.add_to_favorite(self.username, current_wordcard.word)
            current_wordcard.is_favorite = True
        self.view.toggle_image(current_wordcard.is_favorite)
        self.display_word()

    def filter_wordcards(self):
        self.wordcards = self.model.fetch_wordcards(self.selected_levels, username=self.username, only_favorites=self.show_favorites_only)
        self.current_card_index = 0
        self.display_word()

    def toggle_level(self, level):
        if level == 'favorites':
            self.show_favorites_only = not self.show_favorites_only
        else:
            if level in self.selected_levels:
                self.selected_levels.remove(level)
            else:
                self.selected_levels.append(level)
        self.view.selected_levels = self.selected_levels
        self.view.show_favorites_only = self.show_favorites_only
        self.filter_wordcards()
        self.display_word()

    def go_to_home(self):
        from UserController import UserController  # 지연 가져오기
        pygame.quit()
        UserController(self.username).run()  # UserController로 이동

    def run(self):
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
                    elif event.key == K_UP:
                        self.show_previous_ten_cards()
                    elif event.key == K_DOWN:
                        self.show_next_ten_cards()
                elif event.type == MOUSEBUTTONDOWN:
                    if 520 <= event.pos[0] <= 570 and 520 <= event.pos[1] <= 570:
                        self.show_previous_card()
                    elif 620 <= event.pos[0] <= 670 and 520 <= event.pos[1] <= 570:
                        self.show_next_card()
                    elif 620 <= event.pos[0] <= 670 and 130 <= event.pos[1] <= 180:
                        self.toggle_favorite()
                    elif 680 <= event.pos[0] <= 720 and 130 <= event.pos[1] <= 170:
                        self.play_word_pronunciation()
                    elif 680 <= event.pos[0] <= 730 and 580 <= event.pos[1] <= 630:
                        self.go_to_home()
                    else:
                        if 100 <= event.pos[0] <= 700 and 100 <= event.pos[1] <= 500:
                            self.show_meaning()
                    for level, rect in self.view.filter_buttons.items():
                        if rect.collidepoint(event.pos):
                            self.toggle_level(level)
            self.popup.draw(self.screen)
        pygame.quit()

if __name__ == "__main__":
    controller = WordCardController(username="test_user")
    controller.run()