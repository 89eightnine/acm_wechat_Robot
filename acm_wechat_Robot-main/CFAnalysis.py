import matplotlib.pyplot as plt
import requests
import time
from matplotlib import font_manager

def get_problem(id):
    url = "https://codeforces.com/api/user.status?handle=" + id
    response = requests.get(url)
    data = response.json()
    if data['status'] != 'OK':
        return "找不到这个用户"
    return data['result']

def CFAnalysis(id):
    ret=''
    status = get_problem(id)
    if status == None:
        return "名字记错了？真是个杂鱼~"
    if len(status)==0:
        return id + "是题目都不敢交的杂鱼~"
    # 遍历所有提交，对OK的题目统计使用的Language，题目的rating，题目的tag
    # 用一个字典保存每种语言的提交次数
    language_dict = {}
    # 用一个字典保存每种rating的提交次数，分为rating<1200, 1200<=rating<1400, 1400<=rating<1600, 1600<=rating<1900, 1900<=rating<2100, 2100<=rating<2400, rating>=2400
    rating_dict = {'<1200': 0, '1200-1399': 0, '1400-1599': 0, '1600-1899': 0, '1900-2099': 0, '2100-2399': 0, '>=2400': 0}
    # 用一个字典保存每种tag的提交次数
    tag_dict = {}

    ok_count = 0

    for submission in status:
        if submission['verdict'] == 'OK':
            ok_count += 1
            language = submission['programmingLanguage']
            if language in language_dict:
                language_dict[language] += 1
            else:
                language_dict[language] = 1
            if 'rating' in submission['problem']:
                rating = submission['problem']['rating']
                if rating < 1200:
                    rating_dict['<1200'] += 1
                elif rating < 1400:
                    rating_dict['1200-1399'] += 1
                elif rating < 1600:
                    rating_dict['1400-1599'] += 1
                elif rating < 1900:
                    rating_dict['1600-1899'] += 1
                elif rating < 2100:
                    rating_dict['1900-2099'] += 1
                elif rating < 2400:
                    rating_dict['2100-2399'] += 1
                else:
                    rating_dict['>=2400'] += 1
            tags = submission['problem']['tags']
            for tag in tags:
                if tag in tag_dict:
                    tag_dict[tag] += 1
                else:
                    tag_dict[tag] = 1
    
    if(ok_count<400):
        ret+=f"400个AC都没有的杂鱼{id}~\n"
    else:
        ret+=f"写了这么多题，一定没有npy吧~杂鱼{id}~\n"
    ret+="\n"

    # 取前三的语言
    ret+="你的前三提交语言是：\n"
    language_list = sorted(language_dict.items(), key=lambda x: x[1], reverse=True)
    for i in range(min(3, len(language_list))):
        ret+=f"{language_list[i][0]}: {language_list[i][1]}\n"
    ret+="\n"

    # 取前五的tag
    ret+="你的前三tag是：\n"
    tag_list = sorted(tag_dict.items(), key=lambda x: x[1], reverse=True)
    for i in range(min(3, len(tag_list))):
        ret+=f"{tag_list[i][0]}: {tag_list[i][1]}\n"
    ret+="\n"

    # 取前三的rating
    ret+="你的提交rating分布如下：\n"
    for key in rating_dict:
        ret+=f"{key}: {rating_dict[key]}\n"
    ret+="\n"

    ret+="完整语言/标签统计输入#cfanalysis {id} lang/tag查看\n"
    return ret

def CFLangAnalysis(id):
    data = get_problem(id)
    if data == '找不到这个用户':
        return '找不到这个用户'
    
    language_dict = {}
    for submission in data:
        lang = submission['programmingLanguage']
        if submission['verdict'] == 'OK':
            if lang in language_dict:
                language_dict[lang] += 1
            else:
                language_dict[lang] = 1
    
    ret = "你的提交语言分布如下：\n"
    sorted_language_dict = sorted(language_dict.items(), key=lambda x: x[1], reverse=True)
    for key, value in sorted_language_dict:
        ret += f"{key}: {value}\n"
    return ret

def CFTagAnalysis(id):
    data = get_problem(id)
    if data == '找不到这个用户':
        return '找不到这个用户'
    
    tag_dict = {}
    for submission in data:
        if submission['verdict'] == 'OK':
            for tag in submission['problem']['tags']:
                if tag in tag_dict:
                    tag_dict[tag] += 1
                else:
                    tag_dict[tag] = 1
    
    ret = "你的提交标签分布如下：\n"
    sorted_tag_dict = sorted(tag_dict.items(), key=lambda x: x[1], reverse=True)
    for key, value in sorted_tag_dict:
        ret += f"{key}: {value}\n"
    return ret

def CFLangDraw(id):
    data = get_problem(id)
    if data == '找不到这个用户':
        return '找不到这个用户'
    
    language_dict = {}
    for submission in data:
        lang = submission['programmingLanguage']
        if submission['verdict'] == 'OK':
            if lang in language_dict:
                language_dict[lang] += 1
            else:
                language_dict[lang] = 1
    
    sorted_language_dict = sorted(language_dict.items(), key=lambda x: x[1], reverse=True)
    labels = []
    sizes = []
    for key, value in sorted_language_dict:
        labels.append(key)
        sizes.append(value)
    
    def autopct(pct):
        return ('%1.1f%%' % pct) if pct >= 2.5 else ''
    plt.figure(figsize=(10, 10))
    plt.pie(sizes, labels=labels, autopct=autopct)
    plt.axis('equal')
    plt.show()
    plt.savefig('lang.png')
    return 'lang.png'

def CFTagDraw(id):
    data = get_problem(id)
    if data == '找不到这个用户':
        return '找不到这个用户'
    
    tag_dict = {}
    for submission in data:
        if submission['verdict'] == 'OK':
            for tag in submission['problem']['tags']:
                if tag in tag_dict:
                    tag_dict[tag] += 1
                else:
                    tag_dict[tag] = 1
    
    sorted_tag_dict = sorted(tag_dict.items(), key=lambda x: x[1], reverse=True)
    labels = []
    sizes = []
    for key, value in sorted_tag_dict:
        labels.append(key)
        sizes.append(value)
    
    def autopct(pct):
        return ('%1.1f%%' % pct) if pct >= 2.5 else ''
    plt.figure(figsize=(10, 10))
    plt.pie(sizes, labels=labels, autopct=autopct)
    plt.axis('equal')
    plt.show()
    plt.savefig('tag.png')
    return 'tag.png'

if __name__ == '__main__':
    id = 'Swan416'
    print(CFAnalysis(id))
    print(CFLangDraw(id))
    print(CFTagDraw(id))