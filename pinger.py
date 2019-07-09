import ipaddress
from subprocess import Popen, PIPE


i = str(ipaddress.ip_address('172.24.5.25'))
ping = Popen(['ping', '-c', '3', i], stdout=PIPE)
output = ping.communicate()[0]
host_alive = ping.returncode
if host_alive == 0:
    print(i, 'is reachable')
else:
    print(i, 'is unreachable')
