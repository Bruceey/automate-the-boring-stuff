## 1、创建scrapy模板命令

```cmd
(1) scrapy startproject 项目名
(2) cd 项目名
    scrapy genspider 爬虫文件名字 起始请求url(一般写域名)
```

**注意：项目名和爬虫名要不一样.**

*举例：以下内容皆以此为例*

*项目名为 "netbian", 爬虫文件名为 "bian", 起始请求url为 "http://www.netbian.com/"*

```cmd
(1) scrapy startproject netbian
(2) cd netbian
    scrapy genspider bian netbian.com
```



## 2、项目层次结构

![](C:\Users\17634\Desktop\案例\笔记\scrapy架构.png)

```
bian.py 		#爬虫文件，核心代码文件。编写提取数据的代码，会用到xpath、css、re正则来提取数据
items.py        #里面有一个item类，item类内部定义数据每个字段名字。爬虫文件会提供每个字段的内容，进而构造一个对象
middlewares.py  #针对反爬虫使用、异常处理
pipelines.py    #接受item类对象，如何将数据保存
settings.py     #全局的设置，比如设置并发量等
```





## 3、Spiders(爬虫文件)

```python
#(1) 是由scrapy genspider bian netbian.com命令创建的py文件，里面有一个爬虫类(继承scrapy的Spider类)

#(2)代码结构
class BianSpider(scrapy.Spider):
    name = 'bian'   #爬虫类的名字(ID)，启动爬虫时需要用到
    #允许爬虫爬取的域名，举例：彼岸的图片地址在阿里云存储上，此时爬虫就无法爬取。初学时建议注释掉
    allowed_domains = ['netbian.com']  #允许爬取的域名
    start_urls = ['http://netbian.com/'] #爬虫启动后首先开始从哪个url抓取数据 

    def parse(self, response): #提取数据的函数,response即是请求上方start_urls得到的响应
        pass
```

**注意：**

(1) `name = 'bian'`，启动爬虫命令`scrapy crawl bian`

(2) 如果设置 `allowed_domains = ['netbian.com']`，举例：彼岸的图片地址在阿里云存储上，此时爬虫就无法爬取。初学时建议注释掉。

(3)爬虫从`start_urls`中返回response，之后交给`self.parse`函数，该函数用来详细提取数据。

(4)`self.parse`函数是默认提取数据的函数，如果在提取过程中构建新的request请求，并且不指定新的回调函数，则默认将响应体response传给该函数解析。



## 4、Selectors(提取数据的选择器)

```python
利用response提取数据的几种方法
(a)response.css('.list li a::attr(href)').extract()
   .list li a这一部分是css选择器，::attr(href)是获取a标签的href属性，是固定写法；如何想获取文本内容，则用::text(如.list li a::text)
                    
(b)response.xpath('//div[@class="list"]//li//a/@href').extract()
contains(属性, 内容)
如: //a[contains(@href,"file")]   //筛选href属性值包含file的a标签
   //a[contains(text(),"下一页")]  //筛选文本值包含下一页的a标签，其中text()可以用"."代替

(c) extract()  ==   getall()   获取所有满足的内容，返回列表
	extract_first() == get()   获取第一个满足的内容，返回一个
	re(正则语句)		再次利用正则进行筛选，返回列表；常用于对文本内容的筛选
	re_first(正则语句)  返回第一个
	注意：(1)对于正则语句，如果正则里面没有分组括号，则直接返回全匹配；有分组括号，返回分组的正则匹配内容;
	     (2)以上提取函数如果实际为空，则直接返回None，不会报错
```

**注意：**

```python
# xpath()和css()返回的依然是选择器，可继续利用选择器表达式进行提取
a = response.css('.list')
lis = a.css('a::attr(href)').extract()
```



## 5、Scrapy shell(验证提取的数据是否正确)

```python
#(1)需要在当前项目路径下打开终端，输入scrapy shell http://www.netbian.com/meinv/

#(2)此时自动生成了response参数和fetch()函数，
# 利用response.css('.list li a::attr(href)').extract()即可检验提取数据;
# 更换页面url检查数据,即可用fetch(新的url)，之后可再次利用response参数检查数据
```



## 6、Requests and Responses(请求和响应)

```python
# 1. Request
# url链接，callback指定得到url响应体后交给哪个函数来处理
scrapy.Request(url, callback=self.parse_image_url)

# 2. Response
# (a)利用response.css().extract()来提取数据
# (b)response.urljoin(url)拼接完整的url

# 3. meta参数: 页面间传递数据
#如当前页面有产品的简略信息，进入详情页面后发现个别信息没有，但这些信息出现在之前的简略信息的页面上。
scrapy.Request(url, callback=self.parse_image_url, meta={"发布时间": "2016年9月"})

然后在self.parse_image_url方法中即可利用response参数提取出来
pub_time = response.meta["发布时间"]
```



## 7、Items(将商品的每个关键字字段封装成一个Item类)

```python
class NetbianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    filename = scrapy.Field()
    image_bytes = scrapy.Field()
# 该类会被爬虫文件使用，爬虫文件利用提取的数据构造该类的实例对象
```



## 8、Item Pipeline(管道，定义如何存储数据)

比如说将数据存到本地、mysql、mongodb、云服务器，以及存取什么样的格式。

```python
import os

image_store = r"D:\Users\Pictures\bian1"
os.makedirs(image_store, exist_ok=True)

class NetbianPipeline:
    # item是上方讲的Item类的实例对象(里面已经封装好了一条商品的完整数据)
    def process_item(self, item, spider): 
        filename = item['filename']
        image_bytes = item['image_bytes']
        with open(os.path.join(image_store, filename), 'wb') as f:
            f.write(image_bytes)
        return item
```

**注意:**  在该文件内可同时定义多个Pipeline类，即将此商品数据同时保存到不同的地方；另外，在`settings.py`文件中要将相应设置打开。



## 9、Settings(项目全局设置)

```python
#(1)将遵守机器人协议改为False
ROBOTSTXT_OBEY = True     #原始
ROBOTSTXT_OBEY = False    #修改后

#(2)设置请求并发量，默认是16(即每秒发送16个请求)
#CONCURRENT_REQUESTS = 32 #原始
CONCURRENT_REQUESTS = 4   #修改后

# 设置下载延迟(默认没有下载延迟)
DOWNLOAD_DELAY = 0.2

#####举例:############
CONCURRENT_REQUESTS =2
DOWNLOAD_DELAY =5
效果：一开始来2个request（A，B），但5秒后只处理了一个request(A)，新来一个request(C),5秒后又处理一个request（B）,排队一个request（D）。如此循环。
######################

#(3)设置请求头
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#} #原始

DEFAULT_REQUEST_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}  #修改后

#(4)将item_pipelines开关打开
#ITEM_PIPELINES = {
#    'netbian.pipelines.NetbianPipeline': 300,
#}  #原始

ITEM_PIPELINES = {
   'netbian.pipelines.NetbianPipeline': 300,
}   #修改后                                   
```



## 10、启动爬虫

#### 方式一：

```
在当前项目路径下打开命令行，scrapy crawl 爬虫名
			      (如： scrapy crawl bian)
```

#### 方式二：

或者在项目下新建一个启动文件(如start.py)

```python
from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute("scrapy crawl bian".split())
```



## 11、scrapy专门处理文件和图片的技术