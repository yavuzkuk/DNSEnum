import argparse
import dns.resolver
from sites.sites import  CRTsh,Google,Bing,Yandex,Yahoo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def clıInput():
    parser = argparse.ArgumentParser(description="DNS Enumeration")

    parser.add_argument("-u","--url",type=str,help="Url for scanning",required=bool)
    parser.add_argument("-o","--output",help="Output file name",type=str)
    args = parser.parse_args()

    return args.url,args.output


def DNSRecord(url):
    records = ["A", "MX", "NS", "AAAA", "CNAME"]

    for record in records:
        try:
            responseDNS = dns.resolver.resolve(url, record)

            for response in responseDNS:
                print(f"{record} ---> {response}")
        except dns.resolver.NoAnswer:
            print(f"{record} kaydı bulunamadı.")
        except dns.resolver.NXDOMAIN:
            print(f"{url} geçerli bir alan adı değil.")
            break
        except dns.resolver.Timeout:
            print(f"{url} sorgusu zaman aşımına uğradı.")
        except Exception as e:
            print(f"{record} sorgusu sırasında bir hata oluştu: {str(e)}")


subdomains = []
dnsSet = set()

if __name__ == "__main__":

    url,output = clıInput()

    if not str.__contains__(url,"https://") or not str.__contains__(url,"http://"):

        chrome_options = Options()
        # chrome_options.add_argument("--headless"),


        driver = webdriver.Chrome(options=chrome_options)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        subdomains = CRTsh(driver,url) + Bing(driver,url) + Google(driver,url) + Yahoo(driver,url) + Yandex(driver,url)

        for subs in subdomains:
            if url in subs:
                dnsSet.add(subs)

        for subs in dnsSet:
            print(subs)

            if not subs == "":
                f = open(output,"a")
                f.write(subs+"\n")
                f.close()

        DNSRecord(url)
