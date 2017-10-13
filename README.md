# Simple Portscanner
Easy to use, minimalistic port scanner

### Simple Portscanner

Scans the given host for open ports on which attacks could be
performed.  
```bash
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
```
