#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Cn2Int测试"""

from random import sample, randint
import math

import cn2int as c2i


def test_roman2int():
    print("=== test_roman2int ===")

    r = 'IVXLCDM' * 3
    valid_romans = {c2i.int2roman(i): i for i in range(1, 4000)}
    invalid_romans = set(["".join(sample(r, randint(1, 21))) for i in range(4000)]) - valid_romans.keys()

    print("1. 所有受支持的罗马数字: (0, 4000).")
    for s, number in valid_romans.items():
        n = c2i.roman2int(s)
        assert number == n, "s=%s, number=%d, n=%d" % (s, number, n)
    print(">>> OK <<<")

    print("2. 非法格式的罗马数字: 随机%d个." % len(invalid_romans))
    for s in invalid_romans:
        try:
            n = c2i.roman2int(s)
            raise Exception("s=%s, n=%d" % (s, n))
        except:
            pass
    print(">>> OK <<<\n")


def test_chinese2int():
    print("=== test_chinese2int ===")
    dataset = {
        "大小混合": {
            "二千伍佰六十叁": 2563
        },
        "万万": {
            "六万": 60000,
            "六万万": 600000000,
            "六万万万": None,
            "六万万零万": 600000000,
            "六万万万万": None,
            "六亿三千万万": None,
            "四万五千万": 450000000,
            "四万万五千": 400005000,
            "四万万五千万": 450000000,
            "七千一千零一十万六千八百万": None,
            "七千一千零一十万": None,
        },
        "万亿, 亿亿": {
            "三十六万亿一十二亿": None,
            "三万亿": None,
            "六亿亿": None,
            "六千万五亿": None,
        },
        "零填充": {
            "零零零三百六十一": 361,
            "零零零": 0,
            "零三零百六十": 360,
            "零零零零零零零零零零零零零零零": 0,
            "零一零零零零零零零零零零零零零": None,
            "零零零零零一二三零零零零零零零": 1230000000,
        },
        "枚举表示范围": {
            "九二九八七六五四三二一〇": 929876543210,
            "一九二九八七六五四三二一〇": None,
            "负九二九八七六五四三二一〇": -929876543210,
            "负一九二九八七六五四三二一〇": None,
        },
        "传统表示范围": {
            "二千一百八十一亿二千三百四十五万六千七百八十九": 218123456789,
            "九万亿二千一百八十一亿二千三百四十五万六千七百八十九": None,
        },
        "正常数字": {
            "一千零一十": 1010,
        },
        "带正负号的枚举表示": {
            "负一二三": -123,
            "一二三": 123,
            "正一二三": 123,
            "正零": 0,
            "正〇": 0,
            "负零": 0,
            "负〇": 0,
            "零一二三": 123,
            "〇一二三": 123,
            "正零一二三": 123,
            "负零一二三": -123,
        },
        "传统表示中, 数字不能连续出现, 零除外": {
            "一二三四": 1234,
            "一千二百三四": None,
            "一千零四": 1004,
        },
        "十百千 需要从小到大出现(逆序)": {
            "一百一百一百": None,
            "三六亿六百八千二十": None,
        },
        "十百千 不能连续出现": {
            "一二百千": None,
            "一亿万七十二": 100000072,
            "五十三万千六百零一": None,
        },
        "二 => 两(-- 待处理 --)": {
            "两千零六十": 2060,
            # 虽然识别正确, 但这是一个非法格式, 目前cn2int无法检测到.
            # 参考: [二、两和俩、双](http://ling.cass.cn/ziyuan/ywtd/ywmt/202111/t20211129_5377741.html)
            "两千两百两十两": 2222, # None
        },
        "末尾 千百十省略, 万亿前的不省略": {
            "一百二": 120,
            "一千二": 1200,
            "一万二": 12000,
            "十二万": 120000,
            "一千二百二": 1220,
            "一千零二十": 1020,
            "一千零二": 1002,
            "一万零二百二": 10220,
            "一万零二百零二": 10202,
            "一万零二十": 10020,
            "三千二百万": 32000000,
            "三千二万": 30020000,
            "三千零二万": 30020000,
        },
        "一十 => 十": {
            "十": 10,
            "十五万": 150000,
            "二百一十": 210,
            "二百十": None,
            "一千零十": None,
            "一千零百": None,
        },
        "随机(伪)": {
            "一千三百五十二亿六千八百七十五万九千三百八十七": 135268759387,
            "一千三百五十二亿零五万九千三百八十七": 135200059387,
            "一千亿六千八百七十五万九千三百八十七": 100068759387,
            "一千三百五十二亿六千八百万零三百零七": 135268000307,
            "一千三百五十亿零九千三百八十七": 135000009387,
            "五万六千七百八十九": 56789,
            "一千": 1000,
            "一百": 100,
            "一十": 10,
            "一": 1,
            "零": 0,
            "一千零一": 1001,
            "一千零一十": 1010,
            "一千一百": 1100,
            "一百一十": 110,
            "一百零一": 101,
            "一十一": 11,
            "一千一百一十": 1110,
            "一千一百零一": 1101,
            "一千零一十一": 1011,
            "一百一十一": 111,
            "一百三十五亿二千六百八十七万五千九百三十八": 13526875938,
            "一百三十五亿二千万五千九百三十八": 13520005938,
            "一百亿零六百八十七万五千九百三十八": 10006875938,
            "一百三十五亿六千八百万零三百零七": 13568000307,
            "一百三十五亿零九百八十七": 13500000987,
            "五万六千七百八十九": 56789,
            "一百零二亿零三百零四万零五百零六": 10203040506,
            "二千零三十二亿": 203200000000,
            "四千四百零六亿五千七百零五万零四百五十": 440657050450,
            "二千二百二十二亿二千二百二十二万二千二百二十二": 222222222222,
            "五千四百三十二亿九千八百七十六万五千四百三十二": 543298765432,
            "一百二十": 120,
            "一千二百": 1200,
            "一万二千": 12000,
            "一十二万": 120000,
            "一十二万六千": 126000,
            "一十二万六千七百": 126700,
            "一十二万六千七百三十": 126730,
            "一十二万零三十": 120030,
            "一十二万零一十": 120010,
            "一十二万零三百": 120300,
            "二十": 20,
            "二": 2,
            "二十": 20,
            "二十二": 22,
            "二百": 200,
            "二百零二": 202,
            "二百二十": 220,
            "二百二十二": 222,
            "二千": 2000,
            "二千零二": 2002,
            "二千零二十": 2020,
            "二千零二十二": 2022,
            "二千二百": 2200,
            "二千二百零二": 2202,
            "二千二百二十": 2220,
            "二千二百二十二": 2222,
            "二万零二百二十二": 20222,
            "一": 1,
            "一十": 10,
            "一百": 100,
            "一千": 1000,
            "一万": 10000,
            "一十万": 100000,
            "一百万": 1000000,
            "一百万": 1000000,
            "一十一": 11,
            "一百一十": 110,
            "一千一百": 1100,
            "一万一千": 11000,
            "一十一万": 110000,
            "一百一十万": 1100000,
            "一百一十万": 1100000,
            "一亿二千三百四十五万六千七百八十九": 123456789,
            "一十二亿三千四百五十六万七千八百九十": 1234567890,
            "一十九亿八千七百六十五万四千三百二十": 1987654320,
            "二十九亿八千七百六十五万四千三百二十": 2987654320,
            "二十一亿二千三百四十五万六千七百八十九": 2123456789,
            "九十八亿七千六百五十四万三千二百一十": 9876543210,
            "一百九十八亿七千六百五十四万三千二百一十": 19876543210,
            "一百零八亿七千六百五十四万三千二百一十": 10876543210,
            "一千三百五十亿零九千三百八十七": 135000009387,
            "一百三十五亿零九百八十七": 13500000987,
            "二千零三十二亿": 203200000000,
            "一亿零九千": 100009000,
            "一十五亿九千三百万": 1593000000,
            "二万零九": 20009,
        },
    }

    for i, (info, cases) in enumerate(dataset.items()):
        print("%d. %s" % (i + 1, info))
        for s, number in cases.items():
            try:
                n = c2i.chinese2int(s)
            except (OverflowError, ValueError):
                n = None
            assert number == n, "%s => %s | %s" % (s, str(n), str(number))
    print(">>> OK <<<\n")


