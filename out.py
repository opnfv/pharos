{'idf': {'fuel': {'jumphost': {'bridges': {'admin': 'pxebr', 'public': '', 'private': '', 'mgmt': 'br-ctl'}}, 'version': 5.11, 'network': {'node': [{'busaddr': ['0000:06:00.0', '0000:07:00.0', '0000:08:00.0', '0000:09:00.0'], 'interfaces': ['enp6s0', 'enp7s0', 'enp8s0', 'enp9s0']}, {'busaddr': ['0000:06:00.0', '0000:07:00.0', '0000:08:00.0', '0000:09:00.0'], 'interfaces': ['enp6s0', 'enp7s0', 'enp8s0', 'enp9s0']}, {'busaddr': ['0000:06:00.0', '0000:07:00.0', '0000:08:00.0', '0000:09:00.0'], 'interfaces': ['enp6s0', 'enp7s0', 'enp8s0', 'enp9s0']}, {'busaddr': ['0000:06:00.0', '0000:07:00.0', '0000:08:00.0', '0000:09:00.0'], 'interfaces': ['enp6s0', 'enp7s0', 'enp8s0', 'enp9s0']}, {'busaddr': ['0000:06:00.0', '0000:07:00.0', '0000:08:00.0', '0000:09:00.0'], 'interfaces': ['enp6s0', 'enp7s0', 'enp8s0', 'enp9s0']}]}}, 'version': 'poc 2.3', 'pod_name': 'pod0 poc', 'common': {'node_config': {'jumphost': {'fixed_ips': {'admin': '192.168.11.100', 'public': '172.30.10.100', 'mgmt': '10.167.4.100'}}, 'nodes': [{'fixed_ips': {'admin': '192.168.11.101', 'public': '172.30.10.101', 'mgmt': '10.167.4.101'}}, {'fixed_ips': {'admin': '192.168.11.102', 'public': '172.30.10.102', 'mgmt': '10.167.4.102'}}, {'fixed_ips': {'admin': '192.168.11.103', 'public': '172.30.10.103', 'mgmt': '10.167.4.103'}}, {'fixed_ips': {'admin': '192.168.11.104', 'public': '172.30.10.104', 'mgmt': '10.167.4.104'}}, {'fixed_ips': {'admin': '192.168.11.105', 'public': '172.30.10.105', 'mgmt': '10.167.4.105'}}]}, 'network_config': {'oob': {'vlan': 'vlan0_0', 'mask': 24, 'network': '172.30.10.0'}, 'admin': {'vlan': 'vlan1_0', 'mask': 24, 'network': '192.168.11.0'}, 'mgmt': {'vlan': 'vlan1_1000', 'mask': 24, 'network': '10.167.4.0'}, 'storage': {'vlan': 'vlan2_2001', 'mask': 24, 'network': '10.2.0.0'}, 'public': {'vlan': 'vlan2_0', 'mask': 24, 'network': '172.30.10.0', 'dns': ['8.8.8.8', '8.8.4.4'], 'gateway': '172.30.10.1'}, 'private': {'vlan': 'vlan2_2000', 'mask': 24, 'network': '10.1.0.0'}}}}, 'network': {'tor_switch': {'port_vlan_config': {'jumphost': [{'port0': {'vlan0_0': 'native'}}, {'port1': {'vlan1_1002': 1002, 'vlan1_1000': 1000, 'vlan1_1001': 1001, 'vlan1_0': 'native'}}, {'port2': {'vlan2_0': 'native', 'vlan2_2002': 2002, 'vlan2_2000': 2000, 'vlan2_2001': 2001}}, {'port3': 'unused'}, {'port4': 'unused'}], 'node1': [{'port0': {'vlan0_0': 'native'}}, {'port1': {'vlan1_1002': 1002, 'vlan1_1000': 1000, 'vlan1_1001': 1001, 'vlan1_0': 'native'}}, {'port2': {'vlan2_0': 'native', 'vlan2_2002': 2002, 'vlan2_2000': 2000, 'vlan2_2001': 2001}}, {'port3': 'unused'}, {'port4': 'unused'}], 'node3': [{'port0': {'vlan0_0': 'native'}}, {'port1': {'vlan1_1002': 1002, 'vlan1_1000': 1000, 'vlan1_1001': 1001, 'vlan1_0': 'native'}}, {'port2': {'vlan2_0': 'native', 'vlan2_2002': 2002, 'vlan2_2000': 2000, 'vlan2_2001': 2001}}, {'port3': 'unused'}, {'port4': 'unused'}], 'node2': [{'port0': {'vlan0_0': 'native'}}, {'port1': {'vlan1_1002': 1002, 'vlan1_1000': 1000, 'vlan1_1001': 1001, 'vlan1_0': 'native'}}, {'port2': {'vlan2_0': 'native', 'vlan2_2002': 2002, 'vlan2_2000': 2000, 'vlan2_2001': 2001}}, {'port3': 'unused'}, {'port4': 'unused'}], 'node5': [{'port0': {'vlan0_0': 'native'}}, {'port1': {'vlan1_1002': 1002, 'vlan1_1000': 1000, 'vlan1_1001': 1001, 'vlan1_0': 'native'}}, {'port2': {'vlan2_0': 'native', 'vlan2_2002': 2002, 'vlan2_2000': 2000, 'vlan2_2001': 2001}}, {'port3': 'unused'}, {'port4': 'unused'}], 'node4': [{'port0': {'vlan0_0': 'native'}}, {'port1': {'vlan1_1002': 1002, 'vlan1_1000': 1000, 'vlan1_1001': 1001, 'vlan1_0': 'native'}}, {'port2': {'vlan2_0': 'native', 'vlan2_2002': 2002, 'vlan2_2000': 2000, 'vlan2_2001': 2001}}, {'port3': 'unused'}, {'port4': 'unused'}]}, 'network_trunks': {0: {'vlan0_0': 'native'}, 1: {'vlan1_1002': 1002, 'vlan1_1000': 1000, 'vlan1_1001': 1001, 'vlan1_0': 'native'}, 2: {'vlan2_0': 'native', 'vlan2_2002': 2002, 'vlan2_2000': 2000, 'vlan2_2001': 2001}}}}, 'jumphost': {'node': {'vendor': 'Cisco Systems Inc', 'type': 'baremetal', 'cpu_cflags': 'haswell', 'cpus': 2, 'memory': '128G', 'cores': 8, 'model': 'UCSB-B200-M4', 'arch': 'x86_64'}, 'remote_management': {'mac_address': 'a8:9d:21:c9:c4:9e', 'user': 'aaaa', 'versions': [2.0], 'ip_address': '172.30.8.83', 'pass': 'bbbb', 'type': 'ipmi', 'port': 'port0'}, 'name': 'pod0-jump', 'remote_params': {'versions': [2.0], 'type': 'ipmi', 'user': 'aaaa', 'pass': 'bbbb'}, 'port_vlans': [{'port0': {'vlan0_0': 'native'}}, {'port1': {'vlan1_1002': 1002, 'vlan1_1000': 1000, 'vlan1_1001': 1001, 'vlan1_0': 'native'}}, {'port2': {'vlan2_0': 'native', 'vlan2_2002': 2002, 'vlan2_2000': 2000, 'vlan2_2001': 2001}}, {'port3': 'unused'}, {'port4': 'unused'}], 'interfaces': [{'mac_address': '00:25:b5:a0:00:1a', 'speed': '40gb', 'port': 'port1', 'features': 'dpdk|sriov'}, {'mac_address': '00:25:b5:a0:00:1b', 'speed': '40gb', 'port': 'port2', 'features': 'dpdk|sriov'}, {'mac_address': '00:25:b5:a0:00:1c', 'speed': '40gb', 'port': 'port3', 'features': 'dpdk|sriov'}, {'mac_address': '00:25:b5:a0:00:1d', 'speed': '40gb', 'port': 'port4', 'features': 'dpdk|sriov'}], 'disks': [{'disk_interface': 'sas', 'disk_capacity': '2400G', 'name': 'disk1', 'disk_type': 'hdd', 'disk_rotation': None}]}, 'nodes': [{'node': {'vendor': 'Cisco Systems Inc', 'type': 'baremetal', 'cpu_cflags': 'haswell', 'cpus': 2, 'memory': '32G', 'cores': 8, 'model': 'UCSB-B200-M4', 'arch': 'x86_64'}, 'remote_management': {'mac_address': 'a8:9d:21:c9:8b:56', 'user': 'aaaa', 'versions': [2.0], 'type': 'ipmi', 'pass': 'bbbb', 'ip_address': '172.30.8.75', 'port': 'port0'}, 'vlan_config': [{'port0': {'vlan0_0': 'native'}}, {'port1': {'vlan1_1002': 1002, 'vlan1_1000': 1000, 'vlan1_1001': 1001, 'vlan1_0': 'native'}}, {'port2': {'vlan2_0': 'native', 'vlan2_2002': 2002, 'vlan2_2000': 2000, 'vlan2_2001': 2001}}, {'port3': 'unused'}, {'port4': 'unused'}], 'name': 'pod0-node1', 'interfaces': [{'mac_address': '00:25:b5:a0:00:2a', 'speed': '40gb', 'features': 'dpdk|sriov', 'port': 'port1'}, {'mac_address': '00:25:b5:a0:00:2b', 'speed': '40gb', 'features': 'dpdk|sriov', 'port': 'port2'}, {'mac_address': '00:25:b5:a0:00:2c', 'speed': '40gb', 'features': 'dpdk|sriov', 'port': 'port3'}, {'mac_address': '00:25:b5:a0:00:2d', 'speed': '40gb', 'features': 'dpdk|sriov', 'port': 'port4'}], 'disks': [{'disk_interface': 'sas', 'disk_capacity': '2400G', 'name': 'disk1', 'disk_type': 'hdd', 'disk_rotation': None}]}, {'node': {'vendor': 'Cisco Systems Inc', 'type': 'baremetal', 'cpu_cflags': 'haswell', 'cpus': 2, 'memory': '32G', 'cores': 8, 'model': 'UCSB-B200-M4', 'arch': 'x86_64'}, 'remote_management': {'pass': 'bbbb', 'user': 'aaaa', 'versions': [2.0], 'ip_address': '172.30.8.65', 'mac_address': 'a8:9d:21:c9:4d:26', 'type': 'ipmi', 'port': 'port0'}, 'vlan_config': [{'port0': {'vlan0_0': 'native'}}, {'port1': {'vlan1_1002': 1002, 'vlan1_1000': 1000, 'vlan1_1001': 1001, 'vlan1_0': 'native'}}, {'port2': {'vlan2_0': 'native', 'vlan2_2002': 2002, 'vlan2_2000': 2000, 'vlan2_2001': 2001}}, {'port3': 'unused'}, {'port4': 'unused'}], 'name': 'pod0-node2', 'interfaces': [{'mac_address': '00:25:b5:a0:00:3a', 'speed': '40gb', 'port': 'port1', 'features': 'dpdk|sriov'}, {'mac_address': '00:25:b5:a0:00:3b', 'speed': '40gb', 'port': 'port2', 'features': 'dpdk|sriov'}, {'mac_address': '00:25:b5:a0:00:3c', 'speed': '40gb', 'port': 'port3', 'features': 'dpdk|sriov'}, {'mac_address': '00:25:b5:a0:00:3d', 'speed': '40gb', 'port': 'port4', 'features': 'dpdk|sriov'}], 'disks': [{'disk_interface': 'sas', 'disk_capacity': '2400G', 'name': 'disk1', 'disk_type': 'hdd', 'disk_rotation': None}]}, {'node': {'vendor': 'Cisco Systems Inc', 'type': 'baremetal', 'cpu_cflags': 'haswell', 'cpus': 2, 'memory': '32G', 'cores': 8, 'model': 'UCSB-B200-M4', 'arch': 'x86_64'}, 'remote_management': {'pass': 'bbbb', 'user': 'aaaa', 'versions': [2.0], 'ip_address': '172.30.8.74', 'mac_address': 'a8:9d:21:c9:3a:92', 'type': 'ipmi', 'port': 'port0'}, 'vlan_config': [{'port0': {'vlan0_0': 'native'}}, {'port1': {'vlan1_1002': 1002, 'vlan1_1000': 1000, 'vlan1_1001': 1001, 'vlan1_0': 'native'}}, {'port2': {'vlan2_0': 'native', 'vlan2_2002': 2002, 'vlan2_2000': 2000, 'vlan2_2001': 2001}}, {'port3': 'unused'}, {'port4': 'unused'}], 'name': 'pod0-node3', 'interfaces': [{'mac_address': '00:25:b5:a0:00:4a', 'speed': '40gb', 'port': 'port1', 'features': 'dpdk|sriov'}, {'mac_address': '00:25:b5:a0:00:4b', 'speed': '40gb', 'port': 'port2', 'features': 'dpdk|sriov'}, {'mac_address': '00:25:b5:a0:00:4c', 'speed': '40gb', 'port': 'port3', 'features': 'dpdk|sriov'}, {'mac_address': '00:25:b5:a0:00:4d', 'speed': '40gb', 'port': 'port4', 'features': 'dpdk|sriov'}], 'disks': [{'disk_interface': 'sas', 'disk_capacity': '2400G', 'name': 'disk1', 'disk_type': 'hdd', 'disk_rotation': None}]}, {'node': {'vendor': 'Cisco Systems Inc', 'type': 'baremetal', 'cpu_cflags': 'haswell', 'cpus': 2, 'memory': '32G', 'cores': 8, 'model': 'UCSB-B200-M4', 'arch': 'x86_64'}, 'remote_management': {'pass': 'bbbb', 'user': 'aaaa', 'versions': [2.0], 'ip_address': '172.30.8.73', 'mac_address': '74:a2:e6:a4:14:9c', 'type': 'ipmi', 'port': 'port0'}, 'vlan_config': [{'port0': {'vlan0_0': 'native'}}, {'port1': {'vlan1_1002': 1002, 'vlan1_1000': 1000, 'vlan1_1001': 1001, 'vlan1_0': 'native'}}, {'port2': {'vlan2_0': 'native', 'vlan2_2002': 2002, 'vlan2_2000': 2000, 'vlan2_2001': 2001}}, {'port3': 'unused'}, {'port4': 'unused'}], 'name': 'pod0-node4', 'interfaces': [{'mac_address': '00:25:b5:a0:00:5a', 'speed': '40gb', 'port': 'port1', 'features': 'dpdk|sriov'}, {'mac_address': '00:25:b5:a0:00:5b', 'speed': '40gb', 'port': 'port2', 'features': 'dpdk|sriov'}, {'mac_address': '00:25:b5:a0:00:5c', 'speed': '40gb', 'port': 'port3', 'features': 'dpdk|sriov'}, {'mac_address': '00:25:b5:a0:00:5d', 'speed': '40gb', 'port': 'port4', 'features': 'dpdk|sriov'}], 'disks': [{'disk_interface': 'sas', 'disk_capacity': '2400G', 'name': 'disk1', 'disk_type': 'hdd', 'disk_rotation': None}]}, {'node': {'vendor': 'Cisco Systems Inc', 'type': 'baremetal', 'cpu_cflags': 'haswell', 'cpus': 2, 'memory': '32G', 'cores': 8, 'model': 'UCSB-B200-M4', 'arch': 'x86_64'}, 'remote_management': {'pass': 'bbbb', 'user': 'aaaa', 'versions': [2.0], 'ip_address': '172.30.8.72', 'mac_address': 'a8:9d:21:a0:15:9c', 'type': 'ipmi', 'port': 'port0'}, 'vlan_config': [{'port0': {'vlan0_0': 'native'}}, {'port1': {'vlan1_1002': 1002, 'vlan1_1000': 1000, 'vlan1_1001': 1001, 'vlan1_0': 'native'}}, {'port2': {'vlan2_0': 'native', 'vlan2_2002': 2002, 'vlan2_2000': 2000, 'vlan2_2001': 2001}}, {'port3': 'unused'}, {'port4': 'unused'}], 'name': 'pod0-node5', 'interfaces': [{'mac_address': '00:25:b5:a0:00:6a', 'speed': '40gb', 'port': 'port1', 'features': 'dpdk|sriov'}, {'mac_address': '00:25:b5:a0:00:6b', 'speed': '40gb', 'port': 'port2', 'features': 'dpdk|sriov'}, {'mac_address': '00:25:b5:a0:00:6c', 'speed': '40gb', 'port': 'port3', 'features': 'dpdk|sriov'}, {'mac_address': '00:25:b5:a0:00:6d', 'speed': '40gb', 'port': 'port4', 'features': 'dpdk|sriov'}], 'disks': [{'disk_interface': 'sas', 'disk_capacity': '2400G', 'name': 'disk1', 'disk_type': 'hdd', 'disk_rotation': None}]}], 'details': {'pod_owner': 'Guillermo Herrero', 'lab': 'Pharos Lab', 'contact': 'guillermo.herrero@enea.com', 'version': 'poc 2.3', 'link': 'http://www.yamllint.com/', 'location': 'Stockholm', 'type': 'prototype', 'pod_name': 'pod0 poc'}}
---
parameters:
  _param:
    opnfv_jump_bridge_admin: pxebr
    opnfv_jump_bridge_mgmt: br-ctl
    opnfv_jump_bridge_private: 
    opnfv_jump_bridge_public: 

    opnfv_infra_config_address: 10.167.4.100
    opnfv_infra_maas_node01_address: 10.167.4.3
    opnfv_infra_maas_node01_deploy_address: 192.168.11.3
    opnfv_infra_kvm_address: 10.167.4.140
    opnfv_infra_kvm_node01_address: 10.167.4.141
    opnfv_infra_kvm_node02_address: 10.167.4.142
    opnfv_infra_kvm_node03_address: 10.167.4.143

    opnfv_infra_maas_pxe_network_address: 192.168.11.0
    opnfv_infra_maas_pxe_address: 192.168.11.3
    opnfv_infra_maas_pxe_start_address: 192.168.11.5
    opnfv_infra_maas_pxe_end_address: 192.168.11.250

    opnfv_openstack_gateway_node01_address: 10.167.4.124
    opnfv_openstack_gateway_node02_address: 10.167.4.125
    opnfv_openstack_gateway_node03_address: 10.167.4.126
    opnfv_openstack_gateway_node01_tenant_address: 10.1.0.6
    opnfv_openstack_gateway_node02_tenant_address: 10.1.0.7
    opnfv_openstack_gateway_node03_tenant_address: 10.1.0.9
    opnfv_openstack_proxy_address: 172.30.10.103
    opnfv_openstack_proxy_node01_address: 172.30.10.104
    opnfv_openstack_proxy_node02_address: 172.30.10.105
    opnfv_openstack_proxy_node01_control_address: 10.167.4.104
    opnfv_openstack_proxy_node02_control_address: 10.167.4.105
    opnfv_openstack_control_address: 10.167.4.10
    opnfv_openstack_control_node01_address: 10.167.4.11
    opnfv_openstack_control_node02_address: 10.167.4.12
    opnfv_openstack_control_node03_address: 10.167.4.13
    opnfv_openstack_database_address: 10.167.4.50
    opnfv_openstack_database_node01_address: 10.167.4.51
    opnfv_openstack_database_node02_address: 10.167.4.52
    opnfv_openstack_database_node03_address: 10.167.4.53
    opnfv_openstack_message_queue_address: 10.167.4.40
    opnfv_openstack_message_queue_node01_address: 10.167.4.41
    opnfv_openstack_message_queue_node02_address: 10.167.4.42
    opnfv_openstack_message_queue_node03_address: 10.167.4.43
    opnfv_openstack_telemetry_address: 10.167.4.75
    opnfv_openstack_telemetry_node01_address: 10.167.4.76
    opnfv_openstack_telemetry_node02_address: 10.167.4.77
    opnfv_openstack_telemetry_node03_address: 10.167.4.78
    opnfv_openstack_compute_node01_single_address: 10.167.4.101
    opnfv_openstack_compute_node02_single_address: 10.167.4.102
    opnfv_openstack_compute_node03_single_address: 10.167.4.103
    opnfv_openstack_compute_node01_control_address: 10.167.4.101
    opnfv_openstack_compute_node02_control_address: 10.167.4.102
    opnfv_openstack_compute_node03_control_address: 10.167.4.103
    opnfv_openstack_compute_node01_tenant_address: 10.1.0.101
    opnfv_openstack_compute_node02_tenant_address: 10.1.0.102
    opnfv_openstack_compute_node03_tenant_address: 10.1.0.103
    opnfv_openstack_compute_node01_external_address: 172.30.10.101
    opnfv_openstack_compute_node02_external_address: 172.30.10.102

    opnfv_opendaylight_server_node01_single_address: 10.167.4.111

    opnfv_net_public_gw: 172.30.10.1
    opnfv_name_servers: ['8.8.8.8', '8.8.4.4']
    opnfv_dns_server01: '8.8.8.8'

    opnfv_net_mgmt_vlan: vlan1_1000
    opnfv_net_tenant_vlan: vlan2_2000

    opnfv_maas_node01_architecture: 'amd64/generic'
    opnfv_maas_node01_power_address: 172.30.8.75
    opnfv_maas_node01_power_type: ipmi
    opnfv_maas_node01_power_user: aaaa
    opnfv_maas_node01_power_password: bbbb

    # Get the PXE interface for a particualr server
    # Only pxe_vlanid is known. Look for it among the ports
    # with the port, locate the interfaceopnfv_maas_node01_interface_mac: '00:25:b5:a0:00:2a'

    opnfv_maas_node02_architecture: 'amd64/generic'
    opnfv_maas_node02_power_address: 172.30.8.65
    opnfv_maas_node02_power_type: ipmi
    opnfv_maas_node02_power_user: aaaa
    opnfv_maas_node02_power_password: bbbb
    opnfv_maas_node02_interface_mac: '00:25:b5:a0:00:3a'

    opnfv_maas_node03_architecture: 'amd64/generic'
    opnfv_maas_node03_power_address: 172.30.8.74
    opnfv_maas_node03_power_type: ipmi
    opnfv_maas_node03_power_user: aaaa
    opnfv_maas_node03_power_password: bbbb
    opnfv_maas_node03_interface_mac: '00:25:b5:a0:00:4a'

    opnfv_maas_node04_architecture: 'amd64/generic'
    opnfv_maas_node04_power_address: 172.30.8.73
    opnfv_maas_node04_power_type: ipmi
    opnfv_maas_node04_power_user: aaaa
    opnfv_maas_node04_power_password: bbbb
    opnfv_maas_node04_interface_mac: '00:25:b5:a0:00:5a'

    opnfv_maas_node05_architecture: 'amd64/generic'
    opnfv_maas_node05_power_address: 172.30.8.72
    opnfv_maas_node05_power_type: ipmi
    opnfv_maas_node05_power_user: aaaa
    opnfv_maas_node05_power_password: bbbb
    opnfv_maas_node05_interface_mac: '00:25:b5:a0:00:6a'
