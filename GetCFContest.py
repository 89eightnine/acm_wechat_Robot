import requests
import time

def get_cf_contests():
    url = 'https://codeforces.com/api/contest.list?gym=false'
    try:
        res = requests.get(url)
    except Exception as e:
        print(e)
        return None
    if res.status_code != 200 or res.json().get('status') != 'OK':
        print(f"error status {res.status_code} {res.json().get('status')}")
        return None
    return res.json().get('result')

def TimeTrans(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

def getCF_Contest():
    ret = 'Codeforces 近期比赛\n\n'
    contests = get_cf_contests()
    if contests is None:
        return ret + "无法获取比赛数据。"

    # 过滤出 phase 为 BEFORE 的比赛
    before_contests = [contest for contest in contests if contest['phase'] == 'BEFORE']

    # 按 startTimeSeconds 倒序排序
    before_contests_sorted = sorted(before_contests, key=lambda x: x['startTimeSeconds'], reverse=False)

    # 构建输出字符串
    for contest in before_contests_sorted:
        ret += f"{contest['name']}\n开始时间: {TimeTrans(contest['startTimeSeconds'])}\n\n"

    ret += f"共{len(before_contests_sorted)}场比赛,杂鱼学长怎么一场都不敢打啊~"

    return ret

if __name__ == '__main__':
    result = getCF_Contest()
    print(result)