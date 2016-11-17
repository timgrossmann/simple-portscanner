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
        ... -F or --file output.txt, /home/Desktop/output.txt
                        {optional, default: no file output}

    e.g.
      ./sps.py 192.168.128-150 -P 1-500 -F output.txt
                    ^
                    |
        Will scan ports 1-500 on IP range 128-150
        and will write the results to output.txt
        in the same folder
"""

import socket
from argparse import ArgumentParser

socket.setdefaulttimeout(2)

PARSER = ArgumentParser()
PARSER.add_argument('hosts', help='which hosts will be scanned')
PARSER.add_argument('-P', '--ports', help='which ports will be scanned',
                    default='all')
PARSER.add_argument('-F', '--file', help='write results to given file',
                    default=None)

ARGS = PARSER.parse_args()
#from here, ARGS.hosts, ports and file

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
    print('multiple')
  else:
    return [host_str]

  return hosts

print(get_hosts('192.168.178.188'))
#print(get_hosts('192.168.178.188-192'))
#get_hosts('192, 168')

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
    print('Error: "%s" occured.' % (str(e)))
    return 0
