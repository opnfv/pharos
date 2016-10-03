#!/usr/bin/env python3

def test_ssh_thread():
    """Test to see if ssh connections are attempted the proper amount of times"""
    from pharosvalidator.server import ssh_thread
    ssh_thread("127.0.0.1", "0.0.0.0", "1", 10)



