"""
中国行政区划相关。
"""

from zeraora import IntegerChoices


class Province(IntegerChoices):
    """
    中国省级行政区。
    """
    BEIJING = 11, '北京市'
    TIANJIN = 12, '天津市'
    HEBEI = 13, '河北省'
    SHANXI = 14, '山西省'
    NEI_MONGOLIA = 15, '内蒙古自治区'
    LIAONING = 21, '辽宁省'
    JILIN = 22, '吉林省'
    HEILONGJIANG = 23, '黑龙江省'
    SHANGHAI = 31, '上海市'
    JIANGSU = 32, '江苏省'
    ZHEJIANG = 33, '浙江省'
    ANHUI = 34, '安徽省'
    FUJIAN = 35, '福建省'
    JIANGXI = 36, '江西省'
    SHANDONG = 37, '山东省'
    HENAN = 41, '河南省'
    HUBEI = 42, '湖北省'
    HUNAN = 43, '湖南省'
    GUANGDONG = 44, '广东省'
    GUANGXI = 45, '广西壮族自治区'
    HAINAN = 46, '海南省'
    CHONGQING = 50, '重庆市'
    SICHUAN = 51, '四川省'
    GUIZHOU = 52, '贵州省'
    YUNNAN = 53, '云南省'
    XIZANG = 54, '西藏自治区'
    SHAANXI = 61, '陕西省'
    GANSU = 62, '甘肃省'
    QINGHAI = 63, '青海省'
    NINGXIA = 64, '宁夏回族自治区'
    XINJIANG = 65, '新疆维吾尔自治区'
    TAIWAN = 71, '台湾省'
    HONG_KONG = 81, '香港特别行政区'
    MACAO = 82, '澳门特别行政区'


REGIONS = {
    '华东': [Province.SHANGHAI, Province.JIANGSU, Province.ZHEJIANG, Province.ANHUI, Province.JIANGXI],
    '华北': [
        Province.BEIJING, Province.TIANJIN, Province.HEBEI, Province.SHANXI, Province.NEI_MONGOLIA, Province.SHANDONG
    ],
    '华中': [Province.HENAN, Province.HUBEI, Province.HUNAN],
    '华南': [Province.FUJIAN, Province.GUANGDONG, Province.GUANGXI, Province.HAINAN],
    '东北': [Province.LIAONING, Province.JILIN, Province.HEILONGJIANG],
    '西北': [Province.SHAANXI, Province.GANSU, Province.QINGHAI, Province.NINGXIA, Province.XINJIANG],
    '西南': [Province.CHONGQING, Province.SICHUAN, Province.GUIZHOU, Province.YUNNAN, Province.XIZANG],
    '港澳台': [Province.TAIWAN, Province.HONG_KONG, Province.MACAO],
}
