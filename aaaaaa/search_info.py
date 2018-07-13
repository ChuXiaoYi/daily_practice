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
import csv
import types
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import urllib

from lxml import etree

from paramiko_client import ParamikoClient
from multiprocessing import Pool, Manager
import datetime


def find_log(query, *arg):
    qid = arg[0]
    queue = arg[1]
    ssh = ParamikoClient('ssh.ini', query)
    ssh.connect()
    command = str()
    if query == 'query':
        command = 'cd /search/service/nginx/html/order_pay_online/orderAPI; ' \
                  'grep -r "travco" | grep "ba005"'
        print('获取qid')
    if query == 'responseServer':
        command = 'cd /search/service/nginx/html/order_pay_online/orderAPI; ' \
                  'grep -r ' + str(qid) + ' | grep "ResponseServer"'
        print('获取responseServer')
    stdout = ssh.exec_commond(command)

    return [stdout.readlines(), query, queue]


def get_return_rule(resp):
    print('正在获取退改信息')
    # try:
    #     ret = urllib.parse.unquote(resp)
    #     canel = etree.fromstring(json.loads(ret)['response'])
    #     count = len(canel.xpath('.//StartDate'))
    #     can_po = ''
    #     for i in range(count):
    #         can_po += '申请退款开始时间:' + canel.xpath('.//StartDate')[
    #             i].text + '<br/>申请退款截止时间:' + \
    #                   canel.xpath('.//EndDate')[i].text + '<br/>退单费用:' + \
    #                   canel.xpath('.//Penalty')[i].text + 'USD<br/><br/>'
    #         pass
    # except Exception:
    #     can_po = "重要提示：请线下咨询客服！实际退改费用请以线下沟通结果为准"
    # if can_po == '':
    #     can_po = '请求退改失败，对方没有返回退改信息'
    # print(can_po)
    # return can_po
    try:
        resa = ET.fromstring(resp)
    except Exception as e:
        return ''
    title = '{http://www.travco.co.uk/trlink/xsd/hotelcancellationdetailv7/response}'
    canel = resa[0][0][0][0]
    time_z = time_f = time_a = time_b = time_c = time_d = time_e = time_g = time_h = time_i = time_j = time_k = None
    for i in canel.iter():
        if i.tag == title + 'CancellationCharge':
            time_z = i.attrib['LastDateToCancelWithoutCharge']
            time_f = i.attrib['Before']
        elif i.tag == title + 'FirstCancellationCharge':
            time_a = i.attrib['FirstCancellationChargeDate']
            time_b = i.attrib['After']
            time_c = i.attrib['NoOfNts']
            time_d = i.attrib['AtPercentage']
        elif i.tag == title + 'NextCancellationCharges':
            time_e = i.attrib['NextCancellationChargeDate']
            time_g = i.attrib['After']
            time_h = i.attrib['NoOfNts']
            time_i = i.attrib['AtPercentage']
            time_j = i.attrib['PlusNoOfNts']
            time_k = i.attrib['PlusPercentage']
    can_po = '当取消费用计算方式符合多条规则时，以最严格的一条为准<br />'
    if time_z and time_f:
        can_po += '{0} {1} 前免费取消 <br />'.format(time_z, time_f)
    if time_a and time_b and time_c and time_d:
        can_po += '{0} {1} 后取消,取消费用计算方式:{2}晚房费 x {3}% <br />'.format(time_a, time_b, time_c, time_d)
    if time_e and time_g and time_h and time_i and time_j and time_k:
        can_po += '{0} {1} 后取消, 取消费用计算方式:{2}晚房费 x {3}% + {4}晚房费 x {5}% <br />'. \
            format(time_e, time_g, time_h, time_i, time_j, time_k)
    return can_po


def call_back(arg):
    print('进入回调了')
    query = arg[1]
    lines = arg[0]
    if query == 'query':
        qid_queue = arg[2]
        for line in lines:
            search_qid = re.search(r'"qid": "(.*)", "dev"', line)
            qid = search_qid.group(1)
            qid_queue.put_nowait(int(qid))
            print('qid放到队列了')

    if query == 'responseServer':
        result_queue = arg[2]
        # for response_line in lines:
        try:
            resp = re.search(r'resp=(.*),cost', lines[0])
        except IndexError as e :
            pass
        else:
            response = resp.group(1)
            if resp:
                ret = urllib.parse.unquote(response)
                return_rule = get_return_rule(json.loads(ret)['response'])
                result_queue.put_nowait(return_rule)
            else:
                print('没有response')


if __name__ == '__main__':
    pool = Pool(4)
    qid_queue = Manager().Queue()
    # result_queue = Manager().Queue()
    pool.apply_async(find_log, args=('query', 0, qid_queue,), callback=call_back)
    print('有一个线程去找qid了')
    while isinstance(qid_queue.get(), int):
        pool.apply_async(find_log, args=('responseServer', qid_queue.get_nowait(), qid_queue,), callback=call_back)
    pool.close()
    pool.join()
    index = 1
    while qid_queue.qsize() > 0:
        if not isinstance(qid_queue.get_nowait(), int) and index < 30:
            csv_file = open('travco_return_rule.csv', 'a', encoding='utf8')
            writer = csv.writer(csv_file)
            writer.writerow([qid_queue.get()])
            csv_file.close()
            index += 1
