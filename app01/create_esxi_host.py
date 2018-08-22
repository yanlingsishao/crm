#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-7-12 18:30
# @Author  : Jerry Wang
# @Site    : 
# @File    : create_esxi_host.py
# @Software: PyCharm
from pyVim import connect
import atexit
from pyVmomi import vim
# from tools import tasks

#获取连接对象
si = connect.SmartConnectNoSSL(host="192.168.1.217",
                             user="root",
                             pwd="huazhen@123",
                             port=443)

#断开连接
atexit.register(connect.Disconnect, si)




def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj

#添加网卡配置
def add_nic_spec(si, config_spec, network):
    nic_changes = []

    nic_spec = vim.vm.device.VirtualDeviceSpec()
    nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
    nic_spec.device = vim.vm.device.VirtualE1000()
    nic_spec.device.deviceInfo = vim.Description()
    nic_spec.device.deviceInfo.summary = 'vCenter API test'
    nic_spec.device.backing = \
        vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
    nic_spec.device.backing.useAutoDetect = False
    content = si.RetrieveContent()
    nic_spec.device.backing.network = get_obj(content, [vim.Network], network)
    nic_spec.device.backing.deviceName = network
    nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    nic_spec.device.connectable.startConnected = True
    nic_spec.device.connectable.startConnected = True
    nic_spec.device.connectable.allowGuestControl = True
    nic_spec.device.connectable.connected = True
    nic_spec.device.connectable.status = 'untried'
    nic_spec.device.wakeOnLanEnabled = True
    nic_spec.device.addressType = 'generated'
    nic_changes.append(nic_spec)
    config_spec.deviceChange = nic_changes

    return config_spec


def create_dummy_vm(name, si, vm_folder, resource_pool, datastore):
    #定义vm存储目录
    datastore_path = '[' + datastore + '] ' + name

    # bare minimum VM shell, no disks. Feel free to edit
    vmx_file = vim.vm.FileInfo(logDirectory=None,
                               snapshotDirectory=None,
                               suspendDirectory=None,
                               vmPathName=datastore_path,
                               )
    #配置vm boot配置
    config = vim.vm.ConfigSpec(name=name, memoryMB=1048, numCPUs=1, files=vmx_file, guestId='centos7_64Guest',
                               version='vmx-13',)

    # dynamicType = < unset >,
    # dynamicProperty = (vmodl.DynamicProperty)[],
    # name = 'test-p2p-h5-1(233)',
    # template = false,
    # vmPathName = '[other-system-data] test1-h5/test1-h5.vmx',
    # memorySizeMB = 2048,
    # cpuReservation = 0,
    # memoryReservation = 0,
    # numCpu = 1,
    # numEthernetCards = 1,
    # numVirtualDisks = 1,
    # uuid = '564d56ee-fa2e-2cbe-1f9e-0903c818979e',
    # instanceUuid = '529bc6d6-c9f8-9eb0-f248-e01936a4463d',
    # guestId = 'centos6_64Guest',
    # guestFullName = 'CentOS 6 (64-bit)',
    # annotation = '',
    # product = < unset >,
    # installBootRequired = < unset >,
    # ftInfo = < unset >,
    # managedBy = < unset >,
    # tpmPresent = < unset >,
    # numVmiopBackings = < unset >
    config = add_nic_spec(si, config, network='VMXNet3')

    #创建虚拟机
    task = vm_folder.CreateVM_Task(config=config, pool=resource_pool)

    print(task._stub.lock.__dict__)

    #tasks.wait_for_tasks(si, [task])

content = si.RetrieveContent()
container = content.rootFolder
recursive = True
viewType = [vim.VirtualMachine]
datacenter = content.rootFolder.childEntity[0]
vmfolder = datacenter.vmFolder
hosts = datacenter.hostFolder.childEntity
resource_pool = hosts[0].resourcePool

containerView = content.viewManager.CreateContainerView(container, viewType, recursive)
    # 遍历虚拟机列表打印虚拟机详情
children = containerView.view
for child in children:
    print(child.summary)

name = "test_vm02"
create_dummy_vm(name, si, vmfolder, resource_pool,
                        datastore="other-system-data")


