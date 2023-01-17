from cn2int import Cn2Int, Table
import re

from timeit import default_timer


re_dot = re.compile(r"[点點]")
c2i = Cn2Int()
levels = [10**i for i in range(12)]


def chinese2float(s):
    """将中文数字字符串转换为浮点数"""
    number = 0
    tail = 1

    # "六点三万人", "五点八亿斤"
    p = Table.chinese2int.get(s[-1])
    if p and p > 1000:
        tail = p
        s = s[:-1]

    parts = re_dot.split(s)
    count = len(parts)

    if count == 1:
        number = c2i.chinese2int(parts[0])
    elif count == 2:
        a_length = len(parts[0])
        b_length = len(parts[1])
        # 整数部分
        if a_length == 0:
            a = 0
        else:
            a = c2i.chinese2int_traditional(parts[0])
        # 小数部分
        if b_length == 0:
            b = 0
        else:
            b = c2i.chinese2int_enumeration(parts[1])
        number = a + b / levels[b_length]
        number *= tail
    else:
        raise ValueError("invalid Chinese numerals")
    return number


def chinese2number(s):
    if s.startswith("负") or s.startswith("負"):
        signed = -1
        s = s[1:]
    else:
        signed = 1
    n = chinese2float(s)
    number = signed * n
    return number


def test():
    print("\n=== test: chinese2float ===")
    s = "四千五百六十七万八千九百八十二点七六五四三二一"
    print("%s => %s" % (s, chinese2float(s)))


def test_performance_chinese2float():
    print("\n=== performance: chinese2float ===")
    last = default_timer()

    # s = "二千一百八十一亿二千三百四十五万六千七百八十九"
    s = "四千五百六十七万八千九百八十二点七六五四三二一"

    for i in range(int(2e5)):
        try:
            n = chinese2float(s)
        except:
            pass
        if i % 10000 == 0:
            print("\b" * 100, "[%8.4f s](%8d):" % (default_timer() - last, i), flush=True, end="")
    total_time_chinese2float = default_timer() - last
    print("\b" * 100, "[%8.4f s](%8d):" % (total_time_chinese2float, i), flush=True)
    print("--->", int(2e5 / total_time_chinese2float / 1e3), "k/s")


def example():
    print("\n=== example: chinese2float ===")
    sentence = "他又买了五万三千六百五十八点零四九三万斤的干草, 他要做什么? 我记得他已经有六点三四万斤的干草了"
    pattern = "[〇零一二两三四五六七八九十百千万亿壹贰叁肆伍陆柒捌玖拾佰仟萬億点點]+(?=万斤)"
    print("替换前: ", sentence)
    m = re.findall(pattern, sentence)
    for s in m:
        try:
            sentence = sentence.replace(s, str(chinese2float(s)))
        except:
            pass
    print("替换后: ", sentence)

    print()
    sentence = "他背负五千六百点九三万元的债务, 他准备跑路了"
    pattern = "[负負]?[〇零一二两三四五六七八九十百千万亿壹贰叁肆伍陆柒捌玖拾佰仟萬億点點]+(?=元)"
    print("替换前: ", sentence)
    m = re.findall(pattern, sentence)
    for s in m:
        try:
            sentence = sentence.replace(s, str(chinese2number(s)))
        except:
            pass
    print("替换后: ", sentence)



if __name__ == "__main__":
    example()
    test()
    test_performance_chinese2float()
