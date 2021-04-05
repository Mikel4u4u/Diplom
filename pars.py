import re

def change_rImplies(matchobj):
    result = re.findall(r'\b\w\b', matchobj.group(0))
    return " Implies( " + result[0] + ", " + result[1] + ") "


def change1_rImplies(matchobj):
    result = re.findall(r'(\(?\s*\w*\(.*?\)\s*\)?|\b\w\b)', matchobj.group(0))
    return "Implies(" + result[0] + ", " + result[1] + ")"


def rImplies(s):
    result = re.sub(r'\b\w\b\s*\→\s*\b\w\b', change_rImplies, s)
    result = re.sub(r'(\(?\s*\w*\(.*?\)\s*\)?|\b\w\b)\s*\→\s*(\(?\s*\w*\(.*?\)\s*\)?|\b\w\b)', change1_rImplies, result)
    print(result)
    return result

def change_rNand(matchobj):
    result = re.findall(r'\b\w\b', matchobj.group(0))
    return "Nand(" + result[0] + ", " + result[1] + ")"


def change1_rNand(matchobj):
    result = re.findall(r'(\(?\s*\w*\(.*?\)\s*\)?|\b\w\b)', matchobj.group(0))
    return "Nand(" + result[0] + ", " + result[1] + ")"


def rNand(s):
    result = re.sub(r'\b\w\b\s*\↑\s*\b\w\b', change_rNand, s)
    result = re.sub(r'(\(?\s*\w*\(.*?\)\s*\)?|\b\w\b)\s*\↑\s*(\(?\s*\w*\(.*?\)\s*\)?|\b\w\b)', change1_rNand, result)
    return result

def change_rNor(matchobj):
    result = re.findall(r'\b\w\b', matchobj.group(0))
    return "Nor(" + result[0] + ", " + result[1] + ")"


def change1_rNor(matchobj):
    result = re.findall(r'(\(?\s*\w*\(.*?\)\s*\)?|\b\w\b)', matchobj.group(0))
    return "Nor(" + result[0] + ", " + result[1] + ")"


def rNor(s):
    result = re.sub(r'\b\w\b\s*\↓\s*\b\w\b', change_rNor, s)
    result = re.sub(r'(\(?\s*\w*\(.*?\)\s*\)?|\b\w\b)\s*\↓\s*(\(?\s*\w*\(.*?\)\s*\)?|\b\w\b)', change1_rNor, result)
    return result

def change_rEquivalent(matchobj):
    result = re.findall(r'\b\w\b', matchobj.group(0))
    return "Equivalent(" + result[0] + ", " + result[1] + ")"


def change1_rEquivalent(matchobj):
    result = re.findall(r'(\(?\s*\w*\(.*?\)\s*\)?|\b\w\b)', matchobj.group(0))
    return "Equivalent(" + result[0] + ", " + result[1] + ")"


def rEquivalent(s):
    result = re.sub(r'\b\w\b\s+\≡\s*\b\w\b', change_rEquivalent, s)
    result = re.sub(r'(\(?\s*\w*\(.*?\)\s*\)?|\b\w\b)\s*\≡\s*(\(?\s*\w*\(.*?\)\s*\)?|\b\w\b)', change1_rEquivalent, result)
    return result

def rall(expression):
    expression = rImplies(expression)
    expression = rNand(expression)
    expression = rNor(expression)
    expression = rEquivalent(expression)

    return expression
