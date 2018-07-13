#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/12 下午6:46
# @Author  : cxy
# @Site    : 
# @File    : T.py
# @Software: PyCharm
# @desc    :
import time
from multiprocessing import Pool


def run(fn):
    # fn: 函数参数是数据列表的一个元素
    time.sleep(1)
    return fn * fn


if __name__ == "__main__":
    testFL = [1, 2, 3, 4, 5, 6]
    print('顺序执行:')  # 顺序执行(也就是串行执行，单进程)
    s = time.time()
    for fn in testFL:
        print(run(fn))

    e1 = time.time()
    print("顺序执行时间：", int(e1 - s))

    print('多进程执行:')  # 创建多个进程，并行执行
    pool = Pool(5)  # 创建拥有5个进程数量的进程池
    # testFL:要处理的数据列表，run：处理testFL列表中数据的函数
    rl = pool.map(run, testFL)
    # for fn in testFL:
    #     pool.apply_async(run, args=(fn, ))
    pool.close()  # 关闭进程池，不再接受新的进程
    pool.join()  # 主进程阻塞等待子进程的退出
    e2 = time.time()
    print(rl)
    print("并行执行时间：", int(e2 - e1))

