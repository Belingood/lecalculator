import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE result (
            result_id SERIAL PRIMARY KEY,
            result_date TIMESTAMP NOT NULL,
            result_is_successful BOOLEAN NOT NULL,
            result_expression VARCHAR(255) NOT NULL,
            result_answer VARCHAR(255)
        )
        """,
        """ CREATE TABLE test (
                test_id SERIAL PRIMARY KEY,
                test_name VARCHAR(100) NOT NULL,
                test_is_successful BOOLEAN NOT NULL,
                test_date TIMESTAMP NOT NULL,
                test_detail TEXT
                )
        """,
        )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
