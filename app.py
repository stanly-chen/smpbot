from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)
import requests

import os

app = Flask(__name__)

# 填入你的 message api 資訊
line_bot_api = LineBotApi(
    'SRUcrtdO+7KHgmCOyyuVhJqDHI1BID+W3lyUaxrBZKF7PZ8MxeRNU1m7b2/CqyYwUDgZuj9QKF5KIbKTz+5BDy811+w4W9gBb/sdqbgfnWoC7o8S2MsqDajt6m38Aamx0S2ToSf+C8GD3pf2bn8wDgdB04t89/1O/w1cDnyilFU='
)
handler = WebhookHandler('495192b49d94de1ef72da683cd3cf3f4')


# 設定你接收訊息的網址，如 https://YOURAPP.herokuapp.com/callback
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    content = "{}: {}".format(event.source.user_id, event.message.text)
    profile = line_bot_api.get_profile(event.source.user_id)
    text = event.message.text
    userName = str(profile.display_name)
    userStatus = str(profile.status_message)

    if text.lower() == 'me':
        content = str(event.source.user_id) + '_' + userName + '_' + userStatus
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=content))
    elif "電視盒" in text:
        content = '正為您按下電視盒開關'
        param = {'tv': '1Y1', 'tvNum': "pw"}
        requests.get(
            'http://vanlenth6.ddns.net:8080/stanly/tvAction!setJs.action',
            params=param)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=content))
    elif "開鎖" in text:
        content = '正為您開鎖'
        param = {'relay': "0"}
        requests.get(
            'http://vanlenth6.ddns.net:8080/stanly/tvAction!setJs.action',
            params=param)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=content))
    elif "Discovery" in text:
        content = '正為您轉至Discovery'
        param = {'tv': '1Y1', 'tvNum': "19"}
        requests.get(
            'http://vanlenth6.ddns.net:8080/stanly/tvAction!setJs.action',
            params=param)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=content))
    elif text.isdigit():
        if len(text) < 4:
            content = '正為您轉台，請靜候10秒'
            param = {'tv': '1Y1', 'tvNum': text}
            requests.get(
                'http://vanlenth6.ddns.net:8080/stanly/tvAction!setJs.action',
                params=param)
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text=content))
        else:
            content = '請輸入最高兩位的數字'
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text=content))
    elif text.lower() == 'open':
        content = '已為您啟動'
        param = {'temp': '1', 'wet': '1000'}
        requests.get('https://dweet.io/dweet/for/stanlykuasled', params=param)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=content))
    elif "煮水" in text:
        content = '已為您將水煮至你要的溫度'
        param = {'temp': '0', 'water': '1Y1', 'wm': '0'}
        requests.get('https://dweet.io/dweet/for/stanlykuasled', params=param)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=content))
    elif "關燈" in text:
        content = '已為您關閉電燈'
        param = {'temp': '0', 'water': '1Y1', 'wm': '0'}
        requests.get('https://dweet.io/dweet/for/stanlykuasled', params=param)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=content))
    elif "開燈" in text:
        content = '已為您開啟電燈'
        param = {'temp': '0', 'water': '1Y1', 'wm': '0'}
        requests.get('https://dweet.io/dweet/for/stanlykuasled', params=param)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=content))
    # elif "電視" in text:
    #     content = '已發送電視遙控器訊號'
    #     param = {'temp': '0', 'tv': '1Y1', 'wm': '0'}
    #     requests.get('https://dweet.io/dweet/for/stanlykuasled2', params=param)
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=content)
    #         )
    elif "房間" in text:
        content = '已將您的頻道切換至房間'
        param = {'mychannel': 'R'}
        requests.get(
            'http://vanlenth6.ddns.net:8080/stanly/stanly/tvAction!openTv.action',
            params=param)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=content))
    elif "節目" in text:
        content = '已將您的頻道切換至電視節目'
        param = {'mychannel': 'T'}
        requests.get(
            'http://vanlenth6.ddns.net:8080/stanly/stanly/tvAction!openTv.action',
            params=param)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=content))
    elif "監視器" in text:
        content = '已將您的頻道切換至監視器'
        param = {'mychannel': 'C'}
        requests.get(
            'http://vanlenth6.ddns.net:8080/stanly/stanly/tvAction!toRoom.action',
            params=param)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=content))
    elif "電視" in text:
        content = '已將您的頻道切換至電視'
        param = {'mychannel': 'A'}
        requests.get(
            'http://vanlenth6.ddns.net:8080/stanly/stanly/tvAction!toTv.action',
            params=param)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=content))
    elif "開電腦" in text:
        content = '已將您按下電腦電源'
        param = {'computer': 'Y'}
        requests.get('https://dweet.io/dweet/for/stanlyHomeCtrl704',
                     params=param)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=content))
    elif "關電腦" in text:
        content = '已將您按下電腦電源'
        param = {'computer': 'R'}
        requests.get('https://dweet.io/dweet/for/stanlyHomeCtrl704',
                     params=param)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text=content))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ['PORT'])