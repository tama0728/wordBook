import pygame


class Input:
    cons = {'r': 'ㄱ', 'R': 'ㄲ', 's': 'ㄴ', 'e': 'ㄷ', 'E': 'ㄸ', 'f': 'ㄹ', 'a': 'ㅁ', 'q': 'ㅂ', 'Q': 'ㅃ', 't': 'ㅅ',
            'T': 'ㅆ',
            'd': 'ㅇ', 'w': 'ㅈ', 'W': 'ㅉ', 'c': 'ㅊ', 'z': 'ㅋ', 'x': 'ㅌ', 'v': 'ㅍ', 'g': 'ㅎ'}
    # 모음-중성
    vowels = {'k': 'ㅏ', 'o': 'ㅐ', 'i': 'ㅑ', 'O': 'ㅒ', 'j': 'ㅓ', 'p': 'ㅔ', 'u': 'ㅕ', 'P': 'ㅖ', 'h': 'ㅗ', 'hk': 'ㅘ',
              'ho': 'ㅙ', 'hl': 'ㅚ',
              'y': 'ㅛ', 'n': 'ㅜ', 'nj': 'ㅝ', 'np': 'ㅞ', 'nl': 'ㅟ', 'b': 'ㅠ', 'm': 'ㅡ', 'ml': 'ㅢ', 'l': 'ㅣ'}
    # 자음-종성
    cons_double = {'rt': 'ㄳ', 'sw': 'ㄵ', 'sg': 'ㄶ', 'fr': 'ㄺ', 'fa': 'ㄻ', 'fq': 'ㄼ', 'ft': 'ㄽ', 'fx': 'ㄾ', 'fv': 'ㄿ',
                   'fg': 'ㅀ', 'qt': 'ㅄ'}

    def __init__(self, name, view, rect=pygame.Rect(200, 200, 280, 32), limit=17, kor=False):
        self.active = False
        self.name = name
        self.content = ''
        self.view = view
        self.rect = rect
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.limit = limit
        self.kor = kor
        self.hanText = ''

    def draw(self, screen):
        color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(screen, color, self.rect, 2)
        self.view.draw_text(self.name, self.rect, 'left_out')
        self.view.draw_text(self.content, self.rect, 'left_in')

    def set_active(self):
        self.active = True

    def set_inactive(self):
        self.active = False

    def handle_input(self, event):
        if self.kor:
            self.handle_kor(event)
        else:
            if event.key == pygame.K_BACKSPACE:
                self.content = self.content[:-1]
            elif len(self.content) >= self.limit:
                pass
            elif 'z' >= event.unicode >= 'a' or 'Z' >= event.unicode >= 'A' or '9' >= event.unicode >= '0':
                self.content += event.unicode

    def handle_kor(self, event):
        if event.key == pygame.K_BACKSPACE:
            if len(self.hanText) > 0:
                self.hanText = self.hanText[:-1]
        else:
            self.hanText += event.unicode
        self.content + HangulInputBox.engkor(self.hanText)

    def get_content(self):
        return self.content

    def clear_content(self):
        self.content = ''

    def set_content(self, content):
        self.content = content
