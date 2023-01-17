#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Cn2Int的正确性测试"""
from cn2int import Cn2Int
from random import sample, randint


def test_int2arab():
    print("=== test_int2arab ===")
    print("we use the python build-in function to convert integer to ")
    print("to Arabic numerals, we don't need to test `int2arab`")
    print()


def test_arab2int():
    print("=== test_arab2int ===")
    print("we use the python build-in function to convert Arabic numerals")
    print("to integer, we don't need to test `arab2int`")
    print()


def test_int2roman():
    print("=== test_int2roman ===")
    c2i = Cn2Int()

    print("1. test all supported integers.")
    for number in range(1, 4000):
        s = c2i.int2roman(number)
        assert s is not None, "s=%s, number=%d" % (s, number)
    
    print("2. test some invalid integers which are out of the supported range.")
    for i in range(1000):
        number = randint(-5000, 0)
        s = c2i.int2roman(number)
        assert s is None, "s=%s, number=%d" % (s, number)

    for i in range(1000):
        number = randint(4000, 8000)
        s = c2i.int2roman(number)
        assert s is None, "s=%s, number=%d" % (s, number)
    print("2000 invalid integers have been tested")
    print()


def test_roman2int():
    print("=== test_roman2int ===")
    r = 'IVXLCDM'
    c2i = Cn2Int()

    print("1. test all valid Roman numerals. They are genarated by `int2roman`.")
    for number in range(1, 4000):
        s = c2i.int2roman(number)
        n = c2i.roman2int(s)
        assert number == n, "s=%s, number=%d, n=%d" % (s, number, n)

    print("2. test some invalid Roman numerals.")
    valid_romans = {c2i.int2roman(i): i for i in range(1, 4000)}
    count = 0
    invalid_count = 0
    for i in range(10000):
        s = "".join(sample(r * 3, randint(1, 21)))
        if valid_romans.get(s):
            continue
        try:
            n = c2i.roman2int(s)
        except:
            invalid_count += 1
        count += 1
    assert count == invalid_count, "some invalid roman numerals are missed."
    print("%d invalid Roman numerals have been tested. some of them may\n"
         "be duplicated" % count)
    print()


def test_int2chinese(debug=True):
    print("=== test_int2chinese ===")
    c2i = Cn2Int()

    print("1. we don't test enumeration representation, we ensure our conversion\n"
          "must be correct.")
    if debug:
        print("--- Debug Start ---")
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 19, 20, 30, 90,
                   500, 10000, 20304, 9876543210]
        for number in numbers:
            s_lower = c2i.int2chinese(number, lower=True, enumeration=True)
            s_traditional = c2i.int2chinese(number, lower=False, enumeration=True)
            print(number, s_lower, s_traditional)
        print("--- Debug End ---")

    print("2. when enumeration=False, we only need to test the lower=True\n"
          "case. Because lower=True/False use the same processing")
    if debug:
        print("--- Debug Start ---")
        integers = [
            [135268759387, 135200059387, 100068759387, 135268000307, 135000009387, 56789],
            [1000, 100, 10, 1, 0, 1001, 1010, 1100, 110, 101, 11, 1110, 1101, 1011, 111],
            [13526875938, 13520005938, 10006875938, 13568000307, 13500000987, 56789,
             10203040506, 203200000000, 440657050450, 222222222222, 543298765432],
            [120, 1200, 12000, 120000, 126000, 126700, 126730, 120030, 120010, 120300, 20],
            [2, 20, 22, 200, 202, 220, 222, 2000, 2002, 2020, 2022, 2200,
             2202, 2220, 2222, 20222],
            [1, 10, 100, 1000, 10000, 100000, 1000000, 1000000, 
             11, 110, 1100, 11000, 110000, 1100000, 1100000],
            [123456789, 1234567890, 1987654320, 2987654320, 2123456789, 9876543210,
             19876543210, 10876543210],
            [135000009387, 13500000987, 203200000000, 100009000, 1593000000, 20009]
        ]
        for numbers in integers:
            for number in numbers:
                s = c2i.int2chinese(number, lower=True,
                                    enumeration=False,
                                    use_liang=False,
                                    use_simple_ten=False,
                                    use_simple_zero_tail=False)
                print(number, s)
            print("+++++++++++++++++")
        print("--- Debug End ---")
    print("")


def test_chinese2int(debug=True):
    print("=== test_chinese2int ===")
    print("skipped")
    c2i = Cn2Int()

    if debug:
        print("--- Debug Start ---")
        number_strings = [
            ["一千零一十"],
            # 大小混合
            ["二千伍佰六十叁"],
            # 万万
            ["六万", "六万万", "六万万万", "六万万零万", "六万万万万", "六亿三千万万",
             "四万五千万", "四万万五千", "四万万五千万", "七千一千零一十万六千八百万",
             "七千一千零一十万"],
            # 万亿, 亿亿.
            ["三十六万亿一十二亿", "三万亿", "六亿亿", "六千万五亿"],
            # 零
            ["零零零三百六十一", "零零零", "零三零百六十",
             "零零零零零零零零零零零零零零零", "零一零零零零零零零零零零零零零",
             "零零零零零一二三零零零零零零零"],
            # enum range
            ["一九二九八七六五四三二一〇"]
        ]
        for strings in number_strings:
            for s in strings:
                try:
                    n = c2i.chinese2int(s)
                    print(s, n)
                except:
                    print(s, "---failed---")
            print("+++++++++++++++++")
        print("--- Debug End ---")


if __name__ == "__main__":
    test_arab2int()
    test_int2arab()
    test_int2roman()
    test_roman2int()
    test_int2chinese(False)
    test_chinese2int(False)
