__all__ = [
    'Months',
    'Weeks',
    'TimeZones',
]

from ..typeclasses import Items


class Months(Items):
    January = '1月'
    February = '2月'
    March = '3月'
    April = '4月'
    May = '5月'
    June = '6月'
    July = '7月'
    August = '8月'
    September = '9月'
    October = '10月'
    November = '11月'
    December = '12月'


class Weeks(Items):
    Monday = '星期一'
    Tuesday = '星期二'
    Wednesday = '星期三'
    Thursday = '星期四'
    Friday = '星期五'
    Saturday = '星期六'
    Sunday = '星期天'


class TimeZones(Items):
    KLT = '+1400', '基里巴斯线岛时间'
    NZDT = '+1300', '新西兰夏时制'
    NZT = '+1200', '新西兰时间'
    AESST = '+1100', '澳大利亚东部标准夏时制,（俄罗斯马加丹时区）,东边（俄罗斯彼得罗巴甫洛夫斯克时区）'
    CST = '+1030', '澳大利亚中部标准时间'
    EAST = '+1000', '东澳大利亚标准时间'
    SAT = '+0930', '南澳大利亚标准时间'
    KST = '+0900', '朝鲜标准时间'
    WST = '+0800', '西澳大利亚标准时间'
    JT = '+0730', '爪哇时间'
    CXT = '+0700', '澳大利亚圣诞岛时间'
    MMT = '+0630', '缅甸时间'
    ALMT = '+0600', '哈萨克斯坦阿拉木图,时间（俄罗斯鄂木斯克时区）'
    TFT = '+0500', '法属凯尔盖朗岛时间'
    AFT = '+0430', '阿富汗时间'
    SCT = '+0400', '塞舌尔马埃岛时间'
    IRT = '+0330', '伊朗时间'
    HMT = '+0300', '希腊地中海时间'
    SST = '+0200', '瑞典夏时制'
    WETDST = '+0100', '西欧光照利用时间（夏时制）'
    GMT = '000', '格林尼治标准时间'
    WET = '+0000', '西欧'
    FNST = '-0100', '巴西费尔南多·迪诺罗尼亚岛,夏令时'
    BRST = '-0200', '巴西利亚夏令时'
    NDT = '-0230', '纽芬兰夏时制'
    BRT = '-0300', '巴西利亚时间'
    NST = '-0330', '纽芬兰（Newfoundland）标准时间'
    EDT = '-0400', '东部夏时制'
    EST = '-0500', '东部标准时间'
    MDT = '-0600', '山地夏时制'
    PDT = '-0700', '太平洋夏时制'
    YST = '-0800', '育空地区标准时'
    HDT = '-0900', '夏威夷/阿拉斯加夏时制'
    MART = '-0930', '马克萨斯群岛时间'
    CAT = '-1000', '中阿拉斯加时间'
    NT = '-1100', '阿拉斯加诺姆时间（Nome,Time）'
    IDLE = '-1200', '国际日期变更线，西边'

    __properties__ = 'description',

    @property
    def description(self) -> str:
        return self._description_