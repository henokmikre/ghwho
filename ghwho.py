#!/usr/bin/env python

import sys
from getopt import getopt, GetoptError
import os
import json
from os.path import expanduser
import pycurl

home = expanduser("~")
gitconfig = home + '/.gitconfig'
mefile = home + '/.ghuser.json'

class User:
  def __init__(self):
    if (os.path.isfile(gitconfig) == False):
      exit("{0} does not exist. Please create one and try again.".format(gitconfig))

    # Read .gitconfig data.
    options = parse_config(gitconfig)

    self.name = options['name']
    self.email = options['email']
    self.first = options['name'].split()[0]
    self.last = options['name'].split()[1]
    self.user = options['user']

    # Just for kicks, get the GitHub user data and save it to 'mefile' path.
    userdata = self.getUser()

    self.company = userdata['company']

  def getUser(self):
    """Reads GitHub user data from local file, if it exists.
    If file does not exists, it creates one by calling GitHub API.
    """
    # If file does not exist, create it.
    if (os.path.isfile(mefile) == False):
      print "{0} does not exist. Creating one.".format(mefile)
      self.getData()

    # Instantiate dictionary.
    udata = {}

    with open(mefile) as obj:
      data = json.load(obj)

    udata['company'] = data['company']

    # The following is extra data for demo purposes.
    udata['username'] = data['login']
    udata['fullname'] = data['name']
    udata['firstname'] = udata['fullname'].split()[0]
    udata['lastname'] = udata['fullname'].split()[1]
    udata['company'] = data['company']
    udata['website'] = data['blog']
    udata['domain'] = data['blog'].split('//')[1]
    # This is a hacky method of getting email address. Gitconfig is better.
    email = udata['firstname'].lower() + '@' + udata['domain']

    return udata

  def getData(self):
    """Gets GitHub data.
    @see http://stackoverflow.com/a/23718539/871793.
    """
    # Check if user json file exists.
    if os.path.isfile(mefile):
      printData()
    else:
      c = pycurl.Curl()
      c.setopt(c.URL, 'https://api.github.com/users/' + self.user)
      with open(mefile, 'w') as f:
        c.setopt(c.WRITEFUNCTION, f.write)
        c.perform()

def parse_config(filename):
  """Parses config file.
  @see http://www.decalage.info/python/configparser.
  """
  COMMENT_CHAR = '#'
  OPTION_CHAR =  '='

  options = {}
  f = open(filename)
  for line in f:
    # First, remove comments:
    if COMMENT_CHAR in line:
      # split on comment char, keep only the part before
      line, comment = line.split(COMMENT_CHAR, 1)
    # Second, find lines with an option=value:
    if OPTION_CHAR in line:
      # split on option char:
      option, value = line.split(OPTION_CHAR, 1)
      # strip spaces:
      option = option.strip()
      value = value.strip()
      # store in dictionary:
      options[option] = value
  f.close()
  return options

def printData(uvar = None):
  """Prints data from local file.
  """

  # Instantiate user object.
  u = User()

  # Print user property.
  if uvar:
    if uvar == "name":
      print u.name
    elif uvar == 'email':
      print u.email
    if uvar == 'first':
      print u.first
    elif uvar == 'last':
      print u.last
    elif uvar == 'company':
      print u.company
  else:
    usage()

def usage():
  print "Usage: %s -u username -p [user-property]\n" % sys.argv[0]
  print "\t name      Print full name"
  print "\t email     Print email address"
  print "\t first     Print first name"
  print "\t last      Print last name"
  print "\t company   Print company name"
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
