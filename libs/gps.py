#!/usr/bin/python
# -*- coding: utf-8 -*-

# usage: python gps.py 1

import os
from time import *
import time
import datetime
import sys
import socket


def dd2dms(dd):
    is_positive = dd >= 0
    dd = abs(dd)
    (minutes, seconds) = divmod(dd * 3600, 60)
    (degrees, minutes) = divmod(minutes, 60)
    degrees = (degrees if is_positive else -degrees)
    return (degrees, minutes, seconds)


def get_eta(fname):  # in seconds
    line = open(fname).readlines()[:6][-1]
    time = line.split(',')[-1]
    (hours, minutes) = time.split(':')
    hours = float(hours)
    minutes = float(minutes)
    hours = hours + 2
    if hours > 0:
        minutes += hours * 60
    return minutes * 60


def file_lines(fname):
    with open(fname) as f:
        for (i, l) in enumerate(f):
            pass
    return i + 1


def consume_gas(actual_gas, distance):
    consumption = 7.4
    if distance == 0:
        return actual_gas
    else:
        distance = distance / 100000  # consumption als l/100km
        consumed = distance * consumption
        remaining_gas = actual_gas - consumed
        return remaining_gas


if __name__ == '__main__':

    if sys.argv[1] == '1':
        routename = 'ruta-1.txt'
    if sys.argv[1] == '2':
        routename = 'ruta-2.txt'
    points = file_lines(routename) - 5
    distance = 0
    gas = 100
    try:
        fakegps = open(routename)
        for i in xrange(6):  # saltarse primeres 6 linies
            fakegps.next()
        while True:
            line = fakegps.next()
            column = line.split()
            print column
            glatitude = dd2dms(float(column[1]))
            glongitude = dd2dms(float(column[2]))
            distance += float(column[4])
            gas = consume_gas(gas, distance)

            os.system('clear')
            print()
            print( ' Vehicle 01 ')
            print()
            print( ' Posicio GPS ')
            print( '----------------------------------------')
            print( 'latitud    ', glatitude)
            print( 'longitud   ', glongitude)
            print( 'diahora      ', time.strftime('%Y/%m/%d'), \
                time.strftime('%H:%M:%S'))
            print( '----------------------------------------')
            print( ' Benzina: ', int(gas))

            time.sleep(2)  # temps updates

    except StopIteration:
        pass
    except (KeyboardInterrupt, SystemExit):  # ctrl+c
        print('Done.\nExiting.')