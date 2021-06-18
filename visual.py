from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from main import *
text="""Функция: {функция}
1) T0
Функция принадлежит классу T0, если на нулевом наборе она принимает значение 0.
На нулевом наборе значение функции равно {значение0}, поэтому функция {принадлежит0} классу T0.
2) T1
Функция принадлежит классу T1, если на единичном наборе она принимает значение 1.
На единичном наборе значение функции равно {значение1}, поэтому функция {принадлежит1} классу T1.
3) L
Функция принадлежит классу линейных функций (L), если её полином Жегалкина не содержит произведений.
Полином Жегалкина функции: {полином}. Полином {содержит} произведения, поэтому функция {принадлежитl} классу L.
4) M
Функция принадлежит классу монотонных функций (M), если для любой пары наборов α и β таких, что α ≤ β, выполняется условие f(α) ≤ f(β).
{набор}
Таким образом функция {принадлежитm} классу M.
5) S
Функция принадлежит классу самодвойственных функций (S), если на противоположных наборах она принимает противоположные значения. Проверяем:
{наборs}
Поэтому функция {принадлежитs} классу S

Критерий Поста: {поста}
"""



variable = []

buttons = ((' A ', ' B ', ' C ', ' D ', '4'),
           (' ¬', ' & ', ' ⋁ ', ' ⊕ ', '4'),
           (' → ', ' ↑ ', ' ↓ ', ' ≡ ', '4'),
           (' ( ', ' ) ', 'CE', ' F ', '4'),
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
        messagebox.showerror("ERROR", "Wrong function: "+str(value))
    arr = karno(match, v1)
    kstr = karta_karno(match, v1)
    m = arr[0]
    n = arr[1:]
    for widget in Frame22.winfo_children():
        widget.destroy()
    table = Table(Frame22, headings=m, rows=n)
    table.pack(side=TOP)
    message3.set("")
    message3.set(kstr)
    fic = fictivn(match, v1)
    if fic == "":
        message4.set("Все переменные существенные")
    else:
        message4.set("Фиктивные переменные: "+fic)

def dopol(entry):
    value = get_value(entry)
    try:
        v, v1, match = truthTable(value)
    except:
        messagebox.showerror("ERROR", "Wrong function: " + str(value))
    Text31.delete(1.0, END)
    Text31.insert(1.0, "СКНФ: "+ scnf(v, v1, match) +"\n\nСДНФ: "+ sdnf(v, v1, match) +" \n\nПолином Жегалкина: "+ polinom(v1, v, match))

def get_value(entryWidget):
    value = entryWidget.get()
    try:
        return str(value)
    except ValueError:
        return None

def savef(value, Text):
    a = Text.get("1.0", END)
    with open("bfunctions/"+value + '.txt', 'w', encoding="utf-8") as f:
        f.write(a)
        f.close()


def check(text, variable):
    arr = [TRUE, TRUE, TRUE, TRUE, TRUE]
    message1.set(message1.get() + " " + text + ", ")
    for i in variable:
        for j in range(5):
            arr[j] = arr[j] and i[j][1]
    if (sum(arr) == 0):
        message2.set("Полная")
    else:
        message2.set("Не полная. Система булевых функций принадлежит: ")
        for i in range(5):
            if (arr[i] == TRUE):
                message2.set(message2.get() + variable[0][i][0] + ", ")

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
        messagebox.showerror("ERROR", "Wrong function: "+str(value))
    m = match
    m.append('Y')
    table = Table(Frame2, headings=m, rows=v1)
    table.pack(side=LEFT)
    a, b, _ = Post(v, v1)
    variable.append(b)
    check(value, variable)
    table1 = Table(Frame2, headings=a, rows=b)
    table1.pack(side=LEFT, expand=True)

def check_Post2(entry):
    value = get_value(entry)
    try:
        v, v1, match = truthTable(value)
    except:
        messagebox.showerror("ERROR", "Wrong function: " + str(value))
    l, l1 = v.copy(), v1.copy()
    a, b, c = Post(l, l1)
    global text
    newWindow = Toplevel(root, bg="grey")
    newWindow.geometry('800x700')
    newWindow.title("Критерий Поста")
    buttonExample = Button(newWindow, text="Сохранить",
       command=lambda: [savef(value, Textn1)])
    buttonExample.pack(side=TOP, padx=5, pady=5)
    Textn1 = Text(newWindow, font='Times 15', wrap=WORD)
    Textn1.pack(side=TOP,fill=BOTH, expand = TRUE, padx=5, pady=5)
    Textn1.delete(1.0, END)
    if b[0][1] == TRUE:
        принадлежит0 = 'принадлежит'
    else:
        принадлежит0 = 'не принадлежит'
    if b[1][1] == TRUE:
        принадлежит1 = 'принадлежит'
    else:
        принадлежит1 = 'не принадлежит'

    if  b[3][1] == TRUE:
        принадлежитm = "принадлежит"
        набор = "Нет наборов на которых нарушается условие"
    else:
        принадлежитm = "не принадлежит"
        набор = "На наборах " + str(v1[c[1][1]][:-1])+" < "+str(v1[c[1][0]][:-1])+" значения функции "+\
                str(int(v1[c[1][1]][-1]))+" > "+str(int(v1[c[1][0]][-1]))+" - условие нарушается"

    if  b[2][1] == TRUE:
        принадлежитs = "принадлежит"
        наборs = "Нет противороложных наборов на которых нарушается условие"
    else:
        принадлежитs = "не принадлежит"
        наборs = "На противороложных наборах " + str(v1[c[0][1]][:-1])+" и "+str(v1[c[0][0]][:-1])+" значения функции "+\
                str(int(v1[c[0][1]][-1]))+" = "+str(int(v1[c[0][0]][-1]))+" - условие нарушается"

    полином = polinom(v1, v, match)
    if  b[4][1] == TRUE:
        принадлежитl = "принадлежит"
        содержит = "не содержит"
    else:
        принадлежитl = "не принадлежит"
        содержит = "содержит"

    ind = FALSE
    tmp=""
    for j in b:
        ind = ind or j[1]

    if (ind == FALSE):
        поста="Полная"
    else:
        поста="Не полная. Функция принадлежит: "
        for i in range(5):
            if (b[i][1] == TRUE):
                tmp = tmp + b[i][0] + ", "
        поста=поста+tmp
        поста=поста[:-2]


    text1 = text.format(функция= value, значение0 = int(not b[0][1]), значение1 = int(b[1][1]),
                       принадлежит0 = принадлежит0, принадлежит1 = принадлежит1,
                       полином = полином, принадлежитl = принадлежитl, содержит = содержит,
                       принадлежитm = принадлежитm, набор = набор,
                       принадлежитs=принадлежитs, наборs=наборs, поста=поста)

    Textn1.insert(1.0, text1)



def click(text):
    if text == 'CE':
        message.set('')
    else:
        Entry1.insert(Entry1.index(INSERT), text)
        # message.set(message.get() + text )

root = Tk()
root.geometry('800x700')
root.title("Булевый калькулятор")
tab_control = ttk.Notebook(root)

f1 = Frame(root, bg='grey')
f3 = Frame(root, bg='grey')
f2 = Frame(root, bg='grey')

tab_control.add(f1, text='Критерий Поста')
tab_control.pack(fill="both", side="top", expand=True)
tab_control.add(f3, text='СКНФ/СДНФ/Полином Жегалкина')
tab_control.pack(fill="both", side="top", expand=True)
tab_control.add(f2, text='Карта Карно')
tab_control.pack(fill="both", side="top", expand=True)

message = StringVar()
message1 = StringVar()
message2 = StringVar()
message3 = StringVar()
message4 = StringVar()
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
Frame31 = Frame(f3, bg='grey')
Frame31.pack(side=TOP, fill="both")

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
Entry3 = Entry(Frame31, textvariable=message, width=60)
Entry3.pack(side=TOP, padx=5, pady=5)

Label2 = Label(Frame12, textvariable=message1, width=80)
Label2.pack(side=TOP, padx=5, pady=5)
Label3 = Label(Frame12, textvariable=message2, width=80)
Label3.pack(side=TOP, padx=5, pady=5)
Label4 = Label(f2, textvariable=message3, width=60)
Label4.pack(side=TOP, padx=5, pady=5)

Label5 = Label(f2, textvariable=message4, width=60)
Label5.pack(side=TOP, padx=5, pady=5)

# Текстовые поля
Text31 = Text(f3, width=100, height=30, font='Times')
Text31.pack(side=TOP,fill=BOTH, expand = TRUE, padx=5, pady=5)
Text31.insert(1.0, "СКНФ: \n\nСДНФ: \n\nПолином Жегалкина: ")

# Кнопки
Button(Frame1, text='Проверить критерий Поста',
       command=lambda: [check_Post(Entry1)]).pack()
Button(Frame1, text='Полный ответ',
       command=lambda: [check_Post2(Entry1)]).pack()
Button(Frame12, text='Очистить',
       command=lambda: [cleanPost()]).pack(side=TOP)
Button(Frame21, text='карта Карно',
       command=lambda: [karno_tab(Entry2)]).pack(side=TOP)
Button(Frame31, text='Построить',
       command=lambda: [dopol(Entry2)]).pack(side=TOP)

root.mainloop()
