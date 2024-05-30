import pygame
from hangul_utils import join_jamos

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
        self.hanMode = False

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
        if event.type == pygame.KEYDOWN:  # 키다운 이벤트라면, key, mod, ucicode, scancode 속성을 가진다.
            if event.key == pygame.K_BACKSPACE:
                if self.hanMode and len(self.hanText) > 0:
                    self.hanText = self.hanText[:-1]
                elif len(self.content) > 0:
                    self.content = self.content[:-1]
            elif event.key == pygame.K_ESCAPE:  # 한영 변환 인식 Left Shift + space
                self.hanMode = not self.hanMode
            else:
                if self.hanMode:
                    self.hanText += event.unicode
                else:
                    self.content += event.unicode
            self.content += self.eng2kor(self.hanText)
            self.hanText = ''

    def get_content(self):
        return self.content

    def clear_content(self):
        self.content = ''

    def set_content(self, content):
        self.content = content

    def eng2kor(cls, text):
        result = ''  # 영 > 한 변환 결과

        # 1. 해당 글자가 자음인지 모음인지 확인
        vc = ''
        for t in text:
            if t in cls.cons:
                vc += 'c'
            elif t in cls.vowels:
                vc += 'v'
            else:
                vc += '!'

        # cvv → fVV / cv → fv / cc → dd
        vc = vc.replace('cvv', 'fVV').replace('cv', 'fv').replace('cc', 'dd')

        # 2. 자음 / 모음 / 두글자 자음 에서 검색
        i = 0
        while i < len(text):
            v = vc[i]
            t = text[i]

            j = 1
            # 한글일 경우
            try:
                if v == 'f' or v == 'c':  # 초성(f) & 자음(c) = 자음
                    result += cls.cons[t]

                elif v == 'V':  # 더블 모음
                    result += cls.vowels[text[i:i + 2]]
                    j += 1

                elif v == 'v':  # 모음
                    result += cls.vowels[t]

                elif v == 'd':  # 더블 자음
                    result += cls.cons_double[text[i:i + 2]]
                    j += 1
                else:
                    result += t

            # 한글이 아닐 경우
            except:
                if v in cls.cons:
                    result += cls.cons[t]
                elif v in cls.vowels:
                    result += cls.vowels[t]
                else:
                    result += t

            i += j

        return join_jamos(result)

