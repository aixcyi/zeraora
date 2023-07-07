"""
常用枚举。
"""
from enum import Enum

from ..typeclasses import Items


class Region(int, Items):
    """
    用于划分省级行政区的大区。

    可视为 ``django.db.models.enums.IntegerChoices`` 子类使用。
    """
    NORTH = 1, '华北'
    NORTHEAST = 2, '东北'
    EAST = 3, '华东'
    SOUTH_CENTRAL = 4, '中南'
    SOUTHWEST = 5, '西南'
    NORTHWEST = 6, '西北'
    HMT = 0, '港澳台'

    __properties__ = 'label',

    @property
    def label(self) -> str:
        return self._label_


class Province(str, Items):
    """
    中国省级行政区。

    可视为 ``django.db.models.enums.TextChoices`` 子类使用。
    """
    BEIJING = '11', 11, '京', 'BJ', '北京', Region.NORTH, '北京市'
    TIANJIN = '12', 12, '津', 'TJ', '天津', Region.NORTH, '天津市'
    HEBEI = '13', 13, '冀', 'HE', '河北', Region.NORTH, '河北省'
    SHANXI = '14', 14, '晋', 'SX', '山西', Region.NORTH, '山西省'
    NEI_MONGOLIA = '15', 15, '蒙', 'NM', '内蒙古', Region.NORTH, '内蒙古自治区'
    LIAONING = '21', 21, '辽', 'LN', '辽宁', Region.NORTHEAST, '辽宁省'
    JILIN = '22', 22, '吉', 'JL', '吉林', Region.NORTHEAST, '吉林省'
    HEILONGJIANG = '23', 23, '黑', 'HL', '黑龙江', Region.NORTHEAST, '黑龙江省'
    SHANGHAI = '31', 31, '沪', 'SH', '上海', Region.EAST, '上海市'
    JIANGSU = '32', 32, '苏', 'JS', '江苏', Region.EAST, '江苏省'
    ZHEJIANG = '33', 33, '浙', 'ZJ', '浙江', Region.EAST, '浙江省'
    ANHUI = '34', 34, '皖', 'AH', '安徽', Region.EAST, '安徽省'
    FUJIAN = '35', 35, '闽', 'FJ', '福建', Region.EAST, '福建省'
    JIANGXI = '36', 36, '赣', 'JX', '江西', Region.EAST, '江西省'
    SHANDONG = '37', 37, '鲁', 'SD', '山东', Region.EAST, '山东省'
    HENAN = '41', 41, '豫', 'HA', '河南', Region.SOUTH_CENTRAL, '河南省'
    HUBEI = '42', 42, '鄂', 'HB', '湖北', Region.SOUTH_CENTRAL, '湖北省'
    HUNAN = '43', 43, '湘', 'HN', '湖南', Region.SOUTH_CENTRAL, '湖南省'
    GUANGDONG = '44', 44, '粤', 'GD', '广东', Region.SOUTH_CENTRAL, '广东省'
    GUANGXI = '45', 45, '桂', 'GX', '广西', Region.SOUTH_CENTRAL, '广西壮族自治区'
    HAINAN = '46', 46, '琼', 'HI', '海南', Region.SOUTH_CENTRAL, '海南省'
    CHONGQING = '50', 50, '渝', 'CQ', '重庆', Region.SOUTHWEST, '重庆市'
    SICHUAN = '51', 51, '川', 'SC', '四川', Region.SOUTHWEST, '四川省'
    GUIZHOU = '52', 52, '黔', 'GN', '贵州', Region.SOUTHWEST, '贵州省'
    YUNNAN = '53', 53, '滇', 'YZ', '云南', Region.SOUTHWEST, '云南省'
    XIZANG = '54', 54, '藏', 'XY', '西藏', Region.SOUTHWEST, '西藏自治区'
    SHAANXI = '61', 61, '陕', 'SN', '陕西', Region.NORTHWEST, '陕西省'
    GANSU = '62', 62, '甘', 'GS', '甘肃', Region.NORTHWEST, '甘肃省'
    QINGHAI = '63', 63, '青', 'QH', '青海', Region.NORTHWEST, '青海省'
    NINGXIA = '64', 64, '宁', 'NX', '宁夏', Region.NORTHWEST, '宁夏回族自治区'
    XINJIANG = '65', 65, '新', 'XJ', '新疆', Region.NORTHWEST, '新疆维吾尔自治区'
    TAIWAN = '71', 71, '台', 'TW', '台湾', Region.HMT, '台湾省'
    HONG_KONG = '81', 81, '港', 'HK', '香港', Region.HMT, '香港特别行政区'
    MACAO = '82', 82, '澳', 'MO', '澳门', Region.HMT, '澳门特别行政区'

    __properties__ = 'numeric', 'short', 'code', 'nick', 'region', 'label'

    @property
    def numeric(self) -> int:
        """整数形式的区划代码。（2位）"""
        return self._numeric_

    @property
    def short(self) -> str:
        """简称。"""
        return self._short_

    @property
    def code(self) -> str:
        """字母码（见 GB/T 2260--2007）。"""
        return self._code_

    @property
    def nick(self) -> str:
        """常用别称。"""
        return self._nick_

    @property
    def label(self) -> str:
        """全称。"""
        return self._label_

    @property
    def region(self) -> Region:
        """所在大区。"""
        return self._region_

    @property
    def id_code(self) -> str:
        """行政区划代码。（6位）"""
        return self.value[0].ljust(6, '0')

    @property
    def statistics_code(self) -> str:
        """统计用区划代码。（12位）"""
        return self.value[0].ljust(12, '0')

    def __int__(self) -> int:
        return self._numeric_

    def _generate_next_value_(name, start, count, last_values):
        return name


class DivisionLevel(Enum):
    """
    行政区划的层次级别。

    主要参照 `统计用区划代码编制规则 <http://www.stats.gov.cn/sj/tjbz/gjtjbz/202302/t20230213_1902741.html>`_ 。
    """

    PROVINCE = 1
    """省级。自顶向下的第一个层级，包括省、直辖市、自治区、特别行政区。"""
    PREFECTURE = 2
    """市级。自顶向下的第二个层级，包括地级市、地级县、自治州、盟等。"""
    COUNTY = 3
    """县级。自顶向下的第三个层级，包括县、自治县、县级市、旗、自治旗、市辖区等。"""
    TOWNSHIP = 4
    """乡级。自顶向下的第四个层级，包括县辖区、乡、镇、街道等。"""
    VILLAGE = 5
    """村级。自顶向下的第五个层级。"""


class Degree(int, Items):
    """
    描述程度的五个档位。
    """
    HIGHEST = 100, '最高'
    HIGH = 50, '高'
    NORMAL = 0, '正常'
    LOW = -50, '低'
    LOWEST = -100, '最低'

    __properties__ = 'label',

    @property
    def label(self):
        return self._label_
