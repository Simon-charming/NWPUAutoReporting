# **西北工业大学自动疫情填报**
## 1、项目简介
通过Github Action定时完成每日疫情填报，目前定时设置在每天6：00，如有需要可以自行修改./github/workflows中的yml文件。填报完成后通过测试公众号发送消息至被设置的微信号上。
## 2、使用说明
### （1）准备工作
建立微信测试公众号。通过该网址建立：[微信公众平台](https://mp.weixin.qq.com/debug/cgi-bin/sandboxinfo?action=showinfo&t=sandbox/index)
建立后往下翻至测试号二维码，需要接受消息的微信号扫码关注。（注：关注后需发一条消息给公众号）
记住该页面的测试号信息appID、appsecret和已经扫码关注的用户微信号。


### （2）必要步骤
点击页面右上角Fork按钮，复制此仓库。

从自己的主页进入复制的仓库，点击上方栏中的`Settings`，侧边栏中找到`Secrets`点击，进入`Actions`页面。

页面右上角`New repository secret`可以新建一个secret（即私密值），项目需要建立以下secret（Name如下，注意大写）：

> APPID ：值为上述准备工作中的appID
> 
> APPSECRET：值为上述准备工作中的appsecret
> 
> OPENID：值为需要发送消息的用户微信号
> 
> USERNAME：学号
> 
> PASSWORD：密码
> 
> PROVINCE：所在省份（需要全称，如新疆维吾尔自治区），不填默认为在学校
> 
> CITY：所在城市（需要全称）
> 
> DISTRICT：所在区县（需要全称）
> 
> DETAILED：如果住在陕西省西安市，需要填写具体地址

设置完点击上方栏中的`code`，点击./github/workflows，编辑yml文件。
在yml文件最下方找到如下代码：

    python ./main.py -u ${{ secrets.USERNAME1 }} -p ${{ secrets.PASSWORD1 }} -pr ${{ secrets.PROVINCE1 }} -c ${{ secrets.CITY1 }} -d ${{ secrets.DISTRICT1 }} -de ${{ secrets.DETAILED1 }} -ai ${{ secrets.APPID }} -as ${{ secrets.APPSECRET }} -o ${{ secrets.OPENID1 }}
   
   删除这段代码，或者在前面加上#注释。
   至此配置完毕，可以尝试在github上运行，如果运行出错可以留言（回复时间不定）。

### （3）配置运行时间
如果想自己设置填报时间，可以在如上的yml文件中找到如下代码自行修改：

    schedule:
    - cron: '0 18 * * *'
第一个0代表的是分钟，第二个18代表的是小时，即`'0 18 * * *'`代表18：00，因为github采取美国时间，所以修改时间需要注意一下。