from django.test import TestCase

# Create your tests here.

from xmlrpc import client
remote = client.Server("http://192.168.1.138/cobbler_api")
token = remote.login("cobbler", "cobbler")
system_id = remote.new_system(token)


remote.modify_system(system_id, "name", "centos2", token)
remote.modify_system(system_id, "hostname", "hostname.example.com", token)
remote.modify_system(system_id, "gateway", "192.168.1.1", token)
remote.modify_system(system_id, "name_servers", "8.8.8.8", token)



# 关联内核参数，相当于cobbler profile edit --name=CentOS7.2-x86_64 --kopts=‘net.ifnames=0 biosdevname=0‘，这个装6系统不需要
#remote.modify_system(system_id, "kernel_options", "net.ifnames=0 biosdevname=0", token)



remote.modify_system(system_id, 'modify_interface', {
    "macaddress-eth0": "01:02:03:04:05:07",
    "ipaddress-eth0": "192.168.1.80",
    "gateway-eth0": "192.168.1.2", # 改参数不能用
    "subnet-eth0": "255.255.255.0",
    "static-eth0": 1,
    #"dnsname-eth0": "114.114.114.114"
}, token)
remote.modify_system(system_id, "profile", "CentOS-6.9-x86_64", token)
remote.modify_system(system_id, "ks_meta", "/var/lib/cobbler/kickstarts/CentOS-6.8-x86_64.cfg", token)


remote.save_system(system_id, token)
ret = remote.sync(token)
print(ret)