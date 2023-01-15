#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from timeit import default_timer

from cn2int import Cn2Int


def test_performance_int2chinese():
    print("=== performance: int2chinese ===")
    last = default_timer()
    c2i = Cn2Int()

    number = 218123456789

    for i in range(int(2e6)):
        s = c2i.int2chinese(number,
                            lower=True,
                            enumeration=False,
                            use_liang=False,
                            use_simple_ten=False,
                            use_simple_zero_tail=False)
        if i % 10000 == 0:
            print("\b" * 100, "[%8.4f s](%8d):" % (default_timer() - last, i), flush=True, end="")
    total_time_int2chinese = default_timer() - last
    print("\b" * 100, "[%8.4f s](%8d):" % (total_time_int2chinese, i), flush=True)
    print("--->", int(2e6 / total_time_int2chinese / 1e3), "k/s")


def test_performance_chinese():
    print("=== performance: chinese2int ===")
    last = default_timer()
    c2i = Cn2Int()

    s = "二千一百八十一亿二千三百四十五万六千七百八十九"

    for i in range(int(2e6)):
        n = c2i.chinese2int(s)
        if i % 10000 == 0:
            print("\b" * 100, "[%8.4f s](%8d):" % (default_timer() - last, i), flush=True, end="")
    total_time_chinese2int = default_timer() - last
    print("\b" * 100, "[%8.4f s](%8d):" % (total_time_chinese2int, i), flush=True)
    print("--->", int(2e6 / total_time_chinese2int / 1e3), "k/s")


if __name__ == "__main__":
    test_performance_int2chinese()
    test_performance_chinese()
