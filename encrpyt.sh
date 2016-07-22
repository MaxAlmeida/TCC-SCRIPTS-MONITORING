#!/usr/bin/expect -f
set timeout 6000

spawn ccrypt /root/huge-file/random
expect "Enter encryption key: " {send "oi\r"}
expect "Enter encryption key: (repeat) " {send "oi\r"}
expect EOF      { send_user $expect_out(buffer) }

