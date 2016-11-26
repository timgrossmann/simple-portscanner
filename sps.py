#!/usr/bin/env python3

"""
Simple Portscanner
  Scans the given host for open ports on which attacks could be
  performed.

  Usage:
    ./sps.py...
      ... hostname -> 192.168.178.1 ; "192.168.178.1, 192.168.178.5"
                        (single)            (multiple ! use "")
                      192.168.178.5-10
                        (range)                 {required}

        ... -P or --ports 80 ; "80, 85" ; 90-100 {optional, default: all}

    e.g.
      ./sps.py 192.168.128-150 -P 1-500
                    ^
                    |
        Will scan ports 1-500 on IP range 128-150
"""

import socket
from argparse import ArgumentParser
from util.portlist_gen import COMMON_PORTS

socket.setdefaulttimeout(2)

PARSER = ArgumentParser()
PARSER.add_argument('hosts', help='which hosts will be scanned')
PARSER.add_argument('-P', '--ports', help='which ports will be scanned',
                    default='all')

ARGS = PARSER.parse_args()
#from here, ARGS.hosts, ports

def get_hosts(host_str):
  "extracts all the hosts into a list of hosts"
  hosts = []

  if '-' in host_str:
    split_hosts = host_str.split('-')
    split_start = split_hosts[0].split('.')

    start = int(split_start[-1])
    end = int(split_hosts[1])

    for num in range(start, end):
      hosts.append('.'.join(split_start[:-1]) + '.' + str(num))

    return hosts
  elif ',' in host_str:
    split_hosts = host_str.split(', ')
    for num in split_hosts:
      hosts.append(num)
  else:
    return [host_str]

  return hosts

def get_ports(port_str):
  "extracts all the ports into a list of ports"
  ports = []

  if '-' in port_str:
    split_ports = port_str.split('-')
    split_start = split_ports[0].split('.')

    start = int(split_start[-1])
    end = int(split_ports[1])

    for num in range(start, end):
      ports.append(str(num))

    return ports
  elif ',' in port_str:
    split_ports = port_str.split(', ')
    for num in split_ports:
      ports.append(num)
  else:
    return [port_str]

  return ports

def test_port(host, port):
  """Tests the given hosts port
  returns 1 if port is open else 0
  """
  curr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
    curr_socket.connect((host, port))
    return 1
  except socket.gaierror as g_e:
    print('No such host found: %s: "%s"' % (host, str(g_e)))
    return 0
  except socket.timeout as t_e:
    print('Couln\'t connect to host in time: "%s"' % (str(t_e)))
    return 0
  except socket.error as e_e:
    print('Error: "%s" occured.' % (str(e_e)))
    return 0

for host in get_hosts(ARGS.hosts):
  ports = get_ports(ARGS.ports)
  print(host)
  if len(ports) > 0:
    for port in ports:
      print('Port:' + port + ('open' if test_port(host, port) else 'closed'))
  else:
    for port in COMMON_PORTS:
      print('Port:' + port + ('open' if test_port(host, port) else 'closed'))