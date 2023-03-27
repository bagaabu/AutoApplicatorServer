# -*- coding:utf-8 -*-
# !/usr/bin/env Python

import json
import os
import sys
import queue
import time
import logging
import logging.handlers
import traceback

import numpy as np

from flask import request, jsonify
from threading import Thread

lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)

from log import get_logger
from app.Reporter import dbReporter, stage_dict
from app.utils import rerange_search2db, rerange_up2db, send_request
from app.Writer import writer

logger = get_logger(filename='main')


class ProcessThread(Thread):
    def __init__(self, requestID, user_data):
        super(ProcessThread, self).__init__(name=thread_name)
        Recoder = dbReporter()
        Recoder.setup_db('NX-database', 'Articles', 1)
        self.requestID = requestID
        self.name = '{}-{}'.format(requestID, user_data['userID'])
        self.writer = writer(Recoder, requestID, user_data)

    def run(self):
        logger.info("thread:{} is running ......".format(self.name, self.requestID))
        self.writer.get_save_article()
        logger.info("thread:{}'s request haas finished ......".format(self.name, self.requestID))


def application():
    logger.info('get a paper request!')
    resOut = {"status": 0, 'result': {'flag': False, 'records': []}, 'msg': ''}
    try:
        if request.method == 'POST':
            data = str(request.get_data(), encoding="utf8")
            j_data = json.loads(data)
            requestID = j_data['requestID']

            new_thread = ProcessThread(requestID, j_data['data'])
            new_thread.start()

            resOut['msg'] = 'request {} has been received!'.format(requestID)

            return jsonify(resOut)

        elif request.method == 'GET':
            user_data = request.args.get('data')
            requestID = request.args.get('requestID')
            Recoder = dbReporter()
            Recoder.setup_db('NX-database', 'Articles', 1)
            librarian = writer(Recoder, requestID, user_data)
            search_result = librarian.get_article_records
            resOut['result']['records'] = search_result
            resOut['result']['flag'] = True
            return jsonify(resOut)

    except Exception as e:
        resOut['status'] = 1
        exstr = traceback.format_exc()
        resOut['msg'] = exstr
        logging.error(exstr)
        return jsonify(resOut)


def collect_info():
    logger.info('get a request!')
    try:
        resOut = {"status": 0, 'result': {'flag': False, 'infos': None}, 'msg': ''}

        Recoder = dbReporter()
        Recoder.setup_db('NX-database', 'personal-info', 1)

        if request.method == 'POST':
            data = str(request.get_data(), encoding="utf8")
            j_data = json.loads(data)
            userID = j_data['data']['userID']
            logger.info('get request:{}'.format(j_data['request_id']))
            upload_list = rerange_up2db(j_data['data'])

            for table_name, up_data in upload_list.items():
                Recoder.change_db('NX-database', table_name, 1)
                _ = Recoder.log(up_data)

            resOut['result']['flag'] = True
            resOut['msg'] = "user: {}'s info has been recoded".format(userID)
            return resOut

        elif request.method == 'GET':

            infos = {}
            flags = {}

            userID = request.args.get('userID')
            stages = request.args.get('phase')
            keys = request.args.get('keys')
            seach_dict = rerange_search2db(stages, keys)

            for table_name, condition in seach_dict.items():
                Recoder.change_db('NX-database', table_name, 1)
                flag, content = Recoder.search(userID, condition)
                flags[table_name] = flag
                infos[table_name] = content

            resOut['result']['flag'] = flags
            resOut['result']['infos'] = infos

        return jsonify(resOut)

    except Exception as e:
        resOut['status'] = 1
        exstr = traceback.format_exc()
        resOut['msg'] = exstr
        logging.error(exstr)
        return jsonify(resOut)


if __name__ == '__main__':
    pass
