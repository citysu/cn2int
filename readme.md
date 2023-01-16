# cn2int

中文数字字符串和非负整数的相互转换.

## 简介

可以进行如下转换

- 阿拉伯数字字符串和非负整数的相互转换
- 罗马数字字符串和非负整数的相互转换
- 中文数字字符串和非负整数的相互转换

## 使用

### 正常使用

```python
from cn2int import Cn2Int
c2i = Cn2Int()

# 该方法会自动识别出数字字符串的类型, 并转换成整数.
c2i.convert("两亿零六千五")

# 阿拉伯数字字符串 => 整数
c2i.arab2int("12345")

# 罗马数字字符串 => 整数
c2i.roman2int("XVI")

# 中文数字字符串 => 整数
c2i.chinese2int("二十三亿零六百三十万零七十八")

# 整数 => 阿拉伯数字字符串
c2i.int2arab(12345)

# 整数 => 罗马数字字符串
c2i.int2roman(16)

# 整数 => 中文数字字符串
c2i.int2chinese(2306300078)
```

### 转换范围. 

- 阿拉伯数字字符串 => 整数: 零， 和正整数.
- 罗马数字字符串 => 整数: 4000以下的正整数.
- 中文数字字符串 => 整数: 零, 和一万亿以下的正整数.
- 整数 => 阿拉伯数字字符串: 零， 和正整数.
- 整数 => 罗马数字字符串: 4000以下的正整数.
- 整数 => 中文数字字符串: 零, 和一万亿以下的正整数.

### 转换失败.

整数 => 数字字符串: 只有在超出转换范围时, 才会转换失败, 会返回`None`.

数字字符串 => 整数: 有两种转换失败的情况:

- 数字字符串的格式非法, 无法进行转换. 会返回`-1`.
- 数字字符串超出转换范围, 转换中止. 会返回`-2`.

### 数字字符串的**格式要求**.

我们默认要转换成整数的数字字符串都是通过正则表达式提取出来的. 三个转换函数对应的通用pattern如下:

- `arab2int`: "[0-9]+"
- `roman2int`: "[IVXLCDM]+"
- `chinese2int`: "[〇零一二两三四五六七八九十百千万亿壹贰叁肆伍陆柒捌玖拾佰仟萬億]+"

当使用`convert`函数时, 请自行确保数字字符串符合某个通用pattern. 因为该函数无法识别出
"12万零6千"这样的数字字符串. 而且我们也不支持转换这样的数字字符串, 强行转换会抛出`ERROR`.

阿拉伯数字字符串没有特殊要求.

罗马数字字符串的构造有一定的规则, 具体可参考[罗马数字的构造规则](https://zhuanlan.zhihu.com/p/32305410).
所以通过以上通用pattern提取的数字字符串不一定是合法的罗马数字. 但`roman2int`可以检测出
其非法性. 例如: "XIIII"的格式是非法的, `roman2int`会返回`-1`.

中文数字字符串的构造也有一定的规则. 通过以上通用pattern提取的数字字符串不一定是合法的中文数字.
`chinese2int`可以检测出大部分的非法格式. 例如: "一百三千万", "一千百万", "百六十"等都是
非法的, `chinese2int`会返回`-1`.

另外一小部分非法格式`chinese2int`无法检测出来. 但`chinese2int`的实现仍能得到正确的结果,
这是`chinese2int`自带的纠正能力. 例如以下数字字符串的格式是非法的: "二十三亿万七十八",
"二十三亿零零零六百三十万零零零零七十零八", 但结果正确.

"亿万"可以组成新的量级, 导致`chinese2int`对 "六千万五亿", "两万亿", "三亿亿" 类型的数字
字符串无法转换, 会判定为超出转换范围, 返回`-2`.

"万万为亿", `chinese2int`可以正确转换"六万万" => 600000000, 但对于"六万万万", 仍然会
判定为超出转换范围, 返回`-2`. 因为`chinese2int`内部是逆序遍历数字字符串的, "六万万万"会
被首先解释为"六万亿", 而非"六亿万". "六万万零万"会被解释成"六亿零万" => "六亿".
"四亿五千万"也会写作"四万五千万", 或"四万万五千万". 这两种`chinese2int`都可以正确转换.
关于"万万为亿", 可阅读[四万万人民为什么不用四亿](https://www.zhihu.com/question/29731973)
进行了解.

目前已知的合法中文数字字符串可以通过`int2chinese`得到, 但并不是全部, 以下是它的函数签名:

```python
def int2chinese(self, number, lower=True, enumeration=False,
                use_liang=False, use_simple_ten=False,
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
```

对于1306的枚举表示, `int2chinese`只能转换为"一三〇六", 无法得到"一三零六", 但`chinese2int`
可以把"一三零六"转换为1306. 即`chinese2int`可以处理"二千伍佰六十叁"这种大小写混合的数字字符串.

请注意, cn2int只做零或正整数的转换， 不支持负数和浮点数. 另外cn2int**只做数字转换**, 不会
去考虑数字字符串所处的语义环境.例如: 

- "人生不如意事十之八九，可说与人无一二". 如果按照以上的通用pattern处理会得到"十"=>10,
"八九"=>89, "一二"=>12, cn2int这样处理是没有错误的. 错误之处在于这句是俗语, 不该
提取任何数字字符串.
- "五六个石头七八斤", 按照以上的通用pattern处理会得到"五六"=>56(五十六)和"七八"=>78(七十八).
但这改变了原来的语义, 明显是不对的. 因为这句话缺省了顿号. 你应该通过更具体的正则表达式，提取出
"五", "六", "七", "八"来作为数字字符串, 再把它们交给cn2int进行转换. 然后用户要自行把缺省的
顿号也补回来以保持原语义.
- "他花费了三元五角". 货币单位, 温度单位, 长度单位等带有单位的数字都不是cn2int的处理对象.
因为转换后的单位不确定, 很可能得到浮点数. 如: 三元五角 => 3.5元 => 35角 => 350分. 替代方案
是依靠单位用正则表达式把"三元五角"提取出来, 并同时匹配出"三"和"五", cn2int可以做"三"=>3,
"五"=>5. 这样就可以自行把"三元五角"转化到"整数/浮点数+期望单位"了,

## 性能

在cpu:AMD Ryzen 5 4600h环境下使用`performance.py`脚本进行测试

- `int2chinese`: 250 k/s (218123456789)
- `chinese2int`: 160 k/s ("二千一百八十一亿二千三百四十五万六千七百八十九")

## 其他

因为中文数字字符串的合法格式种类较多, 目前还未找到合适的方法对`chinese2int`和`int2chinese`
进行全面测试. 不确定二者是否存在bug. 尤其是`chinese2int`能否检测出中文数字字符串格式非法的
所有情况, 还有待商榷.

`example.py`基于cn2int将中文数字字符串转换为非负浮点数.
