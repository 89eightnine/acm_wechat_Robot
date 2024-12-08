import sys

from PIL import Image, ImageDraw, ImageFont
import Getcodeforces
import io
import requests
from PIL import Image
from io import BytesIO




def get_img(User_name):
    res = Getcodeforces.get_info(User_name)
    if res==None:
        return None
    res = res[0]
    print(f"res :{res}")
    rating = res.get('rating')
    titlePhoto_url = res.get('titlePhoto')
    # 发送GET请求获取图片数据
    response = requests.get(titlePhoto_url)
    titlePhoto_data = BytesIO(response.content)
    titlePhoto = Image.open(titlePhoto_data)
    w,h = titlePhoto.size
    print((w,h))
    titlePhoto = titlePhoto.resize((w//3*2, h//3*2))
    background = Image.new('RGBA', (500,200), (192,192,192))
    background.paste(titlePhoto, (0, 0))

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('fonts/Roboto-Regular.ttf', 50)
    draw.text((220,10), User_name, font=font,fill='black')
    draw.text((220,100), 'rating: '+str(rating), font=font , fill='black')





    background.save('out.png')
    return 'out.png'

    # # 发送图片
    # itchat.send('@img@' + output.getvalue(), toUserName='filehelper')
    #
    # # 保存图片
    # image.save("codeforces_info.png")

if __name__ == '__main__':
    get_img('catbiscuit')