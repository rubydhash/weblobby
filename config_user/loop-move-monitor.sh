#!/bin/bash

sleep 5

while [ true ]; do
  /usr/local/bin/move-to-next-monitor 
  /usr/local/bin/move-to-first-monitor
  sleep 5
done
