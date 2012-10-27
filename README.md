Author : tntCastle

这个脚本需要安装BeautifulSoup 4以及chardet。

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
