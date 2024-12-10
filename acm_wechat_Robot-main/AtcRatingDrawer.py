import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time
from matplotlib import font_manager
import re

def fetch_contest_history(handle):
    url = f'https://atcoder.jp/users/{handle}/history'
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    return res.text

def parse_contest_history(html):
    soup = BeautifulSoup(html, 'html.parser')
    contest_history = []

    # 查找比赛历史表格
    table = soup.find('table', class_='table')
    if table:
        print("Table found")
        rows = table.find_all('tr')
        for row in rows[1:]:  # 跳过表头
            cols = row.find_all('td')
            if len(cols) >= 7:
                date = cols[0].text.strip()
                contest_name = cols[1].text.strip()
                new_rating_text = cols[6].text.strip()
                if new_rating_text:  # 检查 new_rating_text 是否为空
                    try:
                        # 使用正则表达式提取数字部分
                        new_rating = int(re.sub(r'\D', '', new_rating_text))
                        contest_history.append({
                            'date': date,
                            'contest_name': contest_name,
                            'new_rating': new_rating
                        })
                    except ValueError:
                        print(f"Skipping invalid rating value: {new_rating_text}")
                else:
                    print(f"Empty new rating for contest: {contest_name} on {date}")
            else:
                print(f"Unexpected number of columns: {len(cols)}")
    else:
        print("No table found with class 'table'")
    return contest_history

def plot_rating_change(contest_history):
    # 提取日期和评分
    dates = [contest['date'] for contest in contest_history]
    ratings = [contest['new_rating'] for contest in contest_history]

    # 设置中文字体
    font_path = "C:/Windows/Fonts/simhei.ttf"  # 你可以根据需要更改字体路径
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()

    # 绘制折线图
    plt.figure(figsize=(10, 5))
    plt.plot(dates, ratings, marker='o', linestyle='-', color='b')
    plt.xlabel('Date', fontproperties=font_prop)
    plt.ylabel('New Rating', fontproperties=font_prop)
    plt.title('AtCoder Rating Change', fontproperties=font_prop)
    plt.xticks(rotation=45, fontproperties=font_prop)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('atcoder_rating_change.png')
    plt.show()

if __name__ == '__main__':
    handle = 'Swan416'
    html = fetch_contest_history(handle)
    if html:
        contest_history = parse_contest_history(html)
        if contest_history:
            plot_rating_change(contest_history)
        else:
            print("No contest history found.")
    else:
        print("Failed to retrieve contest history.")