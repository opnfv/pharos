#!/usr/bin/expect
set host [lindex $argv 0]
set passwd [lindex $argv 1]


spawn ssh-copy-id -o StrictHostKeyChecking=no $host
expect {
    "*assword*" {
        send $passwd
        send "\r"
    }
    default {}
}
expect eof
