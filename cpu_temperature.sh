#!/bin/bash

CPU_TEMPERATURE=`cat /sys/class/thermal/thermal_zone0/temp`

mysql homeHK -u user_homeHK -pp8PYvkZiTsKm -e "INSERT INTO cpu_temperature VALUES(\"`date \"+%Y-%m-%d %H:%M:%S\"`\", $CPU_TEMPERATURE/1000);"
