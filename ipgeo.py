import urllib.request
import urllib.error
import json
import sys
import socket
import struct

ip = sys.argv[1] if len(sys.argv) > 1 else ''
if not ip:
    ip = ''

url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,org,as,query"

try:
    response = urllib.request.urlopen(url, timeout=10)
    data = json.loads(response.read().decode('utf-8'))
except Exception as e:
    item = {
        "uid": 1,
        "type": "default",
        "title": "Error",
        "subtitle": str(e),
        "arg": url
    }
    items = {"items": [item]}
    sys.stdout.write(json.dumps(items))
    sys.exit(0)

if data.get("status") == "fail":
    item = {
        "uid": 1,
        "type": "default",
        "title": "GEO IP - No results, empty query, or error",
        "subtitle": data.get("message", "Invalid query or IP address"),
        "arg": url
    }
    items = {"items": [item]}
    sys.stdout.write(json.dumps(items))
    sys.exit(0)

def ip_to_numeric(ip_addr):
    try:
        packed = socket.inet_aton(ip_addr)
        return struct.unpack("!I", packed)[0]
    except Exception:
        return ""

geo_parts = [p for p in [data.get("country"), data.get("regionName"), data.get("city")] if p]
geo = " ".join(geo_parts)
ip_addr = data.get("query", "")
isp = data.get("isp", "")

item = {
    "domain": ip,
    "ip": ip_addr,
    "numeric_address": ip_to_numeric(ip_addr),
    "ISP": isp,
    "GEO": geo,
    "title": ip_addr,
    "subtitle": f"{geo} | {isp}",
    "arg": ip_addr
}

items = {"items": [item]}
sys.stdout.write(json.dumps(items))
