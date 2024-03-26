# Cdomain
python简单实现C段扫描，以及ip反查
实现ip反查接口来自https://ipchaxun.com/
实现C段扫描接口来自https://chapangzhan.com/

使用方式：
C段扫描：python Cdomain.py -c ip
单ip反查域名：python Cdomain.py -d ip
导入txt批量查域名，导入到ip_domains.txt：python Cdomain.py -l test.txt
所有C段反查域名，并导出为到domains.txt：python Cdomain.py -all ip

实现过程中遇到的问题:
1.对https网址访问，会报警，一大串影响观感的字段，使用了verify=False，但没用，没解决，所以我将输出导入到txt文件中
2.requests.exceptions.ConnectionError: HTTPConnectionPool(host='sewer.ip138.com', port=80):即添加ua头部即可，解决方案来自：https://www.cnblogs.com/tingtin/p/12907309.html

注意，c段扫描没有剔除掉原ip
