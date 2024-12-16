import requests
import time

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

def timetsf(localtime):
    target_time = time.strptime("05:00:00", "%H:%M:%S")
    target_seconds = target_time.tm_hour * 3600 + target_time.tm_min * 60 + target_time.tm_sec
    current_seconds = localtime.tm_hour * 3600 + localtime.tm_min * 60 + localtime.tm_sec
    if current_seconds >= target_seconds:
        return current_seconds - target_seconds
    else:
        return 86400 - (target_seconds - current_seconds)

def get_sum_2024(id):
    data=get_problem(id)
    if data == "找不到这个用户":
        return "找不到这个用户"
    if data == "无法查询机器人信息":
        return "无法查询机器人信息"

    ## 记录vp场次，vp队友出现次数
    vp_cnt=0;vp_viewed={}
    vp_partner={}
    ## 记录每天按5点算最早的提交和最晚的提交
    earliest_submission_time=1e6;earliest_subbmission_id="";earliest_subbmission_title="";full_earliest_submission_time=0
    latest_submission_time=0;latest_subbmission_id="";latest_subbmission_title="";full_latest_submission_time=0
    ## wa次数最多的题目，wa次数最多的题目的wa次数
    wa_cnt={}
    wa_max_id="";wa_max_title="";wa_max_cnt=0
    ## 第一次wa的提交到最后ac时间最长的题目以及花费的时间
    question_ac_time={};question_wa_time={}
    ## 全年第一道题目的所有信息
    first_question_time=0;first_question_id="";first_question_title=""
    ## 一遍过的题目个数
    dont_miss_ac_cnt=0
    ## 全年提交次数
    submission_cnt=0

    for subbmission in data:
        if time.localtime(subbmission['creationTimeSeconds']).tm_year < 2024:
            break
        if time.localtime(subbmission['creationTimeSeconds']).tm_year > 2024:
            continue

        submission_cnt+=1

        first_question_time=time.localtime(subbmission['creationTimeSeconds'])
        first_question_id="CF" + str(subbmission['contestId']) + str(subbmission['problem']['index'])
        first_question_title=subbmission['problem']['name']

        if subbmission["author"]["participantType"] == "VIRTUAL":
            if vp_viewed.get(subbmission['author']['contestId'], 0) == 0:
                vp_cnt+=1
                vp_viewed[subbmission['author']['contestId']]=1
                for members in subbmission['author']['members']:
                    if members['handle'].lower() != id.lower():
                        if members['handle'] in vp_partner:
                            vp_partner[members['handle']]+=1
                        else:
                            vp_partner[members['handle']]=1

        if timetsf(time.localtime(subbmission['creationTimeSeconds']))<earliest_submission_time:
            earliest_submission_time=timetsf(time.localtime(subbmission['creationTimeSeconds']))
            earliest_subbmission_id="CF"+str(subbmission['contestId'])+subbmission['problem']['index']
            earliest_subbmission_title=subbmission['problem']['name']
            full_earliest_submission_time=time.localtime(subbmission['creationTimeSeconds'])

        if timetsf(time.localtime(subbmission['creationTimeSeconds']))>latest_submission_time:
            latest_submission_time=timetsf(time.localtime(subbmission['creationTimeSeconds']))
            latest_subbmission_id="CF"+str(subbmission['contestId'])+subbmission['problem']['index']
            latest_subbmission_title=subbmission['problem']['name']
            full_latest_submission_time=time.localtime(subbmission['creationTimeSeconds'])

        if subbmission['verdict']!="OK":
            if subbmission['problem']['name'] in wa_cnt:
                wa_cnt[subbmission['problem']['name']]+=1
            else:
                wa_cnt[subbmission['problem']['name']]=1
            if wa_cnt[subbmission['problem']['name']]>wa_max_cnt:
                wa_max_cnt=wa_cnt[subbmission['problem']['name']]
                wa_max_id="CF"+str(subbmission['contestId'])+subbmission['problem']['index']
                wa_max_title=subbmission['problem']['name']

            if subbmission['problem']['name'] not in question_wa_time:
                question_wa_time[subbmission['problem']['name']]=time.localtime(subbmission['creationTimeSeconds'])
            else:
                question_wa_time[subbmission['problem']['name']]=min(question_wa_time[subbmission['problem']['name']],time.localtime(subbmission['creationTimeSeconds']))

        else :
            if subbmission['problem']['name'] not in question_ac_time:
                question_ac_time[subbmission['problem']['name']]=time.localtime(subbmission['creationTimeSeconds'])
            else:
                question_ac_time[subbmission['problem']['name']]=min(question_ac_time[subbmission['problem']['name']],time.localtime(subbmission['creationTimeSeconds']))        

    for key in question_ac_time:
        if key not in question_wa_time:
            dont_miss_ac_cnt+=1

    longest_time_title="";longest_time=0
    for key in question_ac_time:
        if key in question_wa_time:
            ac_time_seconds = time.mktime(question_ac_time[key])
            wa_time_seconds = time.mktime(question_wa_time[key])
            if ac_time_seconds > wa_time_seconds:
                if ac_time_seconds - wa_time_seconds > longest_time:
                    longest_time = ac_time_seconds - wa_time_seconds
                    longest_time_title = key

    url="https://codeforces.com/api/user.info?handles="+id
    response=requests.get(url)
    data=response.json()
    if data['status']!="OK":
        return "找不到这个用户"
    registrationTimeSeconds=data['result'][0]['registrationTimeSeconds']

    ret=id+"同学，你在"+time.strftime("%Y-%m-%d", time.localtime(registrationTimeSeconds))+"加入了Codeforces\n"

    org_improvement=['Swan416','Jayket','jxjxjx','gche','CatBiscuit','Krebet','jiejiejiang',
                'xyktyjayket','kylin370','Dream_M','SHIZHEYANGDE','tootwp']
    doi_silent=['oval_m','evilboy_','Slowly','evilb0y_']
    more_sleep=['RFDd','W.Sherlock.Henry','Lincians','Kay_kit']
    if id in org_improvement:
        ret += "2024的你比起提升自己，更乐意监督队友\n"
    elif id in doi_silent:
        ret += "2024的你仍然坚持偷情\n"
    elif id in more_sleep:
        ret += "2024又加睡了一整年\n"
    else:
        ret += "2024年对你来说也是提升自己的一年\n"

    ret+=time.strftime("%m月%d日%H:%M:%S", first_question_time)+"，你进行了2024年的第一次提交，剑指"+first_question_id+"\n"
    ret+="在此之后，你在2024一共进行了"+str(submission_cnt)+"次提交，每一次提交都可能返回令人意外的结果\n\n"

    if vp_cnt==0:
        ret+="不过你在2024年没有打过vp，是不是有点太摆了？\n"
    elif vp_cnt<10:
        ret+="在vp一途，你小试牛刀，好像感受到了那么一点点实际比赛的感觉？\n"
    else:
        ret+="而且你还打了不少vp吼，我愿称你为加训狂魔！\n"

    if vp_cnt>0:
        ret+="今年你一共打了"+str(vp_cnt)+"场vp，"

    if vp_partner == {}:
        ret+="一直坚持单打独斗，强者的世界想来总是孤独的\n"
    else:
        ret+="和"+max(vp_partner,key=vp_partner.get)+"关系一定很好吧，你们一起打了"+str(vp_partner[max(vp_partner,key=vp_partner.get)])+"场vp\n"
        ret+="也有一些不那么熟的，特别是"+min(vp_partner,key=vp_partner.get)+"，你们一起打了"+str(vp_partner[min(vp_partner,key=vp_partner.get)])+"场vp，2025年也要多联络联络感情\n"

    ret+="\n学习的过程中也不总是一帆风顺，总是过不了还是相当让人红温的\n"
    ret+="我猜你的年度红温题可能是"+wa_max_id+"，交了"+str(wa_max_cnt)+"次还是没有过，可能这个名字"+wa_max_title+"已经深深印在你的脑海里了\n"
    ret+="当然有时可能换个思路又是海阔天空，提升一下自己再补题可能会让你感到豁然开朗\n"

    ret+="最长的一个首wa到ac是"+longest_time_title+"，历经"+str(longest_time//86400)+"天"+str(longest_time%86400//3600)+"小时"+str(longest_time%3600//60)+"分钟"+str(longest_time%60)+"秒，"
    if longest_time<86400:
        ret+="有题从不留到第二天，你就是补题仙人吧！\n"
    else:
        ret+="真的是意志坚定，多久了还惦记着这一道题呢！\n"

    ret+="这些题ac的那一瞬间你肯定很开心，当然更让人心情舒爽的还得是一遍过，你今年这样爽了"+str(dont_miss_ac_cnt)+"次"

    if dont_miss_ac_cnt==0:
        ret+="，你的一遍过之路还很长，加油！\n"
    elif dont_miss_ac_cnt<10:
        ret+="，说不定现在你都还能想起每道题ac的瞬间\n"
    elif dont_miss_ac_cnt<100:
        ret+="，看来你是试错型选手\n"
    else:
        ret+="，真是不得了的成就！\n"

    ret+="\n披星戴月地做题生涯中，你的作息也不见得那么正常\n"
    ret+=time.strftime("%m月%d日%H:%M:%S", full_earliest_submission_time)+"队友还在梦中，你向着"+earliest_subbmission_id+"进行了清晨第一发提交\n"
    ret+=time.strftime("%m月%d日%H:%M:%S", full_latest_submission_time)+"你还在为"+latest_subbmission_id+"苦苦思索，可能写不出这题很难睡着吧\n"

    ret+="\n最后，2024年对你来说是一个怎样的一年呢？\n"
    ret+="想来你自己也有很多的想法，不管怎么样，2025年也要继续加油哦！我们明年年底再见！\n"

    return ret


if __name__ == '__main__':
    print(get_sum_2024('CatBiscuit'))