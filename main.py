import itchat, time
from itchat.content import *
import Getcodeforces
import ImageRenderer
import GetCFContest
import CFRatingDrawer
import CFUnsolved
import GetAtcContest
import AtcRatingDrawer
import CFAnalysis
import Sum2024


flag = 1
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    global flag
    msg.user.send('%s: %s' % (msg.type, msg.text))
    if msg.text.startswith('#stop'):
        password = msg.text[5:].split()[0]
        if password=="0d000721":
            msg.user.send(f'will stop password: {password}')
            flag = 0
        else:
            msg.user.send(f'error stop password {password}')
    elif msg.text.startswith('#start'):
        password = msg.text[6:].split()[0]
        if password=="0d000721":
            msg.user.send(f'will start password: {password}')
            flag = 1
        else:
            msg.user.send(f'error start password {password}')
    elif msg.text.startswith('#exit'):
        password = msg.text[5:].split()[0]
        if password=="0d000721":
            msg.user.send(f'will EXIT password: {password}')
            itchat.logout()
        else:
            msg.user.send(f'error EXIT password {password}')


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
def group_text_reply(msg):
    global flag
    if flag:
        if msg.text.startswith('#sum'):
            Username = msg.text[5:].split()
            if(Username[0]==''):
                msg['User'].send("不给名字我搜个锤子")
            else:
                ret = Sum2024.get_sum_2024(Username[0])
                msg['User'].send(ret)
        elif msg.text.startswith('#cfrating'):
            Username = msg.text[9:].split()
            if(Username[0]==''):
                msg['User'].send("不给名字我搜个锤子")
            else:
                img = CFRatingDrawer.get_img(Username[0])
                if img==None:
                    msg['User'].send(f"苦呀西 找不到{Username[0]} qwq~")
                else:
                    msg['User'].send_image(img)
        elif msg.text.startswith('#atcrating'):
            Username = msg.text[10:].split()
            if(Username[0]==''):
                msg['User'].send("不给名字我搜个锤子")
            else:
                img = AtcRatingDrawer.AtcRatingDrawer(Username[0])
                if img==None:
                    msg['User'].send(f"苦呀西 找不到{Username[0]} qwq~")
                else:
                    msg['User'].send_file(img)
        elif msg.text.startswith('#cfanalysis'):
            Username = msg.text[11:].split()
            if(Username[0]==''):
                msg['User'].send("不给名字我搜个锤子")
            else:
                # 如果后面出现空格，说明是要查看具体的语言或者tag
                if len(Username) > 1:
                    if Username[1] == 'lang':
                        ret = CFAnalysis.CFLangDraw(Username[0])
                        msg['User'].send_image(ret)
                    elif Username[1] == 'tag':
                        ret = CFAnalysis.CFTagDraw(Username[0])
                        msg['User'].send_image(ret)
                    elif Username[1] == 'null':
                        ret = CFAnalysis.CFAnalysis(Username[0])
                        msg['User'].send(ret)
                    else:
                        ret = "杂鱼输错啦~输入#cfanalysis {id} lang/tag/null的话也不是不能给你看一眼喔~"
                else:
                    ret = CFAnalysis.CFAnalysis(Username[0])
                    msg['User'].send(ret)
        elif msg.text.startswith('#cf'):
            Username = msg.text[3:].split()
            img = ImageRenderer.get_img(Username[0])
            if img==None:
                msg['User'].send(f"苦呀西 找不到{Username[0]} qwq~")
            else:
                msg['User'].send_image(img)
        elif msg.text.startswith("#at"):
            msg['User'].send("TODO")
        elif msg.text.startswith('#近期比赛'):
            Resource_name = msg.text[5:].split()
            if(Resource_name[0]=='Codeforces' or Resource_name[0]=='cf' or Resource_name[0]=='codeforces'):
                back=GetCFContest.getCF_Contest()
                msg['User'].send(back)
            elif(Resource_name[0]=='AtCoder' or Resource_name[0]=='atc' or Resource_name[0]=='atcoder' or 
                 Resource_name[0]=='Atcoder' or Resource_name[0]=='atCoder'):
                back=GetAtcContest.GetAtcContest()
                msg['User'].send(back)
            else:
                msg['User'].send("TODO")
        elif msg.text.startswith('#补题'):
            id = msg.text[3:].split()
            if(id[0]==''):
                msg['User'].send("不给id我搜个锤子")
            else:
                back=CFUnsolved.get_unsolved(id[0])
                msg['User'].send(back)

        elif msg.text.startswith('看看腿'):
            msg['User'].send("下头！")

        elif msg.text.startswith('#help'):
            msg['User'].send("1. #cf Userid 查看cf信息\n"
                             "2. #at Userid 查看atcoder信息\n"
                             "3. #cfrating Userid 查看cf rating\n"
                             "4. #atcrating Userid 查看atcoder rating\n"
                             "5. #近期比赛 Resourceid 查看近期的比赛\n"
                             "6. #补题 Userid 查看未完成的题目\n"
                             "7. #cfanalysis Userid lang/tag/null 查看cf分析\n"
                             "8. #help帮助菜单\n"
                             "[限时] #Sum Userid 查看Codeforces2024年终总结\n"
                             "灌注哈基幂谢谢喵~\n")


# itchat.auto_login(hotReload=True)
itchat.auto_login()
itchat.run(True)
