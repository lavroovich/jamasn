"""
- ip details resolver (v.5)
- works on ip-api.com
"""

import requests
import sys
import json
import os
import ipaddress

ipCacheFile = "jamASN_ip_cache.json"

FIELDS = "status,message,country,regionName,city,isp"


def loadCache(filename: str):
    if not os.path.exists(filename):
        return {}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def saveCache(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


ipCaches = loadCache(ipCacheFile)


def getIPInfo(ip: str):
    if ip in ipCaches:
        print("cached", file=sys.stderr)
        return ipCaches[ip]

    rq = requests.get(
        f"http://ip-api.com/json/{ip}?fields={FIELDS}",
        timeout=3
    )
    rq.raise_for_status()

    data = rq.json()

    if data.get("status") != "success":
        message = data.get("message", "unknown error")
        raise Exception(message)

    ipInfo = {
        "country": data.get("country", "N/A"),
        "region": data.get("regionName", "N/A"),
        "city": data.get("city", "N/A"),
        "isp": data.get("isp", "N/A")
    }

    ipCaches[ip] = ipInfo
    saveCache(ipCacheFile, ipCaches)

    return ipInfo


def parseIP(ip: str):
    try:
        ipInfo = getIPInfo(ip)

        isp = ipInfo.get("isp", "N/A")
        country = ipInfo.get("country", "N/A")
        region = ipInfo.get("region", "N/A")
        city = ipInfo.get("city", "N/A")

        return f"{isp} | {country}, {region}, {city}"

    except Exception as e:
        return f"N/A ({e})"


def validateIP(internetProtocolAddress):
    try:
        r = ipaddress.ip_address(internetProtocolAddress)

        if r.is_private:
            return "private"

        return True

    except ValueError:
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("айпишник не передан", file=sys.stderr)
        sys.exit(1)

    ip = sys.argv[1]
    isValid = validateIP(ip)

    if isValid is False:
        print("неккоректный айпи", file=sys.stderr)
        print("это что за говно")
        sys.exit(1)

    elif isValid == "private":
        print("чооооооо локальный чел", file=sys.stderr)
        print("говно локальное")
        sys.exit(192)

    result = parseIP(ip)
    print(result)

    if result.startswith("N/A"):
        sys.exit(2)

    sys.exit(0)