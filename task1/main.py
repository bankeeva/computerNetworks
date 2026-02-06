import subprocess
import re
import pandas as pd


dom = [
    'google.com',
    'cloudflare.com',
    'wikipedia.org',
    'github.com',
    'apple.com',
    'yandex.ru',
    'openai.com',
    'stackoverflow.com',
    'reddit.com',
    'spotify.com' ]
RTT = []
IP = []
ICMP = []
TTL = []


for d in dom:
    inf = subprocess.run(['ping', '-c', '1', d], capture_output=True, text=True)
    out = inf.stdout
    rtt = re.findall(r"time\S+", out)[0][5:] if inf.returncode == 0 else 'None'
    ip = re.findall(r"from \S+", out)[0][5:-1] if inf.returncode == 0 else 'None'
    icmp = re.findall(r"icmp_seq=\S+", out)[0][9:] if inf.returncode == 0 else 'None'
    ttl = re.findall(r"ttl=\S+", out)[0][4:] if inf.returncode == 0 else 'None'
    RTT.append(rtt)
    IP.append(ip)
    ICMP.append(icmp)
    TTL.append(ttl)

df = pd.DataFrame({"domen": dom, "IP": IP, "RTT": RTT, "ICMP_SEQ": ICMP, "TTL": TTL})
df.to_csv("result.csv", index=False)
