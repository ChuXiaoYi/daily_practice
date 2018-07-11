#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/9 下午2:42
# @Author  : cxy
# @Site    :
# @File    : search_info.py
# @Software: PyCharm
# @desc    :
import re
import json
import urllib
from .paramiko_client import ParamikoClient
from multiprocessing import Pool, Manager
import datetime


def find_log(query, qid, q):
    ssh = ParamikoClient('ssh.ini', query)
    ssh.connect()
    command = str()
    if query == 'query':
        command = 'cd /search/service/nginx/html/order_pay_online/orderAPI;' \
                  'grep -r ' + qid + ' | grep "传入参数"'
    if query == 'responseServer':
        command = 'cd /search/service/nginx/html/order_pay_online/orderAPI; ' \
                  'grep -r ' + qid + ' | grep "ResponseServer"'
    stdout = ssh.exec_commond(command)

    return [stdout.readlines(), query, q]


def call_back(arg):
    query = arg[1]
    stdout = arg[0]
    queue = arg[2]
    result = dict()
    if query == 'query':
        line = stdout[0]
        search_query = re.search(r'"query": (.*), "net"', line)
        search_type = re.search(r'"type": "(.*)", "next_id"', line)
        query = search_query.group(1)
        type = search_type.group(1)
        result = {
            'query': query,
            'type': type
        }
    #
    if query == 'responseServer':
        response_result = list()
        for response_line in stdout:
            resp = re.search(r'resp=(.*),cost', response_line)
            if resp:
                response_result.append(resp.group(1))

        json_res_list = list()
        for res in set(response_result):
            json_res = json.loads(urllib.parse.unquote(res))
            json_res_list.append(json_res)
        result = {
            'response': json_res_list
        }
    queue.put(result)


def main(qid):
    q = Manager().Queue()
    pool = Pool()
    # qid = '1516069578765'
    start_time = datetime.datetime.now()
    for arg in ['query', 'responseServer']:
        pool.apply_async(find_log, args=(arg, qid, q,), callback=call_back)
    pool.close()
    pool.join()

    for i in range(q.qsize()):
        result = q.get()
        yield result
    finish_time = datetime.datetime.now()
    time = (finish_time - start_time)
    print(time)


if __name__ == '__main__':
    results = main()
    for result in results:
        print(result)
