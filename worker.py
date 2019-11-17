import os
import json
import logging

import redis
import dotenv
import psycopg2
from psycopg2.extras import DictCursor

import actions


def get_job(rconn):
    if os.path.exists('job_config.json'):
        logging.info('reading from job_config.json')
        job_file = open('job_config.json').read()
        return json.loads(job_file)
    job = rconn.blpop(['queue:jobs'], 60)
    if not job:
        return None
    return json.loads(job[1])


def set_job_status(conn, job_id, status):
    cursor = conn.cursor()
    sql = '''
        update jobs
        set status = %s
        where id = %s;
    '''
    cursor.execute(sql, [status, job_id])
    conn.commit()


def main(opts):
    conn = psycopg2.connect(**opts['postgresql'], cursor_factory=DictCursor)
    rconn = redis.Redis(**opts['redis'])
    logging.info('checking for jobs')
    job = get_job(rconn)
    if not job:
        logging.info('no job to process')
        return
    job_id = job['id']
    job_args = job['args']
    job_file = open('job_config.json', 'w')
    json.dump(job, job_file, default=str)
    set_job_status(conn, job_id, 'processing')
    logging.info(f'processing job: {job_id}')
    try:
        action = actions.make_action(job_args)
        result = action.perform()
        logging.info(f'action result: {result}')
        set_job_status(conn, job_id, 'complete')
        logging.info('job is complete')
    except Exception as e:
        logging.error(f'action failed: {e}')
        set_job_status(conn, job_id, 'failed')
    finally:
        conn.close()
        rconn.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    dotenv.load_dotenv()
    opts = {
        'postgresql': {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME')
        },
        'redis': {
            'host': os.getenv('REDIS_HOST'),
            'port': os.getenv('REDIS_PORT'),
            'password': os.getenv('REDIS_PASSWORD'),
        }
    }
    main(opts)
