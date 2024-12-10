import itchat, time
from itchat.content import *
import Getcodeforces
import ImageRenderer
import GetCFContest
import CFRatingDrawer
import CFUnsolved
import GetAtcContest


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
        if msg.text.startswith('#cfrating'):
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
            msg['User'].send("TODO")
        elif msg.text.startswith('#cf'):
            # 提取'#cf'之后的内容作为命令
            Username = msg.text[3:].split()
            # 根据命令执行相应的操作
            # 这里只是一个示例，您可以根据需要添加具体的逻辑
            # response = f"渲染器(TODO)\n coderforce id: {Username[0]} rate:{Getcodeforces.get_rate(Username[0])} \n这么菜真是杂鱼呢喵~"
            # 回复消息到群聊
            img = ImageRenderer.get_img(Username[0])
            if img==None:
                msg['User'].send(f"苦呀西 找不到{Username[0]} qwq~")
            else:
                msg['User'].send_image(img)
        elif msg.text.startswith("#at"):
            msg['User'].send("TODO")
        elif msg.text.startswith('#近期比赛'):
            Resource_name = msg.text[5:].split()
            if(Resource_name[0]=='Codeforces' or Resource_name[0]=='cf'):
                back=GetCFContest.getCF_Contest()
                msg['User'].send(back)
            elif(Resource_name[0]=='AtCoder' or Resource_name[0]=='atc'):
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
                             "7. #help帮助菜单\n"
                             "灌注哈基幂谢谢喵~\n")


# itchat.auto_login(hotReload=True)
itchat.auto_login()
itchat.run(True)
