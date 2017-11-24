# zicada
Reptile script recording（爬虫规则录制）
Zicada系统最基本的功能就是录制爬虫抓取的页面规则。将抓取规则划分为登录页、列表页、详情页以及翻页，自由定制。 
Zicada系统分为本地模式和远程模式。

Zicada系统的exe免安装文件：百度云http://pan.baidu.com/s/1boKgVs7 密码7ekw

本地模式： 在文件的根目录下有一个zicada.exe文件，双击，默认账号/密码：admin/admin123 进入系统后，可为你的URL创建任务，录制的时候，先要选择抓取的环节，Ctrl+鼠标左键，即可录制web页面中的元素。 当单击无法打开页面链接的时候，Alt+鼠标左键，即可打开页面元素的链接。 点击完成即可将录制的脚本保存到本地sqlite3数据库。

远程模式： 远程模式除了需要客户端之外，还需要一个服务端 服务端的jar包：http://pan.baidu.com/s/1bp32kaz mweo，
sql:http://pan.baidu.com/s/1nuDaUdN kvs5,
需要修改数据库配置 远程模式需要在本地模式下进行配置远程服务端的信息，退出后，再以远程身份登录 默认的远程客户端的账号/密码:admin/admin123 远程模式最大的好处在于，将录制的脚本信息同步到远程的MySQL数据库

使用者可以自行处理这些录制的脚本，比如爬虫等。 欢迎交流QQ：1876780790
