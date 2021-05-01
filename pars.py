from functools import reduce
from operator import mul
import itertools
import re
import pyparsing



# dict of boolean operations
OPERATIONS = {
    'not':      (lambda x: not x),
    '-':        (lambda x: not x),
    '~':        (lambda x: not x),
    '¬':        (lambda x: not x),

    'or':       (lambda x, y: x or y),
    '⋁':       (lambda x, y: x or y),
    'nor':      (lambda x, y: not (x or y)),
    '⊕':      (lambda x, y:  x ^ y),
    'xor':      (lambda x, y: x != y),

    'and':      (lambda x, y: x and y),
    '&':      (lambda x, y: x and y),
    'nand':     (lambda x, y: not (x and y)),
    '↑':     (lambda x, y: not (x and y)),
    '↓':     (lambda x, y: not (x or y)),

    '=>':       (lambda x, y: (not x) or y),
    '→':       (lambda x, y: (not x) or y),
    'implies':  (lambda x, y: (not x) or y),

    '=':        (lambda x, y: x == y),
    '≡':        (lambda x, y: x == y),
    '!=':       (lambda x, y: x != y),
}


def recursive_map(func, data):
    """Recursively applies a map function to a list and all sublists."""
    if isinstance(data, list):
        return [recursive_map(func, elem) for elem in data]
    else:
        return func(data)


def string_to_bool(string):
    """Converts a string to boolean if string is either 'True' or 'False'
    otherwise returns it unchanged.
    """
    if string == 'True':
        return True
    elif string == 'False':
        return False
    return string


def solve_phrase(phrase):
    """Recursively evaluates a logical phrase that has been grouped into
    sublists where each list is one operation.
    """
    if isinstance(phrase, bool):
        return phrase
    if isinstance(phrase, list):
        # list with just a list in it
        if len(phrase) == 1:
            return solve_phrase(phrase[0])
        # single operand operation
        if len(phrase) == 2:
            return OPERATIONS[phrase[0]](solve_phrase(phrase[1]))
        # double operand operation
        else:
            return OPERATIONS[phrase[1]](solve_phrase(phrase[0]),
                                         solve_phrase([phrase[2]]))


def group_operations(phrase):
    """Recursively groups logical operations into separate lists based on
    the order of operations such that each list is one operation.

    Order of operations is:
        not, and, or, implication
    """
    if isinstance(phrase, list):
        if len(phrase) == 1:
            return phrase
        for operator in ['not', '~', '-','¬']:
            while operator in phrase:
                index = phrase.index(operator)
                phrase[index] = [operator, group_operations(phrase[index+1])]
                phrase.pop(index+1)
        for operator in ['and','&', 'nand']:
            while operator in phrase:
                index = phrase.index(operator)
                phrase[index] = [group_operations(phrase[index-1]),
                                 operator,
                                 group_operations(phrase[index+1])]
                phrase.pop(index+1)
                phrase.pop(index-1)
        for operator in ['or','⋁', 'nor', 'xor']:
            while operator in phrase:
                index = phrase.index(operator)
                phrase[index] = [group_operations(phrase[index-1]),
                                 operator,
                                 group_operations(phrase[index+1])]
                phrase.pop(index+1)
                phrase.pop(index-1)
    return phrase


class Truths:
    """
    Class Truhts with modules for table formatting, valuation and CLI
    """

    def __init__(self, bases=None, phrases=None, ints=True, ascending=False):
        if not bases:
            raise Exception('Base items are required')
        self.bases = bases
        self.phrases = phrases or []
        self.ints = ints

        # generate the sets of booleans for the bases
        if ascending:
            order = [False, True]
        else:
            order = [True, False]

        self.base_conditions = list(itertools.product(order,
                                                      repeat=len(bases)))
        self.base_conditions.reverse()
        # regex to match whole words defined in self.bases
        # used to add object context to variables in self.phrases
        self.p = re.compile(r'(?<!\w)(' + '|'.join(self.bases) + r')(?!\w)')

        # uesd for parsing logical operations and parenthesis
        self.to_match = pyparsing.Word(pyparsing.alphanums)
        for item in itertools.chain(self.bases,
                                    [key for key, val in OPERATIONS.items()]):
            self.to_match |= item
        self.parens = pyparsing.nestedExpr('(', ')', content=self.to_match)

    def calculate(self, *args):
        """
        Evaluates the logical value for each expression
        """
        bools = dict(zip(self.bases, args))

        eval_phrases = []
        for phrase in self.phrases:
            # substitute bases in phrase with boolean values as strings
            phrase = self.p.sub(lambda match: str(bools[match.group(0)]), phrase)  # NOQA long line
            # wrap phrase in parens
            phrase = '(' + phrase + ')'
            # parse the expression using pyparsing
            interpreted = self.parens.parseString(phrase).asList()[0]
            # convert any 'True' or 'False' to boolean values
            interpreted = recursive_map(string_to_bool, interpreted)
            # group operations
            interpreted = group_operations(interpreted)
            # evaluate the phrase
            eval_phrases.append(solve_phrase(interpreted))

        # add the bases and evaluated phrases to create a single row
        row = [int(val) for key, val in bools.items()] + eval_phrases
        return row



    def myas_pandas(self):
        """
        Table as Pandas DataFrame
        """
        x = []
        y = []
        for conditions_set in self.base_conditions:
            x.append(self.calculate(*conditions_set))
            y.append(bool(self.calculate(*conditions_set)[-1]))
        return y, x

def reshape(lst, shape):
    if len(shape) == 1:
        return lst
    n = reduce(mul, shape[1:])
    return [reshape(lst[i*n:(i+1)*n], shape[1:]) for i in range(len(lst)//n)]