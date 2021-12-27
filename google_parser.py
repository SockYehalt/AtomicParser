import requests, urllib.parse, threading, random, os, json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()
seen_doms = []
proxylist = []

if not os.path.exists("config.json"):
    with open("config.json", "w") as f:
        data = {"retries": 3}
        json.dump(data, f, indent=4)

with open("config.json", "r") as f:
    data = json.load(f)
    set_rtrs = data["retries"]
while True:
    dks_file = input("dorks file path: ").replace('"', "").strip()
    if dks_file != None and dks_file != "" and dks_file != " ":
        break
broxtype = input("0 for proxyless 1 for http 2 for socks4 3 for socks5\n")
if broxtype != "0":
    while True:
        prox_file = input("proxy file path: ").replace('"', "").strip()
        if prox_file != None and prox_file != "" and prox_file != " ":
            with open(prox_file, "r+", errors="ignore") as f:
                proxiesss = f.readlines()
                for prox in proxiesss:
                    proxylist.append(prox)
            break


def parss(drkk):

    retries, amt = 0, 0
    while True:
        if broxtype == "0":
            proxydic = None

        elif broxtype == "2":
            proxy_to_use = random.choice(proxylist)
            proxydic = {
                "http": f"socks4://{proxy_to_use}",
                "https": f"socks4://{proxy_to_use}",
            }
        elif broxtype == "3":
            proxy_to_use = random.choice(proxylist)
            proxydic = {
                "http": f"socks5h://{proxy_to_use}",
                "https": f"socks5h://{proxy_to_use}",
            }

        elif broxtype == "1":
            proxy_to_use = random.choice(proxylist)
            proxydic = {
                "http": f"http://{proxy_to_use}",
                "https": f"http://{proxy_to_use}",
            }
        else:
            proxydic = None
        try:
            r = requests.get(
                f"https://www.google.com/search?q={drkk}&start={amt*10}",
                headers={"user-agent": ua.chrome},
                proxies=proxydic,
            )
            soup = BeautifulSoup(r.text, "html.parser")

            for link in soup.find_all("a"):
                link = link["href"]
                if "/url?q=" in link:

                    link = link.replace("/url?q=", "")
                    pass
                if "/search" in link:
                    continue
                if "google" in link:
                    continue
                linka = str(link)
                try:
                    dom = linka.split("/")[2]
                    if dom in seen_doms:
                        continue
                    if dom not in seen_doms:
                        seen_doms.append(dom)
                        print(linka)
                        with open("yes1.txt", "a") as f:
                            f.write(linka + "\n")
                except Exception as e:
                    with open("errors.txt", "a") as f:
                        f.write(str(e) + "\n")
                    threading.Thread(target=parss, args=(drkk.strip(),)).start()

        except Exception as e:
            with open("errors.txt", "a") as f:
                f.write(str(e) + "\n")

            retries += 1
            if retries == set_rtrs and amt == 10:
                break
        if amt == 10:
            break


def threadyes():

    with open(dks_file, "r+", errors="ignore") as f:
        drks = f.readlines()
        for drk in drks:
            drk = drk.replace("\n", "")
            drkk = urllib.parse.quote_plus(drk)
            while True:
                if threading.active_count() < 200:
                    threading.Thread(
                        target=parss,
                        args=(drkk.strip(),),
                    ).start()
                    break


threadyes()
