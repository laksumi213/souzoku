import datetime
import re

WAREKI_START = {
    '令和': datetime.datetime(2019, 5, 1),
    '平成': datetime.datetime(1989, 1, 8),
    '昭和': datetime.datetime(1926, 12, 25),
    '大正': datetime.datetime(1912, 1, 1),
    '明治': datetime.datetime(1868, 1, 1)
}


def convert_to_wareki(y, m, d):
    """西暦の年月日を和暦の年に変換する."""
    try:
        y_m_d = datetime.datetime(y, m, d)
        if WAREKI_START['令和'] <= y_m_d:
            reiwa_year = WAREKI_START['令和'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = '令和'
        elif WAREKI_START['平成'] <= y_m_d:
            reiwa_year = WAREKI_START['平成'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = '平成'
        elif WAREKI_START['昭和'] <= y_m_d:
            reiwa_year = WAREKI_START['昭和'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = '昭和'
        elif WAREKI_START['大正'] <= y_m_d:
            reiwa_year = WAREKI_START['大正'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = '大正'
        elif WAREKI_START['明治'] <= y_m_d:
            reiwa_year = WAREKI_START['明治'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = '明治'
        else:
            return '不明'

        if year == 1:
            # year = '元'
            year = '1'

        return era_str + str(year) + '年'
    except ValueError as e:
        raise e


def convert_to_wareki2(s):
    try:
        dt = re.findall('[0-9]+', s)
        y = int(dt[0])
        m = int(dt[1])
        d = int(dt[2])
        y_m_d = datetime.datetime(y, m, d)
        if WAREKI_START['令和'] <= y_m_d:
            reiwa_year = WAREKI_START['令和'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = '令和'
        elif WAREKI_START['平成'] <= y_m_d:
            reiwa_year = WAREKI_START['平成'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = '平成'
        elif WAREKI_START['昭和'] <= y_m_d:
            reiwa_year = WAREKI_START['昭和'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = '昭和'
        elif WAREKI_START['大正'] <= y_m_d:
            reiwa_year = WAREKI_START['大正'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = '大正'
        elif WAREKI_START['明治'] <= y_m_d:
            reiwa_year = WAREKI_START['明治'].year
            era_year = y_m_d.year
            year = (era_year - reiwa_year) + 1
            era_str = '明治'
        else:
            return '不明'

        if year == 1:
            # year = '元'
            year = '1'

        return f'{era_str}{str(year)}年{m}月{d}日'
    except Exception as e:
        print(e)
        return ''
    # except ValueError as e:
    #     raise e