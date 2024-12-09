import requests

def get_problem(id):
    url = "https://codeforces.com/api/user.status?handle=" + id
    response = requests.get(url)
    data = response.json()
    if data['status'] != 'OK':
        return "找不到这个用户"
    return data['result']

def get_unsolved(id):
    data = get_problem(id)
    if data == '找不到这个用户':
        return '找不到这个用户'
    
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
        return '你是补题大王！怎么全都补完了！'
    
    cnt = len(unsolved)
    ret = f"杂鱼怎么留了{cnt}个题没补啊！这么菜的吗？杂鱼杂鱼~\n"
    added_problems = set()
    for submission in data:
        problem_name = submission['problem']['name']
        if problem_name in unsolved and problem_name not in added_problems:
            ret += f"{submission['problem']['contestId']}{submission['problem']['index']} {problem_name}\n"
            added_problems.add(problem_name)
    
    return ret

if __name__ == '__main__':
    print(get_unsolved('Swan416'))