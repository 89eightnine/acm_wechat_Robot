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
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 5:
                date = cols[0].text.strip()
                contest_name = cols[1].text.strip()
                new_rating_text = cols[4].text.strip()
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

    # 找到最高最低点
    max_rating = max(ratings)
    min_rating = min(ratings)
    max_position = ratings.index(max_rating)

    # 设置中文字体
    font_path = "C:/Windows/Fonts/simhei.ttf"  # 你可以根据需要更改字体路径
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()

    # 绘制折线图
    plt.figure(figsize=(10, 5))
    
    # 添加背景色块
    # 添加背景色块
    # 0-400 灰色
    plt.axhspan(0, 400, facecolor='gray', alpha=0.5)
    # 400-800 棕色 RGB(128,64,0)
    if(max_rating > 400):
        plt.axhspan(400, 800, facecolor=(128/255, 64/255, 0), alpha=0.5)
    # 800-1200 绿色
    if(max_rating > 800):
        plt.axhspan(800, 1200, facecolor='green', alpha=0.5)
    # 1200-1600 青色
    if(max_rating > 1200):
        plt.axhspan(1200, 1600, facecolor='cyan', alpha=0.5)
    # 1600-2000 蓝色
    if(max_rating > 1600):
        plt.axhspan(1600, 2000, facecolor='blue', alpha=0.5)
    # 2000-2400 黄色
    if(max_rating > 2000):
        plt.axhspan(2000, 2400, facecolor='yellow', alpha=0.5)
    # 2400-2800 橙色
    if(max_rating > 2400):
        plt.axhspan(2400, 2800, facecolor='orange', alpha=0.5)
    # 2800-inf 红色
    if(max_rating > 2800):
        plt.axhspan(2800, max_rating+200, facecolor='red', alpha=0.5)

    plt.plot(dates, ratings, marker='o', linestyle='-', color='b')
    plt.ylabel('Rating', fontproperties=font_prop)
    plt.title('Atcoder Rating Change', fontproperties=font_prop)
    plt.xticks([])  # 隐藏横坐标
    plt.grid(True)

    # 标记最高点
    plt.text(dates[max_position], max_rating, f'{max_rating}', color='red', fontproperties=font_prop)  # 显示最高点值
    plt.plot(dates[max_position], max_rating, 'ro')  # 红色标记最高点

    plt.savefig('atc_out.png')
    #plt.show()

def AtcRatingDrawer(id):
    handle = id
    html = fetch_contest_history(handle)
    if html:
        contest_history = parse_contest_history(html)
        if contest_history:
            plot_rating_change(contest_history)
            return "atc_out.png"
        else:
            print("No contest history found.")
            return None
    else:
        print("Failed to retrieve contest history.")
        return None

if __name__ == '__main__':
    handle = 'jiangly'
    html = fetch_contest_history(handle)
    if html:
        contest_history = parse_contest_history(html)
        if contest_history:
            plot_rating_change(contest_history)
        else:
            print("No contest history found.")
    else:
        print("Failed to retrieve contest history.")