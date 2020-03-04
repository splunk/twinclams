import datetime

currentDT = datetime.datetime.now()
dstamp = currentDT.strftime("%Y%m%d")
from optparse import OptionParser
import subprocess
import os, base64, difflib
import sys
import re
import itertools

parser = OptionParser(usage="https://www.youtube.com/watch?v=SM5ix55TLbk py2 only for now.")
parser.add_option("-t", dest="input_target", type="string", help="target string for conversion")
parser.add_option("-r", dest="reass_pl_path", type="string",
                  help="Path to reass.pl script (regex assemble) requires libregexp-assemble-perl pkg.")

(options, args) = parser.parse_args()

if not options.input_target:
    print("You gotta tell me what hurts before I can fix it. Give me some input with -t")
    sys.exit(1)

if not options.reass_pl_path or not os.path.exists(options.reass_pl_path):
    print('Point me to the Regex RX script "reass.pl" script included with this file. Also for this to work you need libregexp-assemble-perl')
    sys.exit(1)


import re
import subprocess
domains=[]
f=[]
if os.path.exists(options.input_target) and os.path.isfile(options.input_target):
    f=open(options.input_target).readlines()                          
    f.append("store\n")
else:
    print("couldn't find the file {0}".format(options.input_target))
    sys.exit(1)

def cmd_wrapper(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    return (p.returncode, stdout, stderr)

for entry in f:
    if "." in entry:
        domains.append(r'(?:[^\/<]+\.)?%s(?:\:\d{1,5})?[\s\/<]' % re.escape(entry.strip()))
    else:
        domains.append(r'[^\/<]+\.%s(?:\:\d{1,5})?[\s\/<]' % re.escape(entry.strip()))

fu=open('scratch.txt','w')
for entry in domains:
   fu.write(entry + '\n')
fu.close()

c, out, err = cmd_wrapper("{0} scratch.txt".format(options.reass_pl_path))
print(r'#https://www.youtube.com/watch?v=t08RN2yPJik')
print(r'TwinWave.RemoteTemplateCall.BadDDomainShowdown.{0};Engine:81-255,Target:7;(0&1&2&3);3c72656c6174696f6e73686970::i;7461726765746d6f6465::i;617474616368656474656d706c617465::i;0/\<relationship(?=(?:(?!\/>).)+?targetmode\s*=\s*[\x22\x27]?\s*external)(?=(?:(?!\/>).)+?type\s*=\s*[\x22\x27][^\x22\x27\s]+\/attachedtemplate)(?:(?!\/>).)+?target\s*=\s*[\x27\x22]?\s*(?:https?\x3a|ftp\x3a)[\/]+'.format(dstamp) + r'{0}'.format(out.strip()) + r'/si')

