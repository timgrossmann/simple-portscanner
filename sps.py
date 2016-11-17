"""
Simple Portscanner
  Usage:
    ./sps.py...
      ... hostname -> 192.168.178.1, 192.168.178.5-10, 192.115.112.0/24 {required}
        ... -P or --ports 80, 90-100 {optional, default: all}
        ... -F or --file output.txt, /home/Desktop/output.txt {optional, default: no file output}

    e.g.
      ./sps.py 192.168.128-150 -P 1-500 -F output.txt   <- Will scan ports 1-500 on IP range 128-150
                                                            and will write the results to output.txt
                                                            in the same folder
"""

