from __future__ import annotations

import random


PHONE_PREFIXES = [
    "130",
    "131",
    "132",
    "133",
    "135",
    "136",
    "137",
    "138",
    "139",
    "150",
    "151",
    "152",
    "155",
    "156",
    "157",
    "158",
    "159",
    "166",
    "175",
    "176",
    "177",
    "178",
    "180",
    "181",
    "182",
    "183",
    "185",
    "186",
    "187",
    "188",
    "189",
]

LAST_NAMES = ["李", "王", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴", "徐", "孙", "胡", "朱", "高", "林"]
FIRST_NAMES = ["伟", "芳", "娜", "敏", "静", "秀英", "丽", "强", "磊", "军", "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀兰", "霞", "平", "刚", "桂英"]
AREA_CODES = [
    "110101",
    "110102",
    "310101",
    "440103",
    "440104",
    "440106",
    "440303",
    "440304",
    "440305",
    "330106",
    "320106",
    "510107",
]
ID_CARD_WEIGHTS = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
ID_CARD_CHECK_CODES = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]


def generate_random_phone() -> str:
    """复刻 Postman 的随机手机号生成逻辑。"""

    return random.choice(PHONE_PREFIXES) + str(random.randint(0, 99_999_999)).zfill(8)


def generate_random_chinese_name() -> str:
    """按 Postman 脚本生成两字中文姓名。"""

    return random.choice(LAST_NAMES) + random.choice(FIRST_NAMES)


def generate_random_id_card() -> str:
    """生成符合校验位规则的随机身份证号。"""

    year = random.randint(1970, 2005)
    month = random.randint(1, 12)

    if month in {4, 6, 9, 11}:
        max_day = 30
    elif month == 2:
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        max_day = 29 if is_leap else 28
    else:
        max_day = 31

    day = random.randint(1, max_day)
    birthday = f"{year}{month:02d}{day:02d}"
    sequence = f"{random.randint(1, 999):03d}"
    first17 = random.choice(AREA_CODES) + birthday + sequence
    checksum = sum(int(first17[index]) * ID_CARD_WEIGHTS[index] for index in range(17))
    return first17 + ID_CARD_CHECK_CODES[checksum % 11]
