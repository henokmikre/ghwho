#!/usr/bin/env python

import sys
from getopt import getopt, GetoptError
import os
import json
from os.path import expanduser
import pycurl

home = expanduser("~")
mefile = home + '/.ghuser.json'

def getData(name):
  """Gets GitHub data.
  @see http://stackoverflow.com/a/23718539/871793.
  """
  # Check if user json file exists.

  if os.path.isfile(mefile):
    printData()
  else:
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://api.github.com/users/' + name)
    with open(mefile, 'w') as f:
      c.setopt(c.WRITEFUNCTION, f.write)
      c.perform()

def printData(uvar = None):
  """Prints data from local file.
  """
  if (os.path.isfile(mefile) == False):
    exit("{0} does not exist.".format(mefile))

  with open(mefile) as obj:
    data = json.load(obj)

  username = data['login']
  fullname = data['name']
  firstname = fullname.split()[0]
  lastname = fullname.split()[1]
  company = data['company']
  website_domain = data['blog'].split('//')[1]
  email = firstname.lower() + '@' + website_domain

  # Print user property.
  if uvar:
    if uvar == 'first':
      print firstname
    elif uvar == 'last':
      print lastname
    elif uvar == 'email':
      print email
    elif uvar == "full":
      print fullname
  else:
    usage()

def usage():
  print "Usage: %s -u username -p [user-property]\n" % sys.argv[0]
  print "\t first     Print first name"
  print "\t last      Print last name"
  print "\t email     Print email address"
  print "\t full      Print full name"
  print "\n"

def main(argv):
  """Main program.
  Parse args, call procs.
  @see http://stackoverflow.com/a/4028943/871793.
  @see http://www.cyberciti.biz/faq/python-command-line-arguments-argv-example/.
  """

  username = ''
  uvar = ''

  if argv is None:
    argv = sys.argv

  if len(argv) > 0:
    try:
      myopts, args = getopt(argv,"u:p:")

      for o, a in myopts:
        if o == '-u':
          username = a
        elif o == '-p':
          uvar = a
        else:
          usage()

      printData(uvar)
    except GetoptError as e:
      print "Invalid option.\n"
      usage()
      exit(1)
    except:
      print "Unexpected error:", sys.exc_info()[0]
      raise
  else:
    usage()

  return 0

if __name__ == "__main__":
  main(sys.argv[1:])
