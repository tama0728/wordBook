import tkinter as tk
from tkinter import ttk
import subprocess

def run_program(program_name):
    root.destroy()  # 현재 창 종료
    subprocess.run(["python", f"{program_name}.py"])

def create_program_button(root, program_name, command):
    button = ttk.Button(root, text=program_name, command=command)
    button.configure(style="Home.TButton")
    return button

root = tk.Tk()
root.title("Home")
root.configure(bg="white")
root.geometry("500x300")

# 스타일 지정
style = ttk.Style()
style.configure("Home.TButton", font=("Arial", 14), padding=10, width=15)

# 프로그램 버튼 생성
vocabulary_button = create_program_button(root, "Vocabulary", lambda: run_program("vocabulary"))
vocabulary_button.grid(row=0, column=0, padx=20, pady=20)

flashcard_button = create_program_button(root, "Wordcard", lambda: run_program("wordCard"))
flashcard_button.grid(row=0, column=1, padx=20, pady=20)

game_button = create_program_button(root, "Game", lambda: run_program("game"))
game_button.grid(row=1, column=0, padx=20, pady=20)

test_button = create_program_button(root, "Test", lambda: run_program("test"))
test_button.grid(row=1, column=1, padx=20, pady=20)

root.mainloop()