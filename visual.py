from tkinter import *
from tkinter import ttk
from main import truthTable, Post , karno, karta_karno

variable = []

buttons = (('A', 'B', 'C', 'D', '4'),
           ('¬', '&', '⋁', '⊕', '4'),
           ('→', '↑', '↓', '≡', '4'),
           ('(', ')', 'CE', 'F', '4'),
           )


class Table(Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings
        for head in headings:
            table.heading(head, text=head, anchor=CENTER)
            table.column(head, width=70, anchor=CENTER, )

        for row in rows:
            table.insert('', END, values=tuple(row))

        scrolltable = Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=RIGHT, fill=Y)
        table.pack(expand=YES, fill=BOTH)

def karno_tab(entry):
    value = get_value(entry)

    try:
        v, v1, match = truthTable(value)
    except:
        print("ERROR")
    arr=karno(match, v1)
    kstr = karta_karno(match, v1)
    m=arr[0]
    n=arr[1:]
    for widget in Frame22.winfo_children():
        widget.destroy()
    table = Table(Frame22, headings=m, rows=n)
    table.pack(side=TOP)
    message3.set("")
    message3.set(kstr)




def get_value(entryWidget):
    value = entryWidget.get()
    try:
        return str(value)
    except ValueError:
        return None


def check(text, variable):
    arr=[TRUE,TRUE,TRUE,TRUE,TRUE]
    message1.set(message1.get() + " " + text + ", ")
    for i in variable:
        for j in range(5):
            arr[j]=arr[j] and i[j][1]
    if(sum(arr)==0):
        message2.set("Полная")
    else:
        message2.set("Не полная. Система булевых функций принадлежит: ")
        for i in range(5):
            if(arr[i]==TRUE):
                message2.set(message2.get()+variable[0][i][0]+", ")

def cleanPost():
    message1.set("Система булевых функций: ")
    message2.set("")
    variable.clear()

def check_Post(entry):
    global variable

    for widget in Frame2.winfo_children():
        widget.destroy()
    value = get_value(entry)
    try:
        v, v1, match = truthTable(value)
    except:
        print("ERROR")
    m = match
    m.append('Y')
    table = Table(Frame2, headings=m, rows=v1)
    table.pack(side=LEFT)
    a, b = Post(v, v1)
    variable.append(b)
    check(value, variable)
    table1 = Table(Frame2, headings=a, rows=b)
    table1.pack(side=LEFT, expand=True)


def click(text):
    if text == 'CE':
        message.set('')
    else:
        message.set(message.get() + " " + text + " ")


root = Tk()
root.geometry('800x700')
tab_control = ttk.Notebook(root)
f1 = Frame(root, bg='grey')
f2 = Frame(root, bg='grey')
tab_control.add(f1, text='Критерий Поста')
tab_control.pack(fill="both", side="top", expand=True)

tab_control.add(f2, text='Карта Карно')
tab_control.pack(fill="both", side="top", expand=True)

message = StringVar()
message1 = StringVar()
message2 = StringVar()
message3 = StringVar()

message1.set("Система булевых функций: ")

# Фреймы
Frame1 = Frame(f1, bg='green')
Frame1.pack(side=TOP)

Frame11 = Frame(f1, bg='blue')
Frame11.pack(side=TOP)

Frame12 = Frame(f1, bg='grey')
Frame12.pack(side=TOP, fill="both")

Frame21 = Frame(f2, bg='grey')
Frame21.pack(side=TOP, fill="both")

Frame22 = Frame(f2, bg='grey')
Frame22.pack(side=TOP, fill="both")

# Кнопки
for row in range(4):
    for col in range(4):
        button = Button(Frame11, text=buttons[row][col],
                        command=lambda row=row, col=col: click(buttons[row][col]))
        button.grid(row=row + 2, column=col, sticky="nsew", ipadx=10, ipady=10)

Frame2 = Frame(f1, bg='blue')
Frame2.pack(side=BOTTOM, expand=True)

Entry1 = Entry(Frame1, textvariable=message, width=60)
Entry1.pack(side=TOP, padx=5, pady=5)

Entry2 = Entry(Frame21, textvariable=message, width=60)
Entry2.pack(side=TOP, padx=5, pady=5)

Label2 = Label(Frame12, textvariable=message1, width=60)
Label2.pack(side=TOP, padx=5, pady=5)
Label3 = Label(Frame12, textvariable=message2, width=60)
Label3.pack(side=TOP, padx=5, pady=5)
Label4 = Label(f2, textvariable=message3, width=60)
Label4.pack(side=TOP, padx=5, pady=5)



Button(Frame1, text='Проверить критерий Поста',
       command=lambda: [check_Post(Entry1)]).pack()
Button(Frame12, text='Очистить',
       command=lambda: [cleanPost()]).pack(side=TOP)

Button(Frame21, text='карта Карно',
       command=lambda: [karno_tab(Entry2)]).pack(side=TOP)
root.mainloop()