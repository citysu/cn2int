#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""阿拉伯数字、罗马数字、中文数字字符串 和 整数的相互转换.

Author: suhecheng
Home: https://github/citysu/cn2int
"""

__all__ = ["Cn2Int"]
__version__ = "0.1.0"


class Table:
    roman2int = {
        "I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000
    }
    int2roman =  [
        ["", "I", "II", "III", "IV", "V", "VI", "VII","VIII", "IX"],
        ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"],
        ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"],
        ["", "M", "MM", "MMM"]
    ]

    lower = "零一二三四五六七八九"
    lower_enumeration = "〇一二三四五六七八九"
    lower_uint = ["", "十", "百", "千"]
    lower_delimiter = ["", "万", "亿"]

    upper_enumeration = "零壹贰叁肆伍陆柒捌玖"
    upper = "零壹贰叁肆伍陆柒捌玖"
    upper_unit = ["", "拾", "佰", "仟"]
    upper_delimiter = ["", "萬", "億"]

    chinese2int = {
        "〇": 0,
        "一": 1,
        "二": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9,
        "十": 10,
        "百": 100,
        "千": 1000,
        "万": 10000,
        "亿": 100000000,
        "零": 0,
        "壹": 1,
        "贰": 2,
        "叁": 3,
        "肆": 4,
        "伍": 5,
        "陆": 6,
        "柒": 7,
        "捌": 8,
        "玖": 9,
        "拾": 10,
        "佰": 100,
        "仟": 1000,
        "萬": 10000,
        "億": 100000000,
        "两": 2,
    }


class Cn2Int:
    """中文数字和整数的相互转换

    进行 阿拉伯数字字符串和整数, 罗马数字字符串和整数, 中文数字字符串和整数的相互转换. 只支持
    正整数, 负整数和浮点数都是不支持的. 数字字符串默认字符串是正则提取出来的, 只包含"[0-9〇零
    一二两三四五六七八九十百千万亿壹贰叁肆伍陆柒捌玖拾佰仟萬億]+"中的字符.

    int2arab, int2roman, int2chinese,
        返回None, 表示输入的整数超过支持的转换范围.
    arab2int, roman2int, chinese2int,
        返回-1, 表示输入的数字字符串格式非法, 无法进行转换.
        返回-2, 表示输入的数字字符串对应的整数, 超出了支持的转换范围, 转换失败.
    """
    def __init__(self):
        pass

    def convert(self, s):
        """将数字字符串转化为整数
        
        参数:
            s (string): 数字字符串. 你必须自行确保它是: 阿拉伯数字字符串, 罗马数字字符串,
                或中文数字字符串中的一种. 出于效率考虑, 我们没有对如"12百4五"这样的数字
                字符串进行检测.
        """
        number = 0
        code = ord(s[0])
        # "0-9": [48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
        if code <= 57:
            number = self.arab2int(s)
        # "IVXLCDM": [73, 86, 88, 76, 67, 68, 77]
        elif code <= 88:
            number = self.roman2int(s)
        # "〇一二三四五六七八九十百千万亿零壹贰叁肆伍陆柒捌玖拾佰仟萬億":
        # [12295, 19968, 20108, 19977, 22235, 20116, 20845, 19971, 20843,
        #  20061, 21313, 30334, 21315, 19975, 20159, 38646, 22777, 36144,
        #  21441, 32902, 20237, 38470, 26578, 25420, 29590, 25342, 20336,
        #  20191, 33836, 20740]
        else:
            number = self.chinese2int(s)
        return number


    def arab2int(self, s):
        """将阿拉伯数字字符串转换为整数. 
        
        参数:
            s (string): 阿拉伯数字字符串. 例如: "12345"
        
        取值范围:
            没有范围限制.

        返回:
            int: 零, 或正整数. 如果返回-1, 那么`s`是一个非法的阿拉伯数字字符串.
        """
        if not s.isdigit():
            raise ValueError("invalid Chinese numerals")

        number = int(s)
        return number

    def roman2int(self, s):
        """将罗马数字字符串转换为整数.
        
        参数:
            s (string): 罗马数字字符串. 例如: "XII". 忽略大小写.
        
        取值范围:
            只能是1-4000内的整数. 包括1但不包含4000.

        返回:
            int: 正整数. 如果返回-1, 那么`s`是一个非法的罗马数字字符串.
        
        注意:
            得到整数后, 会再次转化为罗马数字字符串, 并和原来的数字字符串比较. 只有相等时,
            罗马数字字符串`s`才是合法的. 这是最轻松、效率的合法性检测手段了.
        """
        number = 0
        s_upper = s.upper()
        s_length = len(s)

        for i in range(s_length - 1):
            p = Table.roman2int[s_upper[i]]
            p_next = Table.roman2int[s_upper[i+1]]
            if p < p_next:
                number -= p
            else:
                number += p
        number += Table.roman2int[s_upper[s_length - 1]]

        if s != self.int2roman(number):
            raise ValueError("invalid Chinese numerals")

        return number

    def chinese2int(self, s):
        """将中文数字字符串转换为整数.

        参数:
            s (string): 中文数字字符串. 例如: "三百二十一". `int2chinese`返回的所有类型
                中文数字字符串都受到支持.

        取值范围:
            只能是0-1e12内的整数, 包括零但不包含一万亿(1e12).

        返回:
            int: 零, 或正整数. 如果返回负数, 那么`s`是一个非法的罗马数字字符串. 负数值代表了
                中文数字字符串中发生的格式错误类型. -1: 超出了数值的转换范围.
        """
        number = 0
        if len(s) >= 2:
            a, b = Table.chinese2int[s[0]], Table.chinese2int[s[1]]
            # 第一个字符不能是"百千万亿佰仟萬億"
            if a > 10:
                raise ValueError("invalid Chinese numerals")
            if max(a, b) <= 9:
                try:
                    number = self.chinese2int_enumeration(s)
                except ValueError:
                    # "零零零三百六十一"会被错误的判定为枚举表示. (s.lstrip("零〇")
                    # 不可行, e.g. "零三零百六十" => "三零百六十")
                    number = self.chinese2int_traditional(s)
            else:
                number = self.chinese2int_traditional(s)
        else:
            number = Table.chinese2int[s]
        return number


    def int2arab(self, number):
        """将整数转换为阿拉伯数字字符串.

        参数:
            number (int): 零, 或正整数.

        返回:
            string: 阿拉伯数字字符串. 如果返回None, 那么输入的`number`超出了支持的转换
                范围. 该范围为0-nan, 包括0.
        """
        if number < 0:
            return None

        s = str(number)
        return s
    
    def int2roman(self, number):
        """将整数转换为罗马数字字符串.

        参数:
            number (int): 正整数.
        
        返回:
            string: 罗马数字字符串. 如果返回None, 那么输入的`number`超出了支持的转换范围,
                该范围为0-4000, 包括1但不包含4000.
        """
        if number <= 0 or number >= 4000:
            return None
        
        n, s = number, ""
        i = 0

        while n > 0:
            p = n % 10
            n //= 10
            s = Table.int2roman[i][p] + s
            i += 1
        return s
    
    def int2chinese(self, number,
                    lower=True,
                    enumeration=False,
                    use_liang=False,
                    use_simple_ten=False,
                    use_simple_zero_tail=False):
        """将整数转换为中文数字字符串.
        
        参数:
            number (int): 零, 或正整数.
            lower (bool): 是否使用小写数字. 默认Ture.
            enumeration (bool): Ture: 使用枚举表示, 例如, 第一二三章. False: 使用传统
                表示, 例如, 第一百二十三章. 默认False.
            
            (以下参数只在enumeration=False时生效)

            use_liang (bool): True: 用"两"替换, 并尽可能多地替换中文数字字符串中的"二".
                False: 中文数字字符串中不使用"两". 例如, 当为True时, 2222被转换成
                "两千两百二十二", 而非"两千二百二十二". 默认False.
            use_simple_ten (bool): 得到以"一十"开头的的中文数字字符串时, 是否省略"一".
                True: 省略, False: 不省略. 默认False.
            use_simple_zero_tail (bool): 整数以 xx000, xx00, xx0结尾时, 中文数字
                字符串末尾的"十百千"可以省略. x是非零数字. True: 省略, False: 不省略.
                例如: "一万六千"可简写为"一万六", 但"一千零六十"不会简写成"一千零六".
                默认False.

        返回:
            string: 中文数字字符串. 如果返回None, 那么输入的`number`超出了支持的转换
                范围. 该范围为0-1e12, 包括0但不包括1e12(一万亿).
        """
        if number < 0 or number >= 1e12:
            return None

        n = number
        s = ""
        p = 0

        if enumeration:
            if lower:
                table = Table.lower_enumeration
            else:
                table = Table.upper_enumeration

            if n == 0:
                s = table[0]
            while n > 0:
                p = n % 10
                n //= 10
                s = table[p] + s
        else:
            if lower:
                table = Table.lower
                table_delimiter = Table.lower_delimiter
                table_unit = Table.lower_uint
            else:
                table = Table.upper
                table_delimiter = Table.upper_delimiter
                table_unit = Table.upper_unit

            i = 0
            if n == 0:
                s = table[0]
            while n > 0:
                p = n % 10000
                n //= 10000
                delimiter = table_delimiter[0] if p == 0 else table_delimiter[i]

                s_small = self.smallint2chinese(p, n, delimiter, table, table_unit, use_liang)
                s = s_small + delimiter + s
                s = self.int2chinese_fill_zero(s, p, n)

                i += 1

            if use_simple_ten:
                s = self.int2chinese_simple_ten(s, p)
            if use_simple_zero_tail:
                s = self.int2chinese_simple_zero_tail(s, lower)
        return s


    def smallint2chinese(self, number, previous, delimiter, table, table_unit, use_liang):
        n = number
        s = ""
        i = 0

        while n > 0:
            p = n % 10
            n //= 10
            if p == 0:
                if s != "" and s[0] != "零":
                    s = "零" + s
            else:
                if use_liang and ((p == 2 and i > 1) or (number == 2 and delimiter != "")):
                    s = "两" + table_unit[i] + s
                else:
                    s = table[p] + table_unit[i] + s
            i += 1
        return s

    def int2chinese_fill_zero(self, s, p, n):
        """补充零只能在s上进行, 使用s_small替代s, 会把'一亿零九千'中的零漏掉."""
        if n != 0:
            if p < 1000 and p != 0:
                s = "零" + s
            if s != "" and s[0] != "零" and p == 0:
                s = "零" + s
        return s

    def int2chinese_simple_ten(self, s, p):
        if p < 20 and p >= 10:
            s = s.lstrip("一壹")
        return s
    
    def int2chinese_simple_zero_tail(self, s, lower):
        if len(s) >= 3 and s[-3] != "零":
            s = s.rstrip("十百千拾佰仟")
        if s.endswith("两"):
            s = s[:-1] + "二" if lower else "贰"
        return s

    def chinese2int_enumeration(self, s):
        number = 0
        length = len(s)
        i = 0
        m = 1

        while length > 0:
            length -= 1
            p = Table.chinese2int[s[length]]

            # 枚举表示 下不能出现大于9的单个数字.
            if p > 9:
                raise ValueError("invalid Chinese numerals")

            number += p * m

            # 范围限制
            if i == 11 and len(s[:length].lstrip("零〇")) > 0:
                raise OverflowError("the value is out of the supported range")
            m *= 10
            i += 1

        return number

    def chinese2int_traditional(self, s):
        number = 0
        length = len(s)

        # 以"万亿萬億"作为分割符, 得到的每段中文数字子字符串为"X千X百X十X "的模式, 该子串对应
        # 的整数为small.
        small = 0

        # 中文数字子字符串按每两个字符进行分组"(X千)(X百)(X十)(X一)". 组内模式为(a, b),
        # a为数字(0-9), b为权值(一十百千).
        a, b = 0, 1

        # tiny是一个临时值, 当tiny = a * b时, 它始终比旧的small多一位数字. 该现象可确保
        # "千百十"出现的顺序正确.
        tiny = 0

        # 两个flag分辨对应a, b. 逆序遍历中文数字字符串时, b, a应交替出现. 用flag判断是否
        # 连续出现a或连续出现b. 连续的a或b, 意味着中文数字字符串格式非法. 例如"三百二二",
        # "三千百".
        flag_pair_a, flag_pair_b = False, False

        # 表示中文数字字符串中, 分隔符"亿万一"对应的整数.
        delimiter = 1

        # For use_simple_zero_tail=True. 计算出省略的单位.
        p = Table.chinese2int[s[length - 2]]
        if p > 10:
            a = Table.chinese2int[s[length - 1]]
            # 排除 "一百万", "二千亿"这种情况
            if a < 10:
                b = p // 10
                small += a * b
                length -= 1

        # 因为要检查中文数字字符串的格式合法性, 所以if判断较多, 略显复杂.
        while length > 0:
            length -= 1
            p = Table.chinese2int[s[length]]

            if p == 0:
                continue

            if p < 10:
                if flag_pair_a is False:
                    a = p
                    tiny = a * b
                    if tiny > small:
                        small += tiny
                    else:
                        # "千百十"顺序出错, e.g. 五百六千
                        raise ValueError("invalid Chinese numerals")
                    flag_pair_a = True
                else:
                    # 出现连续的a(数字).
                    raise ValueError("invalid Chinese numerals")
                flag_pair_b = False
            else:
                if p == 10000 or p == 100000000:
                    number += small * delimiter
                    small = 0
                    a, b = 0, 1

                    # 万万为亿. e,g 六万万.
                    if p == 10000 and Table.chinese2int[s[length - 1]] == 10000:
                        p = 100000000
                        length -= 1

                    # 新的delimiter始终大于旧的delimiter, 确保"亿"在"万"前.
                    if p > delimiter:
                        delimiter = p
                    else:
                        if delimiter == 100000000:
                            # e.g. 三万亿, 六亿亿, 六千万五亿
                            raise OverflowError("the value is out of the supported range")
                        # 此时必定: p=10000, delimiter=10000. 针对"四万五千万"的情形.
                        delimiter = 100000000                    
                else:
                    if flag_pair_b is False:
                        if p <= b:
                            # e.g 七千一千零一十万
                            raise ValueError("invalid Chinese numerals")
                        b = p
                        flag_pair_b = True
                    else:
                        # 出现连续的b(权值).
                        raise ValueError("invalid Chinese numerals")
                flag_pair_a = False

        # For use_simple_ten=True, "十"开头的中文数字字符串, 逆序遍历到开头的"十"
        # 后, 会终止循环, 导致"十"无法参与到small的计算中, 所以需要修正下.
        if p == 10:
            small += 10

        number += small * delimiter
        return number
