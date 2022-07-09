from fastapi import FastAPI, HTTPException
from datetime import datetime
import psycopg2

from lecalculator import LECalculator
from config import config


app = FastAPI()


@app.get('/calculator/{expression:path}')
def calculator(expression: str):

    err_mes = ''
    s_code = 0

    if not LECalculator.data_checker(expression):
        err_mes = "Please check the sent data. The expression must contain only .()/*-+0123456789"
        s_code = 404

    res = LECalculator.calculator(expression)

    if '{ZeroDivisionError}' in res:
        err_mes = f"ZeroDivisionError: {expression} --> {res}"
        s_code = 404

    set_result(str(datetime.now()), not err_mes, expression, (err_mes, res)[not err_mes])

    if s_code == 404:
        raise HTTPException(status_code=s_code, detail=err_mes)

    return {"result": res}


def set_result(date, is_success, exp, answer):
    sql = """INSERT INTO result(result_date, result_is_successful, result_expression, result_answer)
                         VALUES(%s, %s, %s, %s);"""
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (date, is_success, exp, answer))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'BASE: {error}')
    finally:
        if conn is not None:
            conn.close()
