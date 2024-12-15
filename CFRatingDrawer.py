import matplotlib.pyplot as plt
import requests
import time
from matplotlib import font_manager

def fetch_contest_data(handle):
    url = f'https://codeforces.com/api/user.rating?handle={handle}'
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    data = res.json()
    if data['status'] != 'OK':
        print(f"Error in response: {data['status']}")
        return None
    return data['result']

def plot_rating_change(contests):
    # 提取时间戳和评分
    timestamps = [contest['ratingUpdateTimeSeconds'] for contest in contests]
    ratings = [contest['newRating'] for contest in contests]

    # 将时间戳转换为可读日期
    dates = [time.strftime("%Y-%m-%d", time.localtime(ts)) for ts in timestamps]

    # 找到最高点
    max_rating = max(ratings)
    max_index = ratings.index(max_rating)

    min_rating = min(ratings)

    # 设置中文字体
    font_path = "C:/Windows/Fonts/simhei.ttf"  # 你可以根据需要更改字体路径
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()

    # 绘制折线图
    plt.figure(figsize=(10, 5))

    # 添加背景色块
    if(max_rating>0):
        plt.axhspan(max(0,min_rating-50), 1200, facecolor='grey', alpha=0.5)
    if(max_rating>1200):
        plt.axhspan(1200, 1400, facecolor='green', alpha=0.5)
    if(max_rating>1400):
        plt.axhspan(1400, 1600, facecolor='cyan', alpha=0.5)
    if(max_rating>1600):
        plt.axhspan(1600, 1900, facecolor='blue', alpha=0.5)
    if(max_rating>1900):
        plt.axhspan(1900, 2100, facecolor='purple', alpha=0.5)
    if(max_rating>2100):
        plt.axhspan(2100, 2400, facecolor='orange', alpha=0.5)
    if(max_rating>2400):
        plt.axhspan(2400, max_rating+100, facecolor='red', alpha=0.5)

    plt.plot(dates, ratings, marker='o', linestyle='-', color='b')
    plt.xlabel(' ', fontproperties=font_prop)
    plt.ylabel('Rating', fontproperties=font_prop)
    plt.title('Codeforces Rating Change', fontproperties=font_prop)
    plt.xticks([])  # 隐藏横坐标
    plt.grid(True)

    # 标记最高点
    plt.plot(dates[max_index], max_rating, marker='o', color='r')
    plt.text(dates[max_index], max_rating, f'{max_rating}', color='r', fontproperties=font_prop)

    plt.tight_layout()
    plt.savefig('rating_change.png')
    #plt.show()

def get_img(handle):
    contests = fetch_contest_data(handle)
    if contests:
        plot_rating_change(contests)
        return 'rating_change.png'
    return None

if __name__ == '__main__':
    handle = 'Swan416'
    contests = fetch_contest_data(handle)
    if contests:
        plot_rating_change(contests)