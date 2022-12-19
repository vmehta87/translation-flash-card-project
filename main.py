from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
to_learn = {}

try:
    data = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv('data/french_words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')


def next_word():
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = choice(to_learn)
    canvas.itemconfig(canvas_image, image=front_card)
    canvas.itemconfig(card_title, text='French')
    canvas.itemconfig(card_word, text=current_word['French'])
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text='English')
    canvas.itemconfig(canvas_image, image=back_card)
    canvas.itemconfig(card_word, text=current_word['English'])


def is_known():
    to_learn.remove(current_word)
    data = pandas.DataFrame(to_learn)
    data.to_csv('data/words_to_learn.csv', index=False)
    next_word()


window = Tk()
window.title('Flash Cards')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)


canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card = PhotoImage(file='images/card_front.png')
back_card = PhotoImage(file='images/card_back.png')
canvas_image = canvas.create_image(400, 263, image=front_card)
card_title = canvas.create_text(400, 150, text='French', font=('Arial', 40, 'italic'))
card_word = canvas.create_text(400, 263, text='word', font=('Arial', 60, 'bold'))
canvas.grid(column=0, columnspan=2, row=0)

wrong_image = PhotoImage(file='images/wrong.png')
wrong = Button(image=wrong_image, highlightthickness=0, command=next_word)
wrong.grid(column=0, row=1)
right_image = PhotoImage(file='images/right.png')
right = Button(image=right_image, highlightthickness=0, command=is_known)
right.grid(column=1, row=1)

next_word()

window.mainloop()
