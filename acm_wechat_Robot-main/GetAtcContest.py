import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def get_atc_contests():
    url = 'https://atcoder.jp/contests/'
    try:
        res = requests.get(url)
    except Exception as e:
        print(e)
        return None
    if res.status_code != 200:
        print(f"error status {res.status_code}")
        return None
    return res.text

def parse_contests(html):
    soup = BeautifulSoup(html, 'html.parser')
    upcoming_contests = []

    # 查找未进行的比赛
    upcoming_table = soup.find('div', id='contest-table-upcoming')
    if upcoming_table:
        rows = upcoming_table.find_all('tr')
        for row in rows[1:]:  # 跳过表头
            cols = row.find_all('td')
            if len(cols) >= 3:
                contest_name = cols[1].text.strip()
                start_time = cols[0].text.strip()
                duration = cols[2].text.strip()
                upcoming_contests.append({
                    'name': contest_name,
                    'start_time': start_time,
                    'duration': duration
                })
    return upcoming_contests

def timeTSF(org):
    try:
        dt = datetime.strptime(org, '%Y-%m-%d %H:%M:%S%z')
        dt = dt - timedelta(hours=1)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        print(e)
        return org

def GetAtcContest():
    html = get_atc_contests()
    if html:
        contests = parse_contests(html)
        if contests:
            ret = 'AtCoder 近期比赛\n'
            for contest in contests:
                ret += f"{contest['name'][4:]}\n开始时间: {timeTSF(contest['start_time'])}\n\n"
            ret += f"共{len(contests)}场比赛,杂鱼学长怎么一场都不敢打啊~"
            return ret
        else:
            return "No upcoming contests found."
    else:
        return "Failed to retrieve contests."

if __name__ == '__main__':
    result = GetAtcContest()
    print(result)