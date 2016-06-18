#!/usr/bin/env python

import os
import errno
import sys
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

def printData():
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

  print "First Name: {0}".format(firstname)
  print "Last Name: {0}".format(lastname)
  print "Full Name: {0}".format(fullname)
  print "Company: {0}".format(company)
  print "Email: {0}".format(email)
  print "Username: {0}".format(username)

def main(argv):
  """Main program.
  Parse args, call procs.
  @see http://stackoverflow.com/a/4028943/871793.
  """

  if argv is None:
    argv = sys.argv

  if len(argv) > 0:
    name = argv[0]
    getData(name)
  else:
    printData()

  return 0

if __name__ == "__main__":
  main(sys.argv[1:])
