import random

from Game.AcidRain.AcidRainView import AcidRainView
from Game.make_word_array import create_translation_dict
from Game.make_word_array import generate_word_pairs


class AcidRainModel:
    def __init__(self):
        self.view = AcidRainView()
        self.falling_words = []
        self.dict_list = create_translation_dict((generate_word_pairs(100)))
        self.word_list = list(self.dict_list.values())
        self.lives = 3
        self.score = 0

    def generate_word(self):
        word = random.choice(self.word_list)
        if word not in [word_info["text"] for word_info in self.falling_words]:  # 이미 떨어지는 단어에 없으면 추가
            self.falling_words.append(
                {"text": word, "x": random.randint(0, self.view.SCREEN_WIDTH - 50), "y": 0, "speed": random.randint(3, 4)})

    def update_word_positions(self):
        for word_info in self.falling_words:
            word_info["y"] += word_info["speed"]
            if word_info["y"] > self.view.SCREEN_HEIGHT - 100:  # 단어가 화면 아래 이미지 아래로 내려가면
                self.falling_words.remove(word_info)
                self.lives -= 1

    def check_input(self, input_text):
        input_text = input_text.lower()
        for word_info in self.falling_words:
            if self.dict_list.get(input_text) == word_info["text"]:
                self.falling_words.remove(word_info)
                self.score += 1
                return True
        return False
