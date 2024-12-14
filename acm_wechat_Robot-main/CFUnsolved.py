import requests

def get_problem(id):
    # id删除&后面的内容
    id = id.split('&')[0]

    url = "https://codeforces.com/api/user.rating?handle=" + id
    response = requests.get(url)
    data = response.json()
    if data['result']:
        url = "https://codeforces.com/api/user.status?handle=" + id
    else :
        return "无法查询机器人信息"
    
    response = requests.get(url)
    data = response.json()
    if data['status'] != 'OK':
        return "找不到这个用户"
    return data['result']

def get_unsolved(id):
    data = get_problem(id)
    if data == '找不到这个用户':
        return '找不到这个用户'
    if data == '无法查询机器人信息':
        return '杂鱼不会以为我会傻乎乎地去查机器人信息把自己弄爆炸吧~\n'
    
    solved = set()
    unsolved = set()
    
    for submission in data:
        problem_name = submission['problem']['name']
        if submission['verdict'] == 'OK':
            solved.add(problem_name)
        else:
            if problem_name not in solved:
                unsolved.add(problem_name)
    
    unsolved = unsolved - solved
    
    if len(unsolved) == 0:
        if len(solved) == 0:
            return "杂鱼没做过题目也来装蒜？"
        return "补完题就滚去加训啊！杂鱼一点自觉性没有~"
    
    cnt = len(unsolved)
    ret = f"杂鱼怎么留了{cnt}个题没补啊！这么菜的吗？杂鱼杂鱼~\n"
    added_problems = set()
    for submission in data:
        problem_name = submission['problem']['name']
        if problem_name in unsolved and problem_name not in added_problems:
            ret += f"CF{submission['problem']['contestId']}{submission['problem']['index']} "
            added_problems.add(problem_name)
    
    return ret

if __name__ == '__main__':
    print(get_unsolved('Swan416'))