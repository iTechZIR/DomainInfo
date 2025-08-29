import requests
import socket
import webbrowser

print('(=================================================)')
print('(=================> DomainInfo <==================)')
print('(=================================================)\n\n')


def getsubdomains(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        subdomains = set()
        for entry in data:
            namevalue = entry['namevalue']
            for sub in namevalue.split("\n"):
                if domain in sub:
                    subdomains.add(sub.strip())
        return list(subdomains)
    except Exception as e:
        return [f"Error fetching subdomains: {e}"]

def getipinfo(domain):
    try:
        ips = socket.gethostbyname_ex(domain)[2]
        apiresults = []

        for ip in ips:
            api = f"http://ip-api.com/json/{ip}"
            response = requests.get(api, timeout=10)
            data = response.json()
            info = {
                "/- IP": ip,
                " /- ISP": data.get("isp", "N/A"),
                "  /- Country": data.get("country", "N/A"),
                "   /- City": data.get("city", "N/A"),
                "   /- Lat": data.get("lat", "N/A"),
                "   /- Lon": data.get("lon", "N/A"),
                "  /- Name": data.get("org", "N/A"),
                " /- AS": data.get("as", "N/A"),
                "/- Hostname": socket.getfqdn(ip)
            }
            apiresults.append(info)

        return apiresults

    except Exception as e:
        return [{"Error": str(e)}]

def main():
    while True:
        domain = input("[+] - Please The Enter Ip: ").strip()
        if domain.lower() == "end":
            break

        print(f"\n[+] - Getting Subdomains: {domain}")
        subdomains = getsubdomains(domain)
        if subdomains and not subdomains[0].startswith("Error"):
            for sub in subdomains[:10]:
                print(f"  - {sub}")
        else:
            print("  [!] - No Subdomains")

        print(f"\n[+] - Getting Server: {domain}")
        ipinfolist = getipinfo(domain)
        if "Error" in ipinfolist[0]:
            print(f"  Error: {ipinfolist[0]['Error']}")
        else:
            print(f"Server Domain: {len(ipinfolist)}")
            for idx, info in enumerate(ipinfolist, 1):
                for k, v in info.items():
                    print(f"    {k}: {v}")

                lat = info.get("   /- Lat")
                lon = info.get("   /- Lon")
                if isinstance(lat, (float, int)) and isinstance(lon, (float, int)):
                    mapurl = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                    print(f"[+] - Opening Map For This Ip In Browser: {mapurl}\n")
                    webbrowser.open(mapurl, new=2, autoraise=True)
                else:
                    print("[-] - Lat/Lon Not Available Or Invalid Cant Open Map")


if __name__ == "__main__":
    main()
