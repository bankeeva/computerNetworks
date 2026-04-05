import subprocess
import socket

import pandas as pd


domains = [
    'google.com',
    'cloudflare.com',
    'blog.deepschool.ru'
]
ips = []
traceroutes = []

for domain in domains:
    ip = ''
    traceroute = ''
    
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        ip = 'None'
        traceroute = ''
    else:
        try:
            result = subprocess.run(
                ['traceroute', ip],
                capture_output=True,
                text=True
            )
            traceroute = result.stdout.replace('\n', ' | ')
        except Exception as e:
            print(e)
            traceroute = ''
    
    ips.append(ip)
    traceroutes.append(traceroute)
    

df = pd.DataFrame({
    "domen": domains, 
    "IP": ips, 
    "traceroute": traceroutes
})
df.to_csv("result.csv", index=False)
