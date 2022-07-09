from datetime import datetime
import unittest
from decimal import *
import requests
import json
import psycopg2
from config import config

from lecalculator import LECalculator, calc_context

# Setting up and set the Decimal module context
test_calc_context = Context(prec=12, rounding=ROUND_05UP, Emin=-99999999, Emax=99999999, capitals=0, clamp=1,
                            flags=[], traps=[InvalidOperation, DivisionByZero, Overflow])
setcontext(test_calc_context)

# Operators dictionary from Calculator class
OPERATORS = getattr(LECalculator, '_LECalculator__OPERATORS')
# Dictionary equivalent to operators dictionary from Calculator class
TEST_OPERATORS = ('+', '-', '*', '/')


class TestLECalculator(unittest.TestCase):

    __RESULT_DATA = {}

    def __set_result(self, e=None, raiser=True):
        """
        The function of collecting test results. The results are collected
        in the __RESULT_DATA variable for subsequent entry into the database.
        :param e: Stores the content of the exception, if one has occurred.
        :param raiser: Whether to raise an exception or just handle it.
        """
        name = self.__dict__['_testMethodName']
        self.__RESULT_DATA[name] = (e is None,
                                    str(datetime.utcnow()),
                                    (e, str(e))[e is not None],
                                    )
        if e and raiser:
            raise e

    def test_001_get_data_method(self):
        """
        Testing a GET Request
        """
        e = None
        user_data = json.dumps({'result': '10'})
        exp = '5+5'
        url = f"http://127.0.0.1:8000/calculator/{exp}"
        try:
            r = requests.get(url)
            r.raise_for_status()
            result = json.dumps(r.json())
            assert user_data == result
        except (requests.exceptions.HTTPError, AssertionError, Exception) as err:
            e = err
        self.__set_result(e=e)

    def test_002__OPERATORS(self):
        """
        Check if the operators dictionary corrupted
        """
        e = None
        try:
            self.assertEqual(OPERATORS, TEST_OPERATORS)
        except AssertionError as err:
            e = err
        self.__set_result(e=e)

    def test_003_context(self):
        """
        Check if the context corrupted
        """
        e = None
        try:
            self.assertEqual(calc_context.prec, test_calc_context.prec)
            self.assertEqual(calc_context.rounding, test_calc_context.rounding)
            self.assertEqual(calc_context.Emin, test_calc_context.Emin)
            self.assertEqual(calc_context.Emax, test_calc_context.Emax)
            self.assertEqual(calc_context.clamp, test_calc_context.clamp)
        except AssertionError as err:
            e = err
        self.__set_result(e=e)

    def test_004_calculator(self):
        """
        Testing the main function that calculates the result.
        """
        e = None
        test_data = [('-5+(2-1)*4.5',  '-0.5'), ('5/0', '{ZeroDivisionError}')]
        try:
            for arg, answer in test_data:
                self.assertEqual(LECalculator.calculator(arg), answer)
        except AssertionError as err:
            e = err
        self.__set_result(e=e)

    def test_005_data_checker(self):
        """
        Testing a function that checks the input data for correctness.
        """
        e = None
        test_data = [('+5-3/(2+4)*2.3', True), (128, False), (')123-(56+23)*3', False), ('1(23)-(56+23)*3', False),
                     ('.59-34+71', False), ('125-65+', False), ('*25-36', False), ('(12+(2+1)-4*(1-4)', False)]
        try:
            for arg, answer in test_data:
                self.assertEqual(LECalculator.data_checker(arg), answer)
        except AssertionError as err:
            e = err
        self.__set_result(e=e)

    def test_006_max_deep_indexes(self):
        """
        Testing a function that extracts the indexes of the deepest
        level parentheses (whose content is evaluated first) from a mathematical expression.
        """
        e = None
        test_data = [('5+(17-(7+2.5))*(-2)', [6, 12]), ('5+(17-9.5)*(-2)', [2, 9, 11, 14])]
        try:
            for arg, answer in test_data:
                self.assertEqual(LECalculator._LECalculator__max_deep_indexes(arg), answer)
        except AssertionError as err:
            e = err
        self.__set_result(e=e)

    def test_007_is_first_minus_plus(self):
        """
        Testing a function that checks whether the first
        character of an expression is plus or minus.
        """
        e = None
        test_data = [('7+2.5', False), ('-7+2.5', True)]
        try:
            for arg, answer in test_data:
                self.assertEqual(LECalculator._LECalculator__is_first_minus_plus(arg), answer)
        except AssertionError as err:
            e = err
        self.__set_result(e=e)

    def test_008_is_single_number(self):
        """
        Testing a function that checks if a string
        is a single number or contains more than one number.
        """
        e = None
        test_data = [('7+2.5', False), ('-7', True), ('+2.036', True)]
        try:
            for arg, answer in test_data:
                self.assertEqual(LECalculator._LECalculator__is_single_number(arg), answer)
        except AssertionError as err:
            e = err
        self.__set_result(e=e)

    def test_009_instead_parentheses_result(self):
        """
        Testing a function that evaluates an expression inside parentheses.
        It is assumed that the function takes as input an expression in parentheses
        of the deepest level, which means that it does not contain other parentheses inside.
        """
        e = None
        test_data = [('7+2.5', '9.5'), ('-7-3/2', '-8.5'), ('5*3-6/0*1', '15-{ZeroDivisionError}*1')]
        try:
            for arg, answer in test_data:
                self.assertEqual(LECalculator._LECalculator__instead_parentheses_result(arg), answer)
        except AssertionError as err:
            e = err
        self.__set_result(e=e)

    def test_010_num_separated_operators(self):
        """
        Testing a function that separates operators and numbers and
        puts them in a list as separate arguments. The function must be able
        to distinguish between two adjacent signs, for example, to understand
        which of the adjacent minuses is an operator, and which one refers to a number.
        """
        e = None
        test_data = [('5*3-6/0*1', ['5', '*', '3', '-', '6', '/', '0', '*', '1']),
                     ('5+7.5*-2', ['5', '+', '7.5', '*', '-2'])]
        try:
            for arg, answer in test_data:
                self.assertEqual(LECalculator._LECalculator__num_separated_operators(arg), answer)
        except AssertionError as err:
            e = err
        self.__set_result(e=e)

    def test_011_operators_finder(self):
        """
        Testing a function that takes an expression divided into operators
        and numbers in the form of a list, as well as a pair of operators.
        The function traverses the list from left to right and executes each
        statement contained in the received pair only.
        """
        e = None
        test_data = [(('*', '/', ['5', '+', '7.5', '*', '-2']), ['5', '+', '-15.0']),
                     (('+', '-', ['5', '+', '-15.0']), ['-10.0'])]
        try:
            for arg, answer in test_data:
                self.assertEqual(LECalculator._LECalculator__operators_finder(*arg), answer)
        except AssertionError as err:
            e = err
        self.__set_result(e=e)

    def test_012_action(self):
        """
        Testing a function that takes two numbers and one operator,
        performing the action provided by the operator with the received numbers.
        Note - the function uses the Decimal module for calculations.
        """
        e = None
        test_data = [(('17', '9.5', '-'), '7.5'), (('7.5', '-2', '*'), '-15.0'),
                     (('6', '0', '/'), '{ZeroDivisionError}')]
        try:
            for arg, answer in test_data:
                self.assertEqual(LECalculator._LECalculator__action(*arg), answer)
        except AssertionError as err:
            e = err
        self.__set_result(e=e)

    def test_013_calculation(self):
        """
        Testing a function that takes an expression divided into operators
        and numbers as a list to be passed to the operators_finder function.
        All statements are expected to be executed and the result is a number in string format.
        """
        e = None
        test_data = [(['5', '+', '7.5', '*', '-2'], '-10.0'),
                     (['5', '*', '3', '-', '6', '/', '0', '*', '1'], '15-{ZeroDivisionError}*1')]
        try:
            for arg, answer in test_data:
                self.assertEqual(LECalculator._LECalculator__calculation(arg), answer)
        except AssertionError as err:
            e = err
        self.__set_result(e=e)

    def test_999999_report(self):
        """
        The function of writing test results to the database.
        It is important that it is executed last, after all the tests have been executed.
        """
        sql = """INSERT INTO test(test_name, test_is_successful, test_date, test_detail)
                     VALUES(%s, %s, %s, %s);"""
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            for name, params in self.__RESULT_DATA.items():
                cur.execute(sql, (name, *params))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f'BASE: {error}')
        finally:
            if conn is not None:
                conn.close()


if __name__ == "__main__":
    unittest.main()
