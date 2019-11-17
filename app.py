import os
import json

import redis
import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request


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

conn = psycopg2.connect(**opts['postgresql'], cursor_factory=RealDictCursor)
rconn = redis.Redis(**opts['redis'])
app = Flask(__name__)


@app.route('/v1/jobs', methods=['GET'])
def get_jobs():
    cursor = conn.cursor()
    sql = '''
        select id, args, status, created_at, updated_at
        from Jobs;
    '''
    cursor.execute(sql)
    jobs = cursor.fetchall()
    return {'jobs': jobs}


@app.route('/v1/jobs', methods=['POST'])
def create_job():
    job_args = request.get_json()
    job_args_json = json.dumps(job_args)
    cursor = conn.cursor()
    sql = '''
        insert into Jobs (args, status) values (%s, %s)
        returning id, args, status, created_at, updated_at;
    '''
    cursor.execute(sql, [job_args_json, 'queued'])
    conn.commit()
    new_job = cursor.fetchone()
    rconn.rpush('queue:jobs', json.dumps(new_job, default=str))
    return new_job
