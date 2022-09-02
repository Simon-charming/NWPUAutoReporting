# -*- encoding:utf-8 -*-

import requests
import json


class SendMessage():
    def __init__(self, appID, appSecret, open_id):
        self.appID = appID # 'wx57596acab238197b'
        self.appsecret = appSecret # 'ea93e53e139da2696be0d02a41e855ba'
        self.access_token = self.get_access_token()
        self.open_id = open_id

    def get_access_token(self):
        """
        获取微信公众号的access_token值
        """
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.\
            format(self.appID, self.appsecret)
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
        }
        response = requests.get(url, headers=headers).json()
        print("response:%s" % response)
        access_token = response.get('access_token')
        print("token:%s" % access_token)
        return access_token

    # def get_openid(self):
    #     """
    #     获取所有粉丝的openid
    #     """
    #     next_openid = 'oOuS7542y02BQDPFa3zvdwqiMctk'
    #     url_openid = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (self.access_token, next_openid)
    #     ans = requests.get(url_openid)
    #     print("ans:%s" % ans.content)
    #     openID = json.loads(ans.content)['openid']
    #     return openID

    def send_message(self, msg):
        """
        给所有粉丝发送文本消息
        """
        url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={}".format(self.access_token)
        print(url)
        if self.open_id != '':
            body = {
                "touser": self.open_id,
                "msgtype":"text",
                "text":
                {
                    "content": msg
                }
            }
            data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))
            print(data)
            response = requests.post(url, data=data)
            # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
            result = response.json()
            print(result)
        else:
            print("当前没有用户关注该公众号！")

    def upload_media(self, media_type, media_path):
        """
        上传临时文件到微信服务器，并获取该文件到meida_id
        """
        url = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}'.format(self.access_token, media_type)
        print(url)
        meida = {
            'media': open(media_path, 'rb')
        }
        rsponse = requests.post(url, files=meida)
        parse_json = json.loads(rsponse.content.decode())
        print(parse_json)
        return parse_json.get('media_id')

    def send_media(self, media_type, media_path):
        """
        给所有粉丝发送媒体文件，媒体文件以meida_id表示
        """
        media_id = self.upload_media(media_type, media_path)
        url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={}'.format(self.access_token)
        if self.open_id != '':
            if media_type == "image":
                body = {
                    "touser": self.open_id,
                    "msgtype": "image",
                    "image":
                        {
                            "media_id": media_id
                        }
                }
            if media_type == "voice":
                body = {
                    "touser": self.open_id,
                    "msgtype": "voice",
                    "voice":
                        {
                            "media_id": media_id
                        }
                }
            data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))
            print(data)
            response = requests.post(url, data=data)
            # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
            result = response.json()
            print(result)
        else:
            print("当前没有用户关注该公众号！")


if __name__ == "__main__":
    data = '送你一张美图'
    # shr:oOuS7542y02BQDPFa3zvdwqiMctk  smr:oOuS752jGRwI9CgziqbG5fB6ooCM    hxy:oOuS759GdF3Ob3QUdvCHGb9PXavo    qty:oOuS751w8gIa-do8oLtLMkTDPEB0
    # sends = SendMessage(appID='wx57596acab238197b', appSecret='ea93e53e139da2696be0d02a41e855ba', openID='oOuS7542y02BQDPFa3zvdwqiMctk')
    sends = SendMessage(appID='wx57596acab238197b', appSecret='ea93e53e139da2696be0d02a41e855ba',openID='oOuS751w8gIa-do8oLtLMkTDPEB0')
    sends.send_message(data)
    sends.send_media("image", './test.jpg')
