"""
Crawls the Port tables from Wikipedia
Result is a dict with the port as key
and the name of the service as value
"""
from os import listdir
from re import sub
from requests import get
from bs4 import BeautifulSoup

def minify(name):
  """Removes unnecessary characters from the names"""
  return sub(r'[\[\]0-9]*', '', name)

def get_table_entries(table, ports):
  """Fills the dict with the ports that aren't
  unassigned
  """
  for row in table.find_all('tr')[2:]:
    items = row.find_all('td')

    if items[3].text.encode('utf-8') != b'Unassigned':
      ports[items[0].text.encode('utf-8')] =\
        minify(items[3].text).encode('utf-8')

def crawl_port_dict():
  """Crawls the wikipedia page and calls the
  get_table_entries with the common port table
  and the registered port table
  Returns the final dict"""
  page_html =\
    get('https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers')
  soup = BeautifulSoup(page_html.text, 'html.parser')

  ports = {}

  common_table = soup.find_all('table')[3]
  registered_table = soup.find_all('table')[5]

  get_table_entries(common_table, ports)
  get_table_entries(registered_table, ports)

  return ports

def get_service(port):
  """Checks if given port is in the
  port dict and returns the service name"""
  if port.encode('utf-8') in COMMON_PORTS:
    return COMMON_PORTS[port.encode('utf-8')]
  else:
    return 'Unknown'

def print_to_file(port_dict):
  """writes the key value pairs
  to the file 'portlist.txt in
  assets' """
  with open('../assets/portlist.txt', 'w') as txt_file:
    for key, value in port_dict.items():
      txt_file.write(str(key)[2:-1] + ' ' + str(value)[2:-1] + '\n')

def read_from_file():
  """generates the dict from the file
  portlist.txt"""
  port_dict = {}

  with open('../assets/portlist.txt', 'r') as txt_file:
    for line in txt_file:
      key_value = line.split(' ')
      port_dict[key_value[0].encode('utf-8')] =\
        key_value[1].encode('utf-8')

  return port_dict

def get_port_dict():
  """either crawls the dict from wikipedia
  and writes it to a file for the next use
  or reads the dict from a file"""
  if 'portlist.txt' in listdir('../assets'):
    #read from file
    return read_from_file()
  else:
    port_dict = crawl_port_dict()
    print_to_file(port_dict)

    return port_dict

COMMON_PORTS = get_port_dict()
