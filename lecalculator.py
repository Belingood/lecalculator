import re
from operator import add, sub, mul, truediv
from decimal import *


calc_context = Context(prec=12, rounding=ROUND_05UP, Emin=-99999999, Emax=99999999, capitals=0, clamp=1,
                       flags=[], traps=[InvalidOperation, DivisionByZero, Overflow])
setcontext(calc_context)


class LECalculator:
    """
    The purpose of each method is described in detail in the test_lecalculator file.
    """

    __OPERATORS = ('+', '-', '*', '/')

    @classmethod
    def calculator(cls, expression):
        if cls.data_checker(expression):
            expression = expression.replace(' ', '')
            while expression.count('(') != 0 or expression.count(')') != 0:
                parentheses_ind = cls.__max_deep_indexes(expression)
                for i in range(0, len(parentheses_ind), 2):
                    left, right = parentheses_ind[i], parentheses_ind[i + 1]
                    content = expression[left + 1: right]
                    res = cls.__instead_parentheses_result(content)
                    expression = expression[: left] + res.ljust(len(content) + 2, ' ') + expression[right + 1:]
                    if '{ZeroDivisionError}' in res:
                        return expression.replace(' ', '')
                expression = expression.replace(' ', '')
            expression = expression.replace(' ', '')
            return cls.__instead_parentheses_result(expression)
        return f"Looks like the expression '{expression}' is not spelled correctly."

    @classmethod
    def data_checker(cls, data):
        if not type(data) is str:
            return False
        data = data.replace(' ', '')
        check_first_last = data[0] not in '.)/*' and data[-1] not in '(.+-*/'
        check_symbols = all(filter(lambda x: x in '.()0123456789+-*/', data))
        check_parenthesis = ''.join(filter(lambda x: x in '()', data))
        check_wrong_pairs = not re.search(r'(\d\(|\)\d|\.\(|\.\)|\(\.|\)\.)', data)
        while '()' in check_parenthesis:
            check_parenthesis = check_parenthesis.replace('()', '')
        return all((len(data) > 2, check_first_last, check_symbols, check_wrong_pairs, not check_parenthesis))

    @classmethod
    def __max_deep_indexes(cls, exp):
        level = ind = 0
        res = []
        flag = True
        for i in range(len(exp)):
            ind += ((0, -1)[exp[i] == ')'], 1)[exp[i] == '(']
            if (ind - level) == 1:
                level += 1
                res = []
                flag = False
                res.append(i)
            if (ind - level == -1) and not flag:
                res.append(i)
                flag = True
            if (ind == level) and flag:
                res.append(i)
                flag = False
        return res

    @classmethod
    def __is_first_minus_plus(cls, parentheses_content):
        return parentheses_content[:1] in cls.__OPERATORS[:2]

    @classmethod
    def __is_single_number(cls, parentheses_content):
        pc = parentheses_content[cls.__is_first_minus_plus(parentheses_content):]
        return not any(map(lambda x: x in pc, cls.__OPERATORS))

    @classmethod
    def __instead_parentheses_result(cls, parentheses_content):
        if cls.__is_single_number(parentheses_content):
            return parentheses_content
        else:
            return cls.__calculation(cls.__num_separated_operators(parentheses_content))

    @classmethod
    def __num_separated_operators(cls, exp_without_parentheses):
        ewp = exp_without_parentheses
        match = r'^[\-\+]?\d+(\.{1}\d+)?'
        buf = []
        start = 0
        num = True
        while num:
            num = re.search(match, ewp[start:])
            if num:
                buf.append(num[0])
                start += len(num[0])
                if ewp[start:]:
                    buf.append(ewp[start])
                    start += 1
        return buf

    @classmethod
    def __operators_finder(cls, op1, op2, nso):
        op_count = nso.count(op1) + nso.count(op2)
        for _ in range(op_count):
            op_ind = min((nso.index(op1) if op1 in nso else 100_000), (nso.index(op2) if op2 in nso else 100_000))
            res = cls.__action(nso[op_ind - 1], nso[op_ind + 1], nso[op_ind])
            nso = nso[:op_ind - 1] + [res] + nso[op_ind + 2:]
            if '{ZeroDivisionError}' in res:
                return nso
        return nso

    @classmethod
    def __action(cls, num1, num2, op):
        try:
            return str({'+': add, '-': sub, '*': mul, '/': truediv}[op](Decimal(num1), Decimal(num2)))
        except ZeroDivisionError:
            return '{ZeroDivisionError}'

    @classmethod
    def __calculation(cls, numbers_separated_operators):
        nso = cls.__operators_finder('*', '/', numbers_separated_operators)
        if '{ZeroDivisionError}' in nso:
            return ''.join(nso)
        return ''.join(cls.__operators_finder('+', '-', nso))
