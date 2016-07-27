nodes:
   - name: node1-control
     tags: control      #optional param, other valid value "compute"
     arch: "x86_64"
     mac_address: "4c:09:b4:b2:59:87" #pxe boot interface mac
     power:
       type: ipmi
       address: 129.5.1.101
       user: zteroot
       pass: superuser
   - name: node2-control
     tags: control
     arch: "x86_64"
     mac_address: "4c:09:b4:b2:59:fc"
     power:
       type: ipmi
       address: 129.5.1.22
       user: zteroot
       pass: superuser
   - name: node3-control
     tags: control
     arch: "x86_64"
     mac_address: "4c:09:b4:b2:59:a2"
     power:
       type: ipmi
       address: 129.5.1.3
       user: zteroot
       pass: superuser

   - name: node4-control
     tags: compute
     arch: "x86_64"
     mac_address: "4c:09:b4:b2:59:d8"
     power:
       type: ipmi
       address: 129.5.1.4
       user: zteroot
       pass: superuser

   - name: node5-control
     tags: compute
     arch: "x86_64"
     mac_address: "4c:09:b4:b2:59:75"
     power:
       type: ipmi
       address: 129.5.1.5
       user: zteroot
       pass: superuser

