import subprocess
import urllib.request
from bs4 import BeautifulSoup
import sys
import json
import unicodedata

# config
debug = False
# debug = False
exception = ""

# Get query from Alfred
alfredQuery = str(sys.argv[1])
ip = unicodedata.normalize('NFC',alfredQuery)

# if ip is None or len(ip) == 0 or ip == "null":
# # Get IP address from clipboard
#     process = subprocess.Popen("pbpaste", stdout=subprocess.PIPE)
#     output, error = process.communicate()
#     ip = output.decode("utf-8").strip()

# ip = 'bing.com'

url = f"https://ip.tool.chinaz.com/{ip}"
# response = requests.get(url, timeout=5)

# 发送GET请求获取网页内容
try:
    response = urllib.request.urlopen(url, timeout=5)
except Exception as e:
    trace_back = sys.exc_info()[2]
    line = trace_back.tb_lineno
    exception = str(line) + ": " + str(e)

html_content = response.read().decode('utf-8')
if debug:
    with open("tmp.html", "w") as file:
        file.write(html_content)

def getResult(html_content):
# 解析 HTML 内容
    soup = BeautifulSoup(html_content, 'html.parser')

# 使用 CSS 选择器获取指定的元素
    divs = soup.select('#leftinfo > div:nth-child(3) > div:nth-child(2) > div.WhwtdWrap.bor-b1s.col-gray03')

# 遍历每个 div，并提取每个 span 的信息
    itemList = []
    for div in divs:
        item = {}
        spans = div.find_all('span')
        item["domain"] = spans[0].text.strip()
        item["ip"] = spans[1].text.strip()
        item["numeric_address"] = spans[2].text.strip()
        item["ISP"] = spans[3].text.strip()
        item["GEO"] = spans[4].text.split("\n")[1]
        item["title"] = item["ip"]
        item["subtitle"] = item["GEO"] + "  " + item["ISP"]
        # arg was passed to next object(eg: Copy to Cilpboard)
        item["arg"] = item["ip"]
        itemList.append(item)
    return itemList

itemList = []
if html_content.find("域名或IP解析失败") != -1:
    exception = "chinaz.com: 域名或IP解析失败"
else:
    itemList = getResult(html_content)

# print(itemList)

if exception:
    item = {}
    item["uid"] = 1
    item["type"] = "default"
    item["title"] = "There was an error:"
    item["subtitle"] = str(exception)
    item["arg"] = url
    itemList.append(item)

if not itemList:
    item = {}
    item["uid"] = 1
    item["type"] = "default"
    item["title"] = "GEO IP - No results, empty query, or error"
    item["subtitle"] = " "
    item["arg"] = url
    itemList.append(item)

items = {}
items["items"] = itemList
items_json = json.dumps(items)
sys.stdout.write(items_json)
