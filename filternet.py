import socket
from sys import platform
from os import popen

distinct_ips = []
domains_list = ['list-of-domains.com']


def linux():
    # Find default gateway
    default_gw = popen("ip r | grep default | cut -d ' ' -f 3").read().strip()
    # Find default ethernet device
    default_eth = popen("ip -4 route ls | grep default | cut -d ' ' -f 5").read().strip()
    with open('linux.sh', 'w') as file:
        file.write(f'''ip route add "YOUR_STATIC_IPs" via {default_gw} dev {default_eth}
''')
        for domain in domains_list:
            socket_info = socket.getaddrinfo(domain, 0)
            for result in socket_info:
                ns_ip = result[4][0]
                if distinct_ips.count(ns_ip) == 0:
                    distinct_ips.append(ns_ip)
                    file.write(f'ip route add {ns_ip} via {default_gw} dev {default_eth}\n')
    popen('bash ./linux.sh')  # You may comment if don't want to run it


def windows():
    with open('windows.cmd', 'w') as file:
        file.write('''@echo off
set "ip="
for /f "tokens=2,3 delims={,}" %%a in ('"WMIC NICConfig where IPEnabled="True" get DefaultIPGateway /value | find "I" "') do if not defined ip set ip=%%~a

set "command=route add -p"
::set "delete=route delete -p"
::%command% 1.1.1.1 %ip%
::%delete% 1.1.1.1 %ip%
:: in-line comment: %= COMMENT =%

REM remove this line and add your server's static ips if having no domain names
''')
        for domain in domains_list:
            socket_info = socket.getaddrinfo(domain, 0)
            for result in socket_info:
                ns_ip = result[4][0]
                if distinct_ips.count(ns_ip) == 0:
                    distinct_ips.append(ns_ip)
                    file.write(f'echo adding ip {ns_ip} for {domain}\n%command% {ns_ip} %ip%\n')
        file.write('\npause')
        popen('powershell.exe "Start-Process windows.cmd -verb runAs"')  # You may comment if don't want to run it


if platform == "linux" or platform == "linux2":
    linux()
elif platform == "darwin":
    print('Mac OS, no plans yet:(')
elif platform == "win32":
    windows()
