#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from timeit import default_timer

import cn2int as c2i


def test_performance_int2chinese():
    print("=== performance: int2chinese ===")
    last = default_timer()

    number = 218123456789

    for i in range(int(2e5)):
        s = c2i.int2chinese(number,
                            lower=True,
                            enumeration=False,
                            use_liang=False,
                            use_simple_ten=False,
                            use_simple_zero_tail=False, width=30)
        if i % 10000 == 0:
            print("\b" * 100, "[%8.4f s](%8d):" % (default_timer() - last, i), flush=True, end="")
    total_time_int2chinese = default_timer() - last
    print("\b" * 100, "[%8.4f s](%8d):" % (total_time_int2chinese, i), flush=True)
    print("--->", int(2e5 / total_time_int2chinese / 1e3), "k/s")


def test_template(func, s):
    print("=== performance: %s ===" % func.__name__)
    last = default_timer()

    for i in range(int(2e5)):
        n = func(s)
        if i % 10000 == 0:
            print("\b" * 100, "[%8.4f s](%8d):" % (default_timer() - last, i), flush=True, end="")
    total_time = default_timer() - last
    print("\b" * 100, "[%8.4f s](%8d):" % (total_time, i), flush=True)
    print("--->", int(2e5 / total_time / 1e3), "k/s")


def test_performance_chinese2int():
    func = c2i.chinese2int
    s = "二千一百八十一亿二千三百四十五万六千七百八十九"
    test_template(func, s)


def test_performance_chinese2float():
    func = c2i.chinese2float
    s = "四千五百六十七万八千九百八十二点七六五四三二一"
    test_template(func, s)


if __name__ == "__main__":
    test_performance_int2chinese()
    test_performance_chinese2int()
    test_performance_chinese2float()
