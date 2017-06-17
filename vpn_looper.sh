#!/bin/bash

export PATH=/root/bin/:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
pid=/var/run/vpngate.pid

if [ "$1" = "kill" ]; then
  kill $pid
  exit 0
fi

while true; do
  ping -I tun101 8.8.8.8 -w5 -c1
  if [ $? -eq 0 ]; then
    sleep 28
    continue
  fi

  pkill -f "openvpn --daemon --cd /etc/openvpn --config vpngate.conf"
  sleep 2
  vpngate_fetch.py
  openvpn --daemon --cd /etc/openvpn --config vpngate.conf --log /var/log/openvpn-vpngate.log --writepid $pid
  sleep 10
done

