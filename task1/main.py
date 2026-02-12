import subprocess
import re

import pandas as pd


domains = [
    'google.com',
    'cloudflare.com',
    'wikipedia.org',
    'github.com',
    'apple.com',
    'yandex.ru',
    'openai.com',
    'stackoverflow.com',
    'reddit.com',
    'spotify.com'
]
rtt = []
ip = []
icmp = []
ttl = []


for domain in domains:
    inf = subprocess.run(['ping', '-c', '1', domain], capture_output=True, text=True)
    out = inf.stdout
    rtt_val = re.findall(r"time\S+", out)[0][5:] if inf.returncode == 0 else 'None'
    ip_val = re.findall(r"from \S+", out)[0][5:-1] if inf.returncode == 0 else 'None'
    icmp_val = re.findall(r"icmp_seq=\S+", out)[0][9:] if inf.returncode == 0 else 'None'
    ttl_val = re.findall(r"ttl=\S+", out)[0][4:] if inf.returncode == 0 else 'None'
    rtt.append(rtt)
    ip.append(ip)
    icmp.append(icmp)
    ttl.append(ttl)

df = pd.DataFrame({
    "domen": domains, 
    "IP": ip, 
    "RTT": rtt, 
    "ICMP_SEQ": icmp, 
    "TTL": ttl
})
df.to_csv("result.csv", index=False)
