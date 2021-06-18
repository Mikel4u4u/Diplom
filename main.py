from pars import *
import itertools
import qm
import re
from math import log


def check(match, k):
    kstr = ""
    for i in range(len(k)):
        if k[i] == "1":
            kstr = kstr + str(match[i]) + " & "
        elif k[i] == "0":
            kstr = kstr + str(match[i]) + "'" + " & "
        else:
            continue
    kstr = kstr[:-3]
    kstr = "( " + kstr + " )"
    return kstr

def check1(match, k):
    kstr = ""
    for i in range(len(k) - 1):
        if k[i] == 1:
            kstr = kstr + str(match[i]) + " & "
        elif k[i] == 0:
            kstr = kstr + str(match[i]) + "'" + " & "
        else:
            continue
    kstr = kstr[:-3]
    kstr = "( " + kstr + " )"
    return kstr


def sdnf(v, v1, match):
    kstr = ""
    for i in range(len(v1)):
        if v1[i][-1] == True:
            kstr = kstr + check1(match, v1[i]) + " ⋁ "
    kstr = kstr[:-3]
    if kstr == '':
        kstr="не существует"
    return kstr


def check2(match, k):
    kstr = ""
    for i in range(len(k) - 1):
        if k[i] == 0:
            kstr = kstr + str(match[i]) + " ⋁ "
        elif k[i] == 1:
            kstr = kstr + str(match[i]) + "'" + " ⋁ "
        else:
            continue
    kstr = kstr[:-3]
    kstr = "( " + kstr + " )"
    return kstr

def scnf(v, v1, match):
    kstr = ""
    for i in range(len(v1)):
        if v1[i][-1] == False:
            kstr = kstr + check2(match, v1[i]) + " & "
    kstr = kstr[:-3]
    if kstr == '':
        kstr="не существует"
    return kstr

def check3(match, k):
    kstr = ""
    for i in range(len(k) - 1):
        if k[i] == 1:
            kstr = kstr + str(match[i]) + " & "
        elif k[i] == 0:
            continue
    kstr = kstr[:-3]
    kstr = "( " + kstr + " )"
    return kstr

def polinom(values, valuesy, match):
    kstr = ""
    for i in range(len(values)):
        if valuesy[0] == True:
            if i == 0:
                kstr = kstr + "1 ⊕ "
            else:
                kstr = kstr + check3(match, values[i]) + " ⊕ "

        for j in range(len(valuesy) - 1):
            valuesy[j] = valuesy[j] ^ valuesy[j + 1]
        valuesy.pop()
    kstr = kstr[:-3]
    return kstr

def T0(values):
    if not values[0]:
        return True
    else:
        return False

def T1(values):
    if values[-1]:
        return True
    else:
        return False

def S(values):
    for i in range(len(values) // 2):
        if (values[i] == values[len(values) - 1 - i]):
            return False, [i, len(values) - 1 - i]
    else:
        return True, "Yes"

def M(values):
    for i in range(len(values) - 1):
        for j in range(i + 1, len(values)):
            if values[j][-1] < values[i][-1]:
                s = 0
                for t in range(len(values[0]) - 1):
                    if values[j][t] >= values[i][t]:
                        s = s + 1
                    if s == len(values[0]) - 1:
                        return False, [j, i]
    return True, "NO"

def L(values, valuesy):
    for i in range(len(values)):
        if sum(values[i][:-1]) > 1 and valuesy[0] == True:
            return False

        for j in range(len(valuesy) - 1):
            valuesy[j] = valuesy[j] ^ valuesy[j + 1]
        valuesy.pop()
    return True

def mass_to_str(a):
    s = ''
    for i in a:
        s = s + str(i)
    return s

def fictivn(match, v1):
    arr=""
    for j in range(len(match)):
        tmp=0
        t=2**(len(match)-(j+1))
        for i in range(len(v1)):
            if v1[i][j]==0:
                if v1[i][-1] == v1[i+t][-1]:
                    tmp = tmp+1
        if tmp == (len(v1)/2):
            arr = arr+ str(match[j])+" "
    return arr

def Post(v, v1):
    a = ["Критерий", "True/False"]
    s, s1 = S(v)
    m, m1 = M(v1)
    b = [["T0", T0(v)], ["T1", T1(v)], ["S", s], ["M", m], ["L", L(v1, v)]]
    return a, b, [s1, m1]

def karno(match, v1):
    arr1 = []
    arr2 = []
    arr3 = []
    print("Karta Karno")
    a = len(match) // 2
    b = len(match) - a
    a1 = 2 ** a + 1
    b1 = 2 ** b + 1

    mas = []
    for i in range(a1):
        mas.append([])
        for j in range(b1):
            mas[i].append(0)

    for i in range(len(v1)):
        arr1.append(mass_to_str(v1[i][:a]))
        arr2.append(mass_to_str(v1[i][a:-1]))
        arr3.append(int(v1[i][-1]))

    arr3 = reshape(arr3, (a1 - 1, b1 - 1))
    arr1 = list(set(arr1))
    arr2 = list(set(arr2))
    arr1.sort()
    arr2.sort()
    for i in range(a1):
        for j in range(b1):
            if j != 0:
                mas[0][j] = arr2[j - 1]
            if i != 0:
                mas[i][0] = arr1[i - 1]
            mas[i][j] = arr3[i - 1][j - 1]

    if len(mas[0]) == 5:
        for i in range(a1):
            tmp = mas[i][3]
            mas[i][3] = mas[i][4]
            mas[i][4] = tmp
        if len(mas) == 5:
            tmp = mas[3]
            mas[3] = mas[4]
            mas[4] = tmp

    mas[0][0] = mass_to_str(match[:a]) + "/" + mass_to_str(match[a:])
    for i in mas:
        print(i)

    return mas

def karta_karno(match, v):
    mas = []
    mas0 = []
    kstr = ""
    for i in range(len(v)):
        if v[i][-1] == True:
            mas.append(i)

    for i in range(len(v)):
        if v[i][-1] == False:
            mas0.append(i)

    if len(mas) == len(v):
        return "TRUE"
    elif len(mas) == 0:
        return "FALSE"

    arr = qm.qm(ones=mas, zeros=mas0)
    print(arr)
    for i in range(len(arr)):
        if i == len(arr) - 1:
            kstr = kstr + check(match, arr[i])
        else:
            kstr = kstr + check(match, arr[i]) + " ⋁ "
    return kstr

def truthTable(expression):
    # Для векторного представления функции
    t = re.fullmatch(r'[01]+', expression)
    if t:
        Logn = log(len(t[0]), 2)
        if (Logn == int(Logn)):
            match = []
            bases2 = []
            bases = [int(c) for c in expression]
            bases1 = list(itertools.product([0, 1], repeat=int(Logn)))
            for i in range(len(bases)):
                bases2.append(list(bases1[i]))
                bases2[i].append(bases[i])
            for i in range(int(Logn)):
                match.append(chr(97 + i))
            return bases, bases2, match
    # Для обычного представления функции
    match = re.findall(r'\b[a-zA-Zа-яА-ЯёЁ]\d?\b', expression)
    match = list(set(match))
    match.sort()

    print("Boolean Expression:")
    print("  X = " + expression.upper())
    expression = re.sub(r'\b[1]\b', r'True', expression)
    expression = re.sub(r'\b[0]\b', r'False', expression)
    a = Truths(match, [expression])
    v, v1 = a.my_func()


    return v, v1, match

if __name__ == "__main__":
    expression = "A  → ¬ B & ¬ C ⊕ B"
    v, v1, match = truthTable(expression)
    l = v.copy()
    l1 = v1.copy()

    # print("T0: ", T0(v))
    # print("T1: ", T1(v))
    #print("S: ", S(v))
    #print("M: ", M(v1))
    #print("L: ", L(v1, v))
    #karno(match, v1)
    #print(karta_karno(match, v1))
    #print(sdnf(v, v1, match))
    #print(scnf(v, v1, match))
    #print(polinom(l1, l, match))
    # print(fictivn(match, v1))
    # print("_____________")
    # print()
