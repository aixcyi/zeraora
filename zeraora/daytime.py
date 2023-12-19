"""
日期、时间、时刻相关。
"""
from __future__ import annotations

__all__ = [
    'Months',
    'Weeks',
    'TimeZones',
    'delta2hms',
    'delta2ms',
    'delta2s',
    'wdate',
    'get_week_range',
    'get_week_side',
    'get_week_in_year',
]

from datetime import date, datetime, timedelta

from zeraora.enums import Items


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


def delta2hms(delta: timedelta) -> tuple[int, int, float]:
    """
    将时间增量转换为时分秒格式，其中秒钟以小数形式包含毫秒和微秒。

    :param delta: 时间增量。
    :return: 一个三元元组。
    """
    h = delta.seconds // 3600
    m = delta.seconds % 3600 // 60
    s = delta.seconds % 60 + delta.microseconds / 1000000
    return h, m, s


def delta2ms(delta: timedelta) -> tuple[int, float]:
    """
    将时间增量转换为分秒格式，其中秒钟以小数形式包含毫秒和微秒。

    :param delta: 时间增量。
    :return: 二元元组。前者用一个整数表示分钟数，
             后者用一个小数表示秒钟数和纳秒数。
    """
    m = delta.seconds // 60
    s = delta.seconds % 60 + delta.microseconds / 1000000
    return m, s


def delta2s(delta: timedelta) -> float:
    """
    将时间增量转换为秒钟数，以小数形式包含毫秒和微秒。

    :param delta: 时间增量。
    :return: 一个小数。
    """
    return delta.seconds + delta.microseconds / 1000000


# 仿构造器命名
def wdate(year: int, week_in_year: int, day_in_week: int, sunday_first=False) -> date:
    """
    将某一年的某一周的星期几转换为一个具体的日期。

    :param year: 具体年份。比如 2012、2023 等。
    :param week_in_year: 一年中的第几周。从 0 开始。
    :param day_in_week: 星期几。0 表示周日、1 表示周一，以此类推。
    :param sunday_first: 是否以周日为一周的开始。
    :return: 一个日期。
    """
    day = f'{year:04d}-{week_in_year:02d}-{day_in_week:1d}'
    fmt = '%Y-%U-%w' if sunday_first else '%Y-%W-%w'
    return datetime.strptime(day, fmt).date()


def get_week_range(year: int,
                   week_in_year: int,
                   month: int = None,
                   sunday_first=False) -> tuple[date, ...]:
    """
    计算一年中某一周对应的所有日期。

    :param year: 具体年份。比如 2012、2023 等。
    :param week_in_year: 一年中的第几周。从 0 开始。
    :param month: 具体月份。若指定了这个参数，则只计算这个月的那一部分日期。
    :param sunday_first: 是否以周日为一周的开始。
    :return: 若指定了不恰当的月份，有可能返回空列表。
    :raise ValueError: year 年的 week_in_year 周不在当年的 month 月里。
    """
    fmt = '%Y-%U-%w' if sunday_first else '%Y-%W-%w'
    start = f'{year:04d}-{week_in_year:02d}-{0 if sunday_first else 1}'
    start = datetime.strptime(start, fmt).date()
    days = tuple(start + timedelta(days=i) for i in range(7))
    days = days if month is None else tuple(day for day in days if day.month == month)
    if not days:
        raise ValueError(
            f'{year} 年的 {week_in_year} 周不在当年的 {month} 月里。'
        )
    return days


def get_week_side(year: int,
                  week_in_year: int,
                  month: int = None,
                  sunday_first=False) -> tuple[date, date]:
    """
    计算一年中某一周对应的第一天和最后一天。

    :param year: 具体年份。比如 2012、2023 等。
    :param week_in_year: 一年中的第几周。从 0 开始。
    :param month: 具体月份。若指定了这个参数，则只计算这个月的那一部分日期。
    :param sunday_first: 是否以周日为一周的开始。
    :return: 两个日期，表示（这个月的）这一周的第一天和最后一天。
    :raise ValueError: year 年的 week_in_year 周不在当年的 month 月里。
    """
    days = get_week_range(year, week_in_year, month, sunday_first)
    return days[0], days[-1]


def get_week_in_year(*args, sunday_first=False) -> int:
    """
    计算一个具体日期自一年开始的周序号。

    如果 ``sunday_first=False`` ，那么一年中第一个星期一之前的日子都算作第 0 周。
    如果 ``sunday_first=True`` ，那么一年中第一个星期日之前的日子都算作第 0 周。

    - ``get_week_in_year(date)`` ，提供一个日期。
    - ``get_week_in_year(datetime)`` ，提供一个时刻。
    - ``get_week_in_year(int, int, int)`` ，分别提供年月日。

    :param args: 参数。
    :param sunday_first: 是否以周日作为一周的开始。
    :return: 一个从 0 开始递增的整数。
    """
    if len(args) == 1 and isinstance(args[0], date):
        day = args[0]
    elif len(args) >= 3 and all(isinstance(a, int) for a in args):
        day = date(*args[:3])
    else:
        raise ValueError
    week = day.strftime('%U') if sunday_first else day.strftime('%W')
    return int(week)
