"""
中国行政区划相关。
"""
from enum import Enum

from .typeclasses import IntegerChoices, Items


class Region(IntegerChoices):
    NORTH = 1, '华北'
    NORTHEAST = 2, '东北'
    EAST = 3, '华东'
    SOUTH_CENTRAL = 4, '中南'
    SOUTHWEST = 5, '西南'
    NORTHWEST = 6, '西北'
    HMT = 0, '港澳台'


class Province(Items):
    """
    中国省级行政区。
    """
    BEIJING = '11', '京', 'BJ', '北京', '北京市'
    TIANJIN = '12', '津', 'TJ', '天津', '天津市'
    HEBEI = '13', '冀', 'HE', '河北', '河北省'
    SHANXI = '14', '晋', 'SX', '山西', '山西省'
    NEI_MONGOLIA = '15', '蒙', 'NM', '内蒙古', '内蒙古自治区'
    LIAONING = '21', '辽', 'LN', '辽宁', '辽宁省'
    JILIN = '22', '吉', 'JL', '吉林', '吉林省'
    HEILONGJIANG = '23', '黑', 'HL', '黑龙江', '黑龙江省'
    SHANGHAI = '31', '沪', 'SH', '上海', '上海市'
    JIANGSU = '32', '苏', 'JS', '江苏', '江苏省'
    ZHEJIANG = '33', '浙', 'ZJ', '浙江', '浙江省'
    ANHUI = '34', '皖', 'AH', '安徽', '安徽省'
    FUJIAN = '35', '闽', 'FJ', '福建', '福建省'
    JIANGXI = '36', '赣', 'JX', '江西', '江西省'
    SHANDONG = '37', '鲁', 'SD', '山东', '山东省'
    HENAN = '41', '豫', 'HA', '河南', '河南省'
    HUBEI = '42', '鄂', 'HB', '湖北', '湖北省'
    HUNAN = '43', '湘', 'HN', '湖南', '湖南省'
    GUANGDONG = '44', '粤', 'GD', '广东', '广东省'
    GUANGXI = '45', '桂', 'GX', '广西', '广西壮族自治区'
    HAINAN = '46', '琼', 'HI', '海南', '海南省'
    CHONGQING = '50', '渝', 'CQ', '重庆', '重庆市'
    SICHUAN = '51', '川', 'SC', '四川', '四川省'
    GUIZHOU = '52', '黔', 'GN', '贵州', '贵州省'
    YUNNAN = '53', '滇', 'YZ', '云南', '云南省'
    XIZANG = '54', '藏', 'XY', '西藏', '西藏自治区'
    SHAANXI = '61', '陕', 'SN', '陕西', '陕西省'
    GANSU = '62', '甘', 'GS', '甘肃', '甘肃省'
    QINGHAI = '63', '青', 'QH', '青海', '青海省'
    NINGXIA = '64', '宁', 'NX', '宁夏', '宁夏回族自治区'
    XINJIANG = '65', '新', 'XJ', '新疆', '新疆维吾尔自治区'
    TAIWAN = '71', '台', 'TW', '台湾', '台湾省'
    HONG_KONG = '81', '港', 'HK', '香港', '香港特别行政区'
    MACAO = '82', '澳', 'MO', '澳门', '澳门特别行政区'

    __properties__ = 'short', 'code', 'nick', 'label'

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
        tag = self.value[0][0]
        return Region.HMT if tag in '789' else Region(int(tag))

    @property
    def id_code(self) -> str:
        """行政区划代码。（6位）"""
        return self.value[0].ljust(6, '0')

    @property
    def statistics_code(self) -> str:
        """统计用区划代码。（12位）"""
        return self.value[0].ljust(12, '0')
