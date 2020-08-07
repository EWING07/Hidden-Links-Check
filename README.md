# Hidden-Links-Check

script for checking some types pf hidden links

语言：python3.x

所需模块：re, urllib, tld, selenium, os

输入：txt文件输入，一行一个待检测的url。

输出：如果存在暗链，则进行txt文件输出，每一个被检测的url对应一个输出文件，输出文件中包含url页面中检测出来的暗链url。

目前可检测的暗链类型：
1.	字体大小太小
2.	CSS样式当中，visibility: hidden
3.	CSS样式中，display: none
4.	链接颜色与背景色相同，链接文字使用低像素。
5.	利用跑马灯marquee属性，链接以跑马灯形式迅速闪现，跑马灯的长宽设置很小，同时将闪现的频率设置很大，使得查看页面时不会有任何影响
6.	利用iframe创建隐藏的内联框架
7.	利用标签meta插入链接。位于网页html源码头部内的标签，提供有关页面的元信息，是搜索引擎判定网页内容的主要根据, 攻击者可以在标签中插入大量与网页不相关的词语以及链接
8.	利用elenium库中Is_displayed()函数可以检测出大多页面可见范围之外以及通过js写入css样式导致不可见的暗链。


备注：
需要下载chrome使用其headless模式以及对应版本的chromedriver 
附：chromedriver下载网站https://chromedriver.chromium.org/downloads