def test_chinese2float():
    print("=== test_chinese2float ===")
    dataset = {
        "正常数字": {
            "一千零三十点六六六": 1030.666,
            "正三十九": 39.0,
            "负零点九九九九": -0.9999,
            # 以下是正常现象, 很多数无法用浮点数精确表示.
            "一十二亿三千四百五十六万七千八百九十点九八七六五四三": 1234567890.9876542,
            "一十二亿三千四百五十六万七千八百九十点九八七六五四二": 1234567890.9876542,
            "负一十二亿三千四百五十六万七千八百九十点九八七六五四二": -1234567890.9876542,
        },
        "点开头": {
            "点九八七六": None,
            "负点一二": None,
            "正点六六六": None,
            "点": None,
            "点零": None,
            "零点": None,
            "零点零": 0.0,
        },
        "以万亿结尾的浮点数": {
            "三点六万": 36000,
            "三十六万": 360000,
            "一亿六千万": 160000000,
        }
    }

    for i, (info, cases) in enumerate(dataset.items()):
        print("%d. %s" % (i + 1, info))
        for s, number in cases.items():
            try:
                n = c2i.chinese2float(s)
            except (OverflowError, ValueError):
                n = None
            # math.isclose
            assert number == n , "%s => %s | %s" % (s, str(n), str(number))
    print(">>> OK <<<\n")


def test_convert2int():
    print("=== test_convert2int ===")
    dataset = {
        "正常数字": {
            "+123": 123,
            "XI": 11,
            "正九十九": 99,
            "正三十九": 39,
            "-987": -987
        },
    }

    for i, (info, cases) in enumerate(dataset.items()):
        print("%d. %s" % (i + 1, info))
        for s, number in cases.items():
            try:
                n = c2i.convert2int(s)
            except (OverflowError, ValueError):
                n = None
            assert number == n , "%s => %s | %s" % (s, str(n), str(number))
    print(">>> OK <<<\n")


if __name__ == "__main__":
    test_roman2int()
    test_chinese2int()
    test_chinese2float()
    test_convert2int()
