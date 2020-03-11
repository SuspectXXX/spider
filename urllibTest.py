# 导入urllib.request库
import urllib.request
import urllib.parse
import urllib.error
# 导入cookieJar库
from http import cookiejar

# urlopen()函数接受3个参数，分别是url, data, timeout
# 3个参数分别代表爬虫请求的url，要传递的数据，设置超时时间
# 单独打印response返回对一个对象的描述，加read()才能读出网页内容
response = urllib.request.urlopen("https://www.baidu.com/")
print(response.read())

# 演示data参数的作用
# 模拟登录，来演示data参数的作用
# 实际登录比较复杂，此处只是演示
# POST提交方式
# values = {"username": "13262639708", "password": "yuan199638"}
# data = urllib.parse.urlencode(values)
# url = "https://accounts.douban.com/login"
# response = urllib.request.urlopen(url, data)
# print(response.read())

# GET提交方式
# 直接构造一个带参数的url即可
# values = {"username": "13262639708", "password": "yuan199638"}
# data = urllib.parse.urlencode(values)
# url = "https://accounts.douban.com/login"
# getUrl = url + "?" + data
# response = urllib.request.urlopen(getUrl)
# print(getUrl)

# 加入Headers,这里模拟登录知乎能够成功
url = "https://www.zhihu.com/signin?next=%2F"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
values = {"username": "18336150565", "password": "yuan199638"}
data = urllib.parse.urlencode(values).encode('utf-8')
# 对付反盗链
refer = "https://www.zhihu.com/signin?next=%2F"
headers = {'User-Agent': user_agent, "Refer": refer}
# 此处需留意
req = urllib.request.Request(url, data, headers=headers)
response = urllib.request.urlopen(req)
print(response.read())

# URLError异常处理
# 产生原因
# 1 网络无连接，即本机无法上网
# 2 连接不到特定的服务器
# 3 服务器不存在
# 需要导入urllib.error库，该库有两个方法HTTPError和URLError
# URLError只有reason，HTTPError还有code，且HTTPError是URLError的子类
req = urllib.request.Request("http://www.blog.csdn.net/cqcre")
try:
    response = urllib.request.urlopen(req)
except urllib.error.HTTPError as e:
    print(e.reason)
    print(e.code)
except urllib.error.URLError as e:
    print(e.reason)

# 使用Cookie
# 为何使用cookie？
# Cookie指某些网站为了辨别用户、进行session跟踪而存储在用户本地终端上的数据（通常经过加密）
# 比如说有些网站需要登陆后才能访问某个页面，在登录之前，向抓取某个页面是不允许的。则可以利用我们保存的cookie，来抓取其他页面
# Opener
# 当获取一个URL时，使用一个opener(一个urllib.request.OpenerDirector的实例)，前面使用的urlopen就是默认的opener
# 当需要用到Cookie时，需要创建一个更一般的opener来实现对cookie的设置
# 声明一个cookieJar对象来保存cookie
cookie = cookiejar.CookieJar()
# 利用urllib.request库的HTTPCookieProcessor来创建cookie容器
handler = urllib.request.HTTPCookieProcessor(cookie)
# 通过handler来创建opener
opener = urllib.request.build_opener(handler)
# 此处使用open方法打开网页
response = opener.open("https://www.baidu.com")
for item in cookie:
    print("Name = " + item.name)
    print("Value = " + item.value)

# 保存cookie到文件
# 设置cookie保存到目录
filename = "cookie.txt"
# 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookiejar.MozillaCookieJar(filename)
# 利用urllib.request库的HTTPCookieProcessor对象来创建cookie容器
handler = urllib.request.HTTPCookieProcessor(cookie)
# 通过handler来创建opener
opener = urllib.request.build_opener(handler)
# 创建一个请求
response = opener.open("https://www.baidu.com")
# 保存cookie到文件
cookie.save(ignore_discard=True, ignore_expires=True)

# 从文件中读取Cookie并访问
# 创建一个MozillaCookieJar对象实例
cookie = cookiejar.MozillaCookieJar()
# 读取已经保存的cookie
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
# 创建请求的request
req = urllib.request.Request("https://www.baidu.com")
# 创建一个opener
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
response = opener.open(req)
print(response.read())

# 利用cookie模拟网站登录,这里科恩那个是因为校外无法访问，失败了

filename = "cookie.txt"
cookie = cookiejar.MozillaCookieJar(filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
data = urllib.parse.urlencode({"username": "192570484", "password": "Yuan199638"}).encode('utf-8')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.66'
headers = {'User-Agent': user_agent}
loginUrl = "http://yjsxt.usst.edu.cn/epstar/login/index.jsp"
req = urllib.request.Request(loginUrl, data, headers)
response = opener.open(req)
cookie.save(ignore_discard=True, ignore_expires=True)
gradeUrl = "http://yjsxt.usst.edu.cn/epstar/web/swms/mainframe/home/index.jsp"
req = urllib.request.Request(gradeUrl, headers=headers)
response = opener.open(req)
print(response.read().decode())