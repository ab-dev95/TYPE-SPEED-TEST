from tkinter import *
from tkinter import messagebox
import random


font = ('Ariel', 12, 'bold')


with open('data/sentences.txt', 'r') as f:
    data = f.read()
    word_list = data.split(' ')
game_list = []
correct_words = []
failed_words = []
minutes = 1


def words():
    add = True
    while add:
        word = random.choice(word_list)
        if word in game_list:
            word = random.choice(word_list)
        else:
            game_list.append(word)

        if len(game_list) == 70:
            add = False


def get_text(_, txt, lb, lb1):
    word = txt.get("1.0", "end-1c")
    ans_list = word.split(' ')
    
    for i in ans_list:
        if i != '':
            if i == game_list[ans_list.index(i)]:
                msg.tag_config(i, foreground='green')  
                if i not in correct_words:
                    correct_words.append(i) 
            else:
                if i not in failed_words:
                    failed_words.append(i) 
                fail = game_list[ans_list.index(i)]
                msg.tag_config(fail, foreground='red')
                i = fail

            msg.config(state=NORMAL)
            num = msg.search(i, '1.0', 'end')
            offset = f'+{len(i)}c'
            num_end = num + offset
            msg.tag_add(i, num, num_end)
            msg.config(state=DISABLED)
    calculate(lb, lb1)


def calculate(lb, lb1):
    global acc, gwpm, wpm, err
    length = 0
    for i in correct_words:
        length += len(i)

    for i in failed_words:
        length += len(i)
    gwpm = (length / 5) / minutes

    lb.config(text=f'GWPM: {gwpm:.2f}')

    err = len(failed_words) / minutes
    wpm = gwpm - err

    lb1.config(text=f'WPM: {wpm:.2f}')

    tl_wrds = len(correct_words) + len(failed_words)
    ct_wrds = len(correct_words)
    acc = (ct_wrds / tl_wrds) * 100


def insert_text(txt):
    if len(game_list) == 0:
        words()

    text = '  '.join(item for item in game_list)
    txt.config(state=NORMAL)
    txt.insert('end', text)
    txt.config(state=DISABLED)

    millsec = minutes * 60 * 1000
    root.after(millsec, end)


def end():
    final_text = f'Final Gross Words Per Minute: {gwpm:.2f}\nFinal Word Per Minute: {wpm:.2f}\nError Rate: {err:.2f}\nAccuracy: {acc:.2f}'
    messagebox.showinfo('Message', final_text)
    restart(result_frame, msg_frame, input_frame)
    msg.config(state=NORMAL)
    msg.insert('end', final_text)
    msg.config(state=DISABLED)


def restart(f1, f2, f3): 
    global game_list
    f1.destroy()
    f2.destroy()
    f3.destroy()
    design()
    game_list = []


root = Tk()
root.title('Typing Speed Test')


def design():
    global msg, result_frame, msg_frame, input_frame
    result_frame = Frame(root, width=50)
    result_frame.grid(column=0, row=0, pady=10)

    msg_frame = Frame(root, height=20, width=50)
    msg_frame.grid(column=0, row=1, padx=10)

    input_frame = Frame(root, height=20, width=50)
    input_frame.grid(column=0, row=2, pady=15)

    msg = Text(msg_frame, width=50, height=10, font=font, wrap=WORD, state=DISABLED)
    msg.pack()

    txt = Text(input_frame, width=50, height=10, font=font, wrap=WORD)
    txt.pack()

    lb = Label(result_frame, text=f'GWPM: 00.00', font=font)
    lb.grid(column=0, row=0)

    lb1 = Label(result_frame, text=f'WPM: 00.00', font=font)
    lb1.grid(column=1, row=0, padx=50)

    btn = Button(result_frame, text='Restart', fg='white', bg='red', font=font, command=lambda: restart(result_frame, msg_frame, input_frame))
    btn.grid(column=3, row=0)

    btn1 = Button(result_frame, text='Start', fg='white', bg='green', font=font, command=lambda: insert_text(msg))
    btn1.grid(column=2, row=0, padx=10)

    root.bind('<space>', lambda i: get_text(i, txt, lb, lb1))

design()


root.mainloop()