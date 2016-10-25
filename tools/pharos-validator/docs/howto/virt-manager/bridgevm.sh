sudo /usr/libexec/qemu-kvm -hda /vm/template/jump-host.img -device e1000,netdev=net0,mac=DE:AD:BE:EF:FE:7A -netdev tap,id=net0
