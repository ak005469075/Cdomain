import requests
from lxml import etree
import sys
import ipaddress
import traceback
import random
from requests.packages import urllib3

def uagent():
         USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Opera/8.0 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
    ]
         return random.choice(USER_AGENTS)
def proxy(url):
        

        #ua = {'user-agent':'Mozilla/5.0'}
        ua={'user-agent':'{}'.format(uagent())}
        # 使用本地代理访问特定网址
        proxy = 'http://127.0.0.1:2080'
        # 使用本地代理访问
        urllib3.disable_warnings()
        response = requests.get(url,headers=ua,verify=False,timeout=5,proxies={'http': proxy, 'https': proxy})
         # 如果不使用代理，可以直接使用下面这行代码
        urllib3.disable_warnings()
        #response = requests.get(url,headers=ua,verify=False,timeout=5)
        return response
def output(response,xpath,k=None):
       # 解析HTML内容
            # 使用XPath选择器提取固定内容
            tree = etree.HTML(response.text)
           
            ips=tree.xpath(xpath)
            if ips:
                for ip in ips:
                    print(ip)
                    if k == 1:
                         with open('domains.txt', 'a+') as file:
                                file.write(ip + '\n')
                    elif k==2:
                         with open('ip_domains.txt', 'a+') as file:
                                file.write(ip + '\n')
            else:
                 print("暂无域名")
def output2(response,xpath):
            tree = etree.HTML(response.text)
            ips=tree.xpath(xpath)
            if ips:
                for ip in ips:
                    print("{}的域名".format(ip))
                    C_domains(ip,1)
            else:
                 print("暂无域名")
def C_ips(ip):
    try:
        ip=ipaddress.ip_network(ip, strict=False)
        c_ip = ip.supernet(new_prefix=24)
        url = 'http://chapangzhan.com/'+str(c_ip)
        response=proxy(url)
        if response.status_code == 200:
          #"/html/body/div/div[2]/div/div[1]/div[1]/div/div[2]/table/tbody/tr/td[1]/a/text()"
          xpath='//tr[@class="J_link"]/td/a/text()'
          output(response,xpath)
    except Exception as e:
         print("C段查询异常",traceback.format_exc())

def C_domains(ip,k=None):
        try:
            url = 'https://ipchaxun.com/'+ip
            response=proxy(url)
            if response.status_code == 200:
                #"/html/body/div/div[2]/div/div[1]/div/div/div/div/p/a/text()"
                xpath='//div[@id="J_domain"]/p/a/text()'
                output(response,xpath,k)
        except Exception as e:
            print("ip反查异常",traceback.format_exc())

def C_all_domains(ip):
       try:
            ip=ipaddress.ip_network(ip, strict=False)
            c_ip = ip.supernet(new_prefix=24)
            url = 'http://chapangzhan.com/'+str(c_ip)
            response=proxy(url)
            if response.status_code == 200:
                xpath='//tr[@class="J_link"]/td/a/text()'
                output2(response,xpath)
       except Exception as e:
         print("C段全域名查询异常",traceback.format_exc())

def C_ips_domains(file):
         try:
            with open(file, 'r') as f:
                lines=f.readlines()
                for line in lines:
                     s=line.strip('\n').strip()
                     with open('ip_domains.txt', 'a+') as file:
                                file.write(s + ':\n')
                     C_domains(s,2)
         except Exception as e:
            print("ip反查异常",traceback.format_exc())

def main():
    if len(sys.argv) < 2:
        print("\nCreate by————————yuleiyun\n")
        print("ipC段扫描：-c ip")
        print("单ip反查域名：-d ip")
        print("导入txt批量查域名：-l test.txt")
        print("所有C段反查域名，并导出为文件：-all ip")
    else:   
        if sys.argv[1]=='-c':
            C_ips(sys.argv[2])
        elif sys.argv[1]=='-d':
            C_domains(sys.argv[2])
        elif sys.argv[1]=='-all':
            #先清空txt文件
            with open('domains.txt', 'w+') as file:
                 file.truncate(0)
            C_all_domains(sys.argv[2])
        else:
            with open('ip_domains.txt', 'w+') as file:
                 file.truncate(0)
            C_ips_domains(sys.argv[2])
             
        
if __name__ == "__main__":
    main()