#!/usr/bin/expect -f
set timeout 60000

spawn ccdecrypt /root/huge-file/random.cpt
expect "Enter decryption key: " {send "oi\r"}
expect EOF      { send_user $expect_out(buffer) }
