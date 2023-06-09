# cn2int: Chinese Numerals To Int/Float

## 简介

- 中文数字和整数/浮点数的相互转换.
- 罗马数字和正整数的相互转换.

## 使用

中文数字 <==> 整数/浮点数

```python
import cn2int as c2i

# 中文数字 => 整数
c2i.chinese2int("二十三亿零六百三十万零七十八")

# 中文数字 => 浮点数
c2i.chinese2float("二千三百零六万三千点七八")


# 整数 => 中文数字
c2i.int2chinese(2306300078)

# 浮点数 => 中文数字
c2i.float2chinese(23063000.78)
```

罗马数字 <==> 整数

```python
# 罗马数字 => 整数
c2i.roman2int("XVI")

# 整数 => 罗马数字
c2i.int2roman(16)
```

自动识别阿拉伯数字、罗马数字、中文数字, 并转换成整数.

```python
# 不支持2亿600万这样的混合表示.
c2i.convert2int("两亿零六千五")
```

## 转换范围

- 罗马数字 <==> 整数: 4000以下的正整数.
- 中文数字 <==> 整数: (-1e12, 1e12)区间内的整数.
- 中文数字 <==> 浮点数: (-1e12, 1e12)区间内的浮点数.

## 转换失败.

整数/浮点数 => 数字字符串:

- 只有在超出转换范围时, 才会转换失败, 会返回`None`.

数字字符串 => 整数/浮点数:

- 数字字符串的格式非法, 转换中止. 会抛出`ValueError`.
- 数字字符串超出转换范围, 转换中止. 会抛出`OverflowError`.

## 数字字符串的模式

数字字符串需要至少符合以下正则表达式

- `roman2int`: "[IVXLCDM]+"
- `chinese2int`: "[正负負]?[〇一二三四五六七八九十百千万亿零壹贰叁肆伍陆柒捌玖拾佰仟萬億两]+"
- `chinese2float`: "[正负負]?[〇一二三四五六七八九十百千万亿零壹贰叁肆伍陆柒捌玖拾佰仟萬億两点點]+"

不符合的会抛出`KeyError`

cn2int**只做数字转换**, 不会去考虑数字字符串所处的语义环境.例如: 

- "人生不如意事十之八九，可说与人无一二", "一穷二白"
- "五六个石头七八斤"
- "正一教"
- "几点了? 六点十五了"

这些中文数字转换成整数/浮点数可能并不合适.

## 中文数字格式

中文数字(整数) 使用两种方式表示.

- 传统表示. 例如: 第一百二十三章.
- 枚举表示. 例如: 第一二三章.

中文数字(浮点数) 使用一种方式进行表示.

- 整数部分, 使用传统表示或枚举表示.
- 小数部分, 使用枚举表示

中文数字(整数 | 枚举表示): 支持以下合法格式组合.

- 大写、小写或大小写混合
- 正数、负数
- 零填充, 如: 零一二三.
- 除去正负号和左侧填充的零, 有效数字最多12位.

中文数字(整数 | 传统表示): 支持以下合法格式组合.

- 大写、小写或大小写混合
- 正数、负数
- 零填充, 如: 零一百二十三.
- "两"替换"二"
- "一十..."简写为"十..."
- "万万"替换"亿". 有两种表达方式: "四万五千万"或"四万万五千万"
- 末尾"千百十"省略. 如: 一万二.
- 有多余的"零", 如: 一千零零零零零零六(1006), 一千六万(10060000), 一千六(1600), 一千零六(1006)

注: 六万万"是合法的, "六万万零万"会被解释成"六亿零万" => "六亿", 也是合法的. "六万万万"会被
解释为"六万亿", 会被判定为超出转换范围.

中文数字(浮点数): 支持的合法格式为 中文数字(整数 | 枚举表示)和中文数字(整数 | 传统表示)的合法
格式组合.

中文数字(整数 | 枚举表示): 可检测以下非法格式.

- 出现大于9的数字.

中文数字(整数 | 传统表示): 可检测以下非法格式.

- 出现连续的数字. 如: "一百六六".
- 出现连续的"十百千". 如: "一百十"
- 跳过数字, "十百千"中的小数在大数前. 如"一百一百".
- "百千万亿"开头. 如: "亿六十"
- "十百千"是"万亿"后紧跟着的字符. 如: "一万千零六"

中文数字(整数 | 传统表示): 可检测以下超出转换范围的合法格式.

- "万亿", "亿亿"组成的量级. 会被判定为超出转换范围. 如: "六万亿"
- "万"在"亿"前, 如: “四千五百万零六十亿”

中文数字(浮点数): 可检测以下非法格式.

- 中文数字(整数)的非法格式
- 出现两个、或两个以上的"点"
- 除去正负号和左侧填充的零, 以"点"开头. 或以"点"结尾.

注: 以"万", "亿"结尾的浮点数是合法的. 如: 三点六万.
