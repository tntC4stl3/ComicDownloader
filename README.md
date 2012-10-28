Author : tntCastle

这个脚本需要安装BeautifulSoup 4以及chardet。

## 2012.10.28
###修正
>给urlopen打开chapter页面也加上了三次重试的机制，保证能从页面源代码中找出图片地址。
拼出的“http://imgfast.manhua.178.com/h/海贼王 OnePiece/619话/01.jpg”这种有中文的url地址，
不能调用urllib2.quote()进行url编码，需要先将url encode 为 utf8，然后调用urllib2.quote()。
线程数定为了15个。
###问题
>存在下载不完整的图片，数量非常少，还不知道有什么好的解决办法。


## 2012.10.27
>采用别人的建议，用json模块处理了pages字段，增加了下载失败自动重下的机制（三次）。
代解决问题：类似“http://imgfast.manhua.178.com/o/OnePiece/58/One Piece 58_000.jpg”这样的
url无法urlopen，需要找原因。

## 2012.10.20
>增加了Queue和threading来实现多线程，但是有有时候会有文件夹没创建的情况，待研究解决。
增加了对.jpg和.png后缀的判断。

## Beginning
>这个脚本的目的是从 http://manhua.178.com 下载指定漫画。
目前的版本还是单线程的，那个速度，我自己都忍不了，哈哈哈。。。
测试可以下载One Piece的漫画，会自动建立文件夹，并且给图片编号。
后续会慢慢尝试把脚本实现成多线程的，因为还完全没写过多线程的东西。
