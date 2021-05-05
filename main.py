from pars import *
import qm
import re


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
            return False
    else:
        return True


def M(values):
    for i in range(len(values) - 1):
        for j in range(i + 1, len(values)):
            if values[j][-1] < values[i][-1]:
                s = 0
                for t in range(len(values[0]) - 1):
                    if values[j][t] >= values[i][t]:
                        s = s + 1
                    if s == len(values[0]) - 1:
                        return False
    return True


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


def Post(v, v1):
    a = ["Критерий", "True/False"]
    b = [["T0", T0(v)], ["T1", T1(v)], ["S", S(v)], ["M", M(v1)], ["L", L(v1, v)]]
    return a, b


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
    match = re.findall(r'\b\w\d?\b', expression)
    match = list(set(match))
    match.sort()

    print("Boolean Expression:")
    print("  X = " + expression.upper())

    a = Truths(match, [expression])
    v, v1 = a.my_as_pandas()
    print(match)
    for i in v1:
        print(i)
    return v, v1, match


if __name__ == "__main__":
    expression = " A  &  B  →   C     "
    v, v1, match = truthTable(expression)
    karno(match, v1)
    print(karta_karno(match, v1))
    print(sdnf(v, v1, match))
    print(scnf(v, v1, match))
    print(polinom(v1, v, match))
    # print("_____________")
    # print("T0: ", T0(v))
    # print("T1: ", T1(v))
    # print("S: ", S(v))
    # print("M: ", M(v1))
    # print("L: ", L(v1, v))
    # print()
