#!/usr/bin/expect
spawn ssh-keygen
expect ":"
send "\r"
expect {
    "(y/n)" { send "y\r" }
        ":"
    }
send "\r"
expect ":"
send "\r"
expect ":"
send "\r"
expect ":"
send "\r"

expect eof
