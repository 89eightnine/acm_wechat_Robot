import requests

def get_problem(id):
    url = "https://codeforces.com/api/user.status?handle="+id
    response = requests.get(url)
    data = response.json()
    if(data['status']!='OK'):
        return "找不到这个用户"
    data = data['result']
    return data

def get_unsolved(id):
    data = get_problem(id)
    if(data=='找不到这个用户'):
        return '找不到这个用户'
    solved=set()
    unsolved=set()
    for i in data:
        if(i['verdict']=='OK'):
            solved.add(i['problem']['name'])
        else:
            if i not in solved:
                unsolved.add(i['problem']['name'])
    unsolved=unsolved-solved
    if(len(unsolved)==0):
        return '你是补题大王！怎么全都补完了！'
    ret='未完成题目：\n'
    for i in unsolved:
        ret+='CF'+i['problem']['contestId']+i['problem']['index']+' '+i['problem']['name']+'\n'
    return ret