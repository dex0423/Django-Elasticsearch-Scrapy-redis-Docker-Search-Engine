
项目简述：

	- 基于 django + scrapy-redis + elasticsearch + docker 搭建分布式搜索引擎。


功能描述：

	- 利用 scrapy-redis 抓取网页，此处的抓取对象为六安市房产数据 http://fcj.luan.gov.cn/laweb/Web/PreSellInfo/ShowPreSellCertList.aspx；

	- 利用 elasticsearch 存储抓取的数据，同事存储于 MySQL 实现持久化；

	- 利用 django 搭建数据搜索界面；

	- 实现 docker 容器化部署；

	- 实现分布式部署；

