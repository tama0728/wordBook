import random
import time
import Game.make_word_array


# 카드 클래스 정의
class Card:
    def __init__(self, value):
        self.value = value       # 카드 값 (짝을 맞출 때 사용)
        self.state = 'hidden'    # 카드 상태: hidden, shown, matched


# 게임 모델 (데이터 및 게임 로직 연결)
class CardFlipModel:
    def __init__(self):
        self.cards = []           # 카드 목록
        self.first_card = None    # 첫 번째로 선택한 카드 인덱스
        self.second_card = None   # 두 번째로 선택한 카드 인덱스
        self.match_count = 0      # 맞춘 카드 쌍의 수
        self.word_pairs = Game.make_word_array.generate_word_pairs(12)  # 단어 쌍 생성
        self.create_cards()       # 카드 생성 및 섞기
        self.disable_card_selection = False  # 카드 선택 비활성화 상태
        self.paused = False  # 일시정지 상태
        self.pause_duration = 0
        self.start_time = 0  # 시작 시간

    # ESC가 눌리면 카드 선택 불가
    def toggle_card_selection(self):
        # 카드 선택 상태 토글
        self.disable_card_selection = not self.disable_card_selection
        if self.disable_card_selection:
            # 일시정지 상태인 경우, 일시정지된 시간 누적
            self.pause_time = time.time()
        else:
            # 일시정지 상태가 해제된 경우, 일시정지된 시간을 pause_duration에 누적
            if self.pause_time is not None:
                self.pause_duration += time.time() - self.pause_time
            self.pause_time = None
        # 일시정지 상태 토글
        self.paused = not self.paused

    # 게임 시간을 측정하는 함수
    def start_timer(self):
        self.start_time = time.time()

    # 게임이 종료 됐을 때 종료 시간을 리턴하는 함수
    def get_elapsed_time(self):
        if self.paused:
            return self.pause_duration
        else:
            return time.time() - self.start_time - self.pause_duration

    # 데이터베이스에서 카드를 불러와 12개의 튜플로 만드는 함수
    def create_cards(self):
        # 각 단어와 그 뜻을 카드 값으로 갖는 카드 리스트 생성
        cards = []
        for english, korean in self.word_pairs:
            cards.append(Card(english))  # 영어 단어 카드 추가
            cards.append(Card(korean))  # 뜻 카드 추가

        random.shuffle(cards)
        self.cards = cards

    # 카드 선택
    def flip_card(self, index):
        # 숨겨진 카드를 클릭하면 보여지는 상태로 변경
        if self.cards[index].state == 'hidden':
            self.cards[index].state = 'shown'
            if self.first_card is None:
                self.first_card = index  # 첫 번째 카드 선택
            elif self.second_card is None:
                self.second_card = index # 두 번째 카드 선택
                return True
        return False

    # 선택한 쌍이 맞는지 확인하는 함수
    def check_match(self):
        # 두 카드를 비교하여 값이 같으면 'matched' 상태로 변경
        first_card_value = self.cards[self.first_card].value
        second_card_value = self.cards[self.second_card].value

        # 첫 번째 카드의 값이 영어 단어인 경우
        if (first_card_value, second_card_value) in self.word_pairs:
            # 영어 단어와 뜻이 일치하면
            self.cards[self.first_card].state = 'matched'
            self.cards[self.second_card].state = 'matched'
            self.match_count += 1
        # 첫 번째 카드의 값이 뜻인 경우
        elif (second_card_value, first_card_value) in self.word_pairs:
            # 뜻과 영어 단어가 일치하면
            self.cards[self.first_card].state = 'matched'
            self.cards[self.second_card].state = 'matched'
            self.match_count += 1
        else:
            # 값이 다르면 다시 'hidden' 상태로 변경
            self.cards[self.first_card].state = 'hidden'
            self.cards[self.second_card].state = 'hidden'

        # 선택된 카드 초기화
        self.first_card = None
        self.second_card = None

    # 게임이 끝났는지 판별하는 함수
    def is_won(self):
        # 모든 카드 쌍을 맞추었는지 확인
        return self.match_count == len(self.word_pairs)