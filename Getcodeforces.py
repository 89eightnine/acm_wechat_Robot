import requests
from html2image import Html2Image

def get_rate(User_name):
    url = f'https://codeforces.com/api/user.rating?handle={User_name}'
    # print(url)
    try:
        res = requests.get(url)
    except Exception as e:
        print(e)
        return -1
    if res.status_code != 200 or res.json().get('status') != 'OK':
        return -1
    print(res.json())
    return res.json().get('result')[-1].get('newRating')

def get_info(User_name):
    # url = f'https://codeforces.com/api/user.info?handle={User_name}'
    url = f"https://codeforces.com/api/user.info?handles={User_name};Fefer_Ivan&checkHistoricHandles=false"
    try:
        res = requests.get(url)
    except Exception as e:
        print(e)
        return None
    if res.status_code != 200 or res.json().get('status') != 'OK':
        print(f"error status {res.status_code} {res.json().get('status')}")
        return None
    print(res.json())
    return res.json().get('result')

if __name__ == '__main__':
    print(get_info('catbiscuit'))
