import os
import logging

import dotenv
import psycopg2
from psycopg2.extras import DictCursor

import actions


def get_job(conn):
    try:
        cursor = conn.cursor()
        select_sql = '''
            update jobs set processing = true
            where id = (
              select id
              from jobs
              where
                processing is not true and
                complete is not true
              order by id
              for update skip locked
              limit 1
            )
            returning id, args;
        '''
        cursor.execute(select_sql)
        conn.commit()
        job = cursor.fetchone()
        return job
    except Exception as e:
        logging.exception(e)


def set_job_to_complete(conn, job_id):
    try:
        cursor = conn.cursor()
        sql = '''
            update jobs
            set
              processing = false,
              complete = true
            where id = %s;
        '''
        cursor.execute(sql, [job_id])
        conn.commit()
    except Exception as e:
        logging.exception(e)


def main(opts):
    conn = psycopg2.connect(**opts, cursor_factory=DictCursor)
    job = get_job(conn)
    if not job:
        print('no jobs')
        return
    action = actions.make_action(job['args'])
    result = action.perform()
    print('action result', result)
    set_job_to_complete(conn, job['id'])
    print('action is complete')
    conn.close()


if __name__ == '__main__':
    dotenv.load_dotenv()
    opts = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
    main(opts)
