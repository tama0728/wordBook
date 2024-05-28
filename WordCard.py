import tkinter as tk
from tkinter import ttk
from tkinter import Canvas, IntVar
import pyttsx3
from PIL import Image, ImageTk  # Pillow 라이브러리 임포트

import mysql.connector
import subprocess

from config import config

class Flashcard:
    def __init__(self, word, mean):
        self.word = word
        self.mean = mean

# MySQL 연결
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# 단어 데이터 불러오기
def fetch_flashcards(filter_levels=None):
    filter_query = ""
    if filter_levels:
        filter_query = " WHERE lv IN ({})".format(",".join(filter_levels))
    cursor.execute("SELECT word, mean FROM words" + filter_query)
    return cursor.fetchall()

# GUI 생성
root = tk.Tk()
root.title("Flashcards")
root.configure(bg="white")

canvas = tk.Canvas(root, bg="white", width=800, height=650)
canvas.pack()

current_card_index = 0  # 현재 단어 인덱스 초기화

# 필터링된 단계
selected_levels = []

# 단계 필터링 함수
def filter_flashcards():
    selected_levels.clear()
    for level, var in level_vars.items():
        if var.get() == 1:
            selected_levels.append(level)
    display_word()

# 단어 표시 함수
def display_word():
    canvas.delete("all")
    flashcards = fetch_flashcards(selected_levels)
    if flashcards:
        current_flashcard = flashcards[current_card_index]
        canvas.create_rectangle(100, 100, 700, 500, fill="aliceblue", outline="light cyan", width=2)
        canvas.create_text(400, 260, text=current_flashcard[0], font=("Arial", 48, "bold"), fill="black")
    else:
        canvas.create_text(400, 260, text="No flashcards found", font=("Arial", 24), fill="black")

# 단어 클릭 시 뜻 표시
def show_mean(event):
    canvas.delete("mean_text")
    flashcards = fetch_flashcards(selected_levels)
    if flashcards:
        current_flashcard = flashcards[current_card_index]
        canvas.create_text(400, 380, text=current_flashcard[1], font=("Arial", 28), fill="black", tags="mean_text")

# 초기화면 표시
display_word()

# 이벤트 바인딩: 단어 클릭 시 뜻 표시
canvas.bind("<Button-1>", show_mean)

# 단계 선택 Checkbutton 생성
level_vars = {}
levels = ["1", "2", "3"]
for i, level in enumerate(levels):
    level_vars[level] = IntVar()
    level_checkbox = ttk.Checkbutton(root, text=level, variable=level_vars[level], command=filter_flashcards)
    level_checkbox.place(x=20, y=100 + i * 30)

# 이전 단어 버튼
def show_previous_card():
    global current_card_index
    flashcards = fetch_flashcards(selected_levels)
    if flashcards:
        current_card_index = (current_card_index - 1) % len(flashcards)
        display_word()

previous_image = tk.PhotoImage(file="left_arrow.png")
previous_button = tk.Button(root, image=previous_image, command=show_previous_card, bd=0, highlightthickness=0)
previous_button.place(x=520, y=520)

# 다음 단어 버튼
def show_next_card():
    global current_card_index
    flashcards = fetch_flashcards(selected_levels)
    if flashcards:
        current_card_index = (current_card_index + 1) % len(flashcards)
        display_word()

next_image = tk.PhotoImage(file="right_arrow.png")
next_button = tk.Button(root, image=next_image, command=show_next_card, bd=0, highlightthickness=0)
next_button.place(x=620, y=520)

# 홈 화면으로 이동하는 함수
def go_to_home():
    root.destroy()  # 현재 창을 닫음
    subprocess.run(["python", "home.py"])  # home.py 실행

# 홈 화면 버튼
home_image = tk.PhotoImage(file="home.png")
home_button = ttk.Button(root, image=home_image, command=go_to_home)
home_button.place(x=670, y=600)

engine = pyttsx3.init()
def play_word_pronunciation():
    flashcards = fetch_flashcards(selected_levels)
    if flashcards:
        current_flashcard = flashcards[current_card_index]
        word = current_flashcard[0]  # 현재 단어
        engine.say(word)  # 단어 발음을 음성 출력 엔진에 전달
        engine.runAndWait()  # 음성 출력

# 소리 버튼 생성
sound_image = tk.PhotoImage(file="sound.png")
sound_button = tk.Button(root, image=sound_image, command=play_word_pronunciation, bd=0, highlightthickness=0)
sound_button.place(x=700, y=100)

# 이미지 변경 함수

def change_image(event=None):
    # 현재 이미지 객체 확인
    current_image = image_button.cget("image")
    if current_image == str(black_tree_image):
        image_button.config(image=star_image)
    else:
        image_button.config(image=black_tree_image)

# 초기 이미지 설정
black_tree_image = Image.open("black_star.png")
black_tree_image = black_tree_image.resize((50, 50), Image.Resampling.LANCZOS)  # 이미지 크기 조정
black_tree_image = ImageTk.PhotoImage(black_tree_image)
star_image = Image.open("star.png")
star_image = star_image.resize((50, 50), Image.Resampling.LANCZOS)  # 이미지 크기 조정
star_image = ImageTk.PhotoImage(star_image)
image_button = tk.Button(root, image=black_tree_image, bd=0, highlightthickness=0)
image_button.place(x=600, y=100)
image_button.bind("<Button-1>", change_image)



root.mainloop()