import datetime

currentDT = datetime.datetime.now()
dstamp = currentDT.strftime("%y%m%d")
from optparse import OptionParser
from collections import OrderedDict
import subprocess
import os, base64, difflib
import sys
import re
import itertools

parser = OptionParser(usage="https://www.youtube.com/watch?v=SM5ix55TLbk py2 only for now.")
parser.add_option("-t", dest="input_target", type="string", help="target string for conversion")
parser.add_option("-i", action="store_true", dest="i", default=False,
                  help="generate base64 case insensitve string generation. Can cause docxrstrgood to have a bad trip.")
parser.add_option("-u", action="store_true", dest="b64u", default=False,
                  help="generate b64 wide strings. Can cause docxrstrgood to have a bad trip.")
parser.add_option("-w", action="store_true", dest="b64w", default=False,
                  help="Make b64 regex optional wide strings... There is some stupidity here as regexp::assemble seems to eat nulls")
parser.add_option("-r", dest="reass_pl_path", type="string",
                  help="Path to reass.pl script (regex assemble) requires libregexp-assemble-perl pkg.")
parser.add_option("-b", action="store_true", dest="b", default=False,
                  help="Disable regex start at word boundary. Likely you want this but sometimes you don't.")
parser.add_option("-z", action="store_true", dest="z", default=False,
                  help="reverse the input string")
parser.add_option("-x", action="store_true", dest="x", default=False,
                  help="don't do base64 strings")
parser.add_option("-e", action="store_true", dest="e", default=False,
                  help="generate char'd excel4 macro matches in any order")

(options, args) = parser.parse_args()
strings = []
if not options.input_target:
    print("You gotta tell me what hurts before I can fix it. Give me some input with -t")
    sys.exit(1)

if options.z:
    tmp_strings = options.input_target.split(",")
    for entry in tmp_strings:
        strings.append(entry[::-1])
else:
    strings = options.input_target.split(",") 
if not options.e:
    if not options.reass_pl_path or not os.path.exists(options.reass_pl_path):
        print('Point me to the Regex RX script "reass.pl" script included with this file. Also for this to work you need libregexp-assemble-perl')
        sys.exit(1)

def prGreen(prt): print("\033[92m {}\033[00m".format(prt))


drfeelgood=("""
https://www.youtube.com/watch?v=SM5ix55TLbk
apt-get install -y libregexp-assemble-perl 
%%%%%%%%%%%%%%%%%%%%%%%%(%%%%%%%%%%%%##%&&%%%%%%%%%%%/#%%%%%%%%%%%%#%%%%%%%%%%%
%%%%%%%##%%(%&%#%%%%%%#%#%%###%#%((//#(&%%%%%%#%%#%%%,%%%%%%%%%%%%%%%%%%%%%%&&&
%%%%%%%%%%%#%%%%%%%%%%%%%%%%%%%%##*/. ,/ /%%%%%%%%%%%/%%%%%%%%%%%%%%%%%%%&%&%&&
%%%%%%%%%%%(%%%%%%%%%%%%%%%%%%%%#(*,   (*#%%&%%%%%%%%(&&&&&%%%%%%%%%&&&&&&&&%
%%%%%%%%%%%(&&%%%%%%%%%%%#%%%%%%%#(.,*/#%(#&%%%%%%%%%*%%%%%%%%%%&&%%&&&&%%&&%
%%%%%%%%%%%(%%%%%%%%%%%%%%(.   ./#/,****.,%%%#.    *#/%%%%%%%%%%%%%%#%%%%&&%%%%
%%%%%%%%%%%(%%%%%%%%%#          ,#,*.  /#.%(#(.        .%%%%%%%%%%%%%%%%%&%%%
%%%%%%%%%%%/%%%%%#            ,#%%#*.   . %%%%%(     .     ,#%%%%%%%%%%%%%%%%%%
,,,,,,,,,*.         . .        *., .      .  .*..      .        ,,,,...... ,.,,
%%%%%%%%%%%*%/                        ,,,   ./  .         . .  .%%%%%%%%%%%%%%%
%%%%%%%%%%#/%%%%.%%%( .      *    .   .,.          .   . ,*#(.%%%#%%%%%%%%%%%%%
%%%%%%%%%%%*%%%%%%%.(%..         ...,   ,  ..          .#( %%%%(%%%%%%%%%%%%%%%
%%%%%%%%%%%*%%%%%%%%% #%%(* ...   .  *. ..  ,. ,* *,*#%% %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%/%%%%%%%%%%%%%%#% %%%,##*        (.%%%.%%%%%%%%%%%%%%%%%%&%%%%%%%%%%
%%%%%%%%%%%*%%%%%%%%%%%%%#%%%*%%%%,     (.  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%*%%%%%%%%%%%%%%%#%%%%%#   .,  ,. #%%%%%%%%%%%%%%%##%##%%#%%##%#%####
%%%%%%%%%%%*%%%%%%%%%%%%%&%%%%%%%%/    .  /%%%%%%%%%%&%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%/%%%%%%%%%%%%%%%%%%%%%%.     .  /%%%%%%%%%&%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%*%%%%%%%%%%%%%%%%%(. .  ,  .%@,  #%%%%%%%%&%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%,%%%%%%%%%%%%%%%%%%  ,.  ..*/#.. #%%%%%%%%&%%%%%%%%%%%%%%#%%%%%%%%%%
%%%%%%%%%%%/%%%%%%%%%%%%%%#%%%/ *, .      .#%%%%%%%%%%%%%%%%%%%%%%%%#%%%%%%%%%%
%%%%%%%%%%%/(%%%%%%%%%%%%%%%(%#(...**.  , ..%%%%%%%%%%%%%%%%%%%%%%%%#%%%%%%%%%%
""")
prGreen(drfeelgood)


def cmd_wrapper(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    return (p.returncode, stdout, stderr)


def b64(encode):
    return base64.b64encode(encode)


def longest(a, b):
    match = difflib.SequenceMatcher(None, a, b)
    m = match.find_longest_match(0, len(a), 0, len(b))
    return a[m.a:m.a + m.size]


def ude(string_to_encode):
    string_tmp = ''
    for c in string_to_encode:
        string_tmp += '%s\x00' % c
        string_to_encode = string_tmp.rstrip('\x00')
    return string_to_encode


def b64u(encode):
    encode = ude(encode)
    return base64.b64encode(encode)


if options.e:
    matches = OrderedDict() 
    for s in strings:
        sl = s
        su = s
        if options.i:
            sl = s.lower()
            su = s.upper()
        i = 0
        while i < len(s):
            if sl[i] == su[i]:
                match = "1E{0}00416F00".format(sl[i].encode('hex'))
                if match not in matches:
                    matches[match] = {}
                    matches[match]['cnt']=0
                    matches[match]['alt']="416F0007020400010000{0}".format(sl[i].encode('hex'))
                else:
                    matches[match]['cnt'] = matches[match]['cnt'] + 1
            else:
                match = "1E({0}|{1})00416F00".format(sl[i].encode('hex'),su[i].encode('hex'))
                if match not in matches:
                    matches[match] = {}
                    matches[match]['cnt']=0
                    matches[match]['alt']="416F0007020400010000({0}|{1})".format(sl[i].encode('hex'),su[i].encode('hex'))
                else:
                    matches[match]['cnt'] = matches[match]['cnt'] + 1
            i = i + 1
        rulep1='TwinWave.EvilDoc.DOCXSTRGOOD.AOEX4.BITSNEEDEDFOR.{0}.{1};Engine:81-255,Target:2;((0|1|2)&(3|('.format(s.upper().replace(';', '').replace(' ',''), dstamp)
        rulep2='8500{6}0201{1-8192}18001700200000010700000000000000000000013A::aw;8500{6}0101{1-8192}18001700200000010700000000000000000000013A::aw;8500{6}0001{1-8192}18001700200000010700000000000000000000013A::aw'
        if options.i:
            rulep2 = rulep2 + ";{0}::awi".format(s.encode('hex'))
        else:
            rulep2 = rulep2 + ";{0}::aw".format(s.encode('hex'))
        cnt = 4
        for entry in matches:
            if matches[entry]['cnt'] > 0:
                if cnt == 4:
                    rulep1=rulep1 + '(({0}|{1})>{2})'.format(cnt,cnt+1,matches[entry]['cnt'])
                else:
                    rulep1=rulep1 + '&(({0}|{1})>{2})'.format(cnt,cnt+1,matches[entry]['cnt'])                    
            else:
                if cnt == 4:
                    rulep1=rulep1 + '({0}|{1})'.format(cnt,cnt+1)
                else:
                    rulep1=rulep1 + '&({0}|{1})'.format(cnt,cnt+1)

            rulep2 = rulep2 + ";{0};{1}".format(entry,matches[entry]['alt'])    
            cnt = cnt + 2
        rulep1 = rulep1 + ')));'
        print(rulep1 + rulep2)
    sys.exit(0)

for s in strings:
    sl = s
    su = s
    if options.i:
        sl = s.lower()
        su = s.upper()
    if options.b:
        regex = '(?:'
    else:
        regex = '\\b(?:'
    i = 0
    while i < len(s):
        if i == 0:
            hexregex = ''
            regex += "(?:" + re.escape(s[0]) + "(?!" + re.escape(s[1:])
            if sl[0] == su[0]:
                regex += ")|(?:Chr[WB]?\\$?\\s*\\(+\\s*(?:Abs\\$?\\s*\\(+\\s*-?)?)?{0}(?:\.\d+)*?\\s*\\)*)|{1})".format(
                    ord(s[0]), s[0].encode('hex'))
                hexregex += "|{0}".format(s[0].encode('hex'))
            else:
                regex += ")|(?:Chr[WB]?\\$?\\s*\\(*\\s*(?:Abs\\$?\\s*\\(+\\s*-?)?)?(?:{0}|{1})(?:\.\d+)*?\\s*\\)*|(?:{2}|{3}))".format(
                    ord(sl[0]), ord(su[0]), su[0].encode('hex'), sl[0].encode('hex'))
                hexregex += "|(?:{0}|{1})".format(su[0].encode('hex'), sl[0].encode('hex'))
        else:
            if sl[i] == su[i]:
                regex += "[\\x22\\x27+,\\s&^_\\r\\n]*(?:(?:Chr[WB]?\\$?\\s*\\(+\\s*(?:Abs\\$?\\s*\\(+\\s*-?)?)?{0}(?:\.\d+)*?\\s*\\)*|{1}|{2})".format(
                    ord(s[i]), re.escape(s[i]), s[i].encode('hex'))
                hexregex += "{0}".format(s[i].encode('hex'))
            else:
                regex += "[\\x22\\x27+,\\s&^_\\r\\n]*(?:(?:Chr[WB]?\\$?\\s*\\(*\\s*(?:Abs\\$?\\s*\\(+\\s*-?)?)?(?:{0}|{1})(?:\.\d+)*?\\s*\\)*|{2}|(?:{3}|{4}))".format(
                    ord(sl[i]), ord(su[i]), re.escape(s[i]), sl[i].encode('hex'), su[i].encode('hex'))
                hexregex += "(?:{0}|{1})".format(sl[i].encode('hex'), su[i].encode('hex'))
        i = i + 1

        
    try:
        m=re.compile(regex)
    except Exception as e:
        #print("Hold my beer lets try to fix this")
        regex = regex + ")"
    try:
        m = re.compile(regex)
        #print("fixed it")
    except:
        print("Will is probably an idiot, unable to make a regex that compiles properly")
        sys.exit(1)
    if not options.z:
        if su[0] == sl[0]:
            print('TwinWave.EvilDoc.DOCXSTRGOOD.{0}.{1};Engine:81-255,Target:2;(0&(1|2|3|4|5|6)&7);0:417474726962757465205642::i;{2}::i;{3}::i;{4}::i;{5}::i;{6}::i;{7};(1|2|3|4|5|6)/{8}/si'.format(
                s.upper().replace(';', ''), dstamp, s[0].encode('hex').encode('hex'),
                s[0].encode('hex') + s[1].encode('hex'), (s[0] + '\x27').encode('hex'), (s[0] + '\x22').encode('hex'),
                "chr".encode('hex'), str(ord(s[0])).encode('hex'), regex))
        else:
            print('TwinWave.EvilDoc.DOCXRSTRGOOD.{0}.{1};Engine:81-255,Target:2;(0&(1|2|3|4|5|6|7|8)&9);0:417474726962757465205642::i;{2}::i;{3}::i;{4}::i;{5}::i;{6}::i;{7}::i;{8};{9};(1|2|3|4|5|6|7|8)/{10}/si'.format(
                s.upper().replace(';', ''), dstamp, sl[0].encode('hex').encode('hex'), su[0].encode('hex').encode('hex'),
                s[0].encode('hex') + s[1].encode('hex'), (s[0] + '\x27').encode('hex'), (s[0] + '\x22').encode('hex'),
                str(ord(sl[0])).encode('hex'), str(ord(su[0])).encode('hex'), "chr".encode('hex'), regex))
    else:
        if options.b:
            if su[0] == sl[0]:
                print('TwinWave.EvilDoc.DOCXSTRGOOD.{0}.{1};Engine:81-255,Target:2;(((0&1)|(0&(2|3|4|5|6|7)&8)));0:417474726962757465205642::i;{2}::i;{3}::i;{4}::i;{5}::i;{6}::i;{7}::i;{8};(2|3|4|5|6|7)/{9}/si'.format(
                    s.upper().replace(';', '')[::-1] + ".REV", dstamp, s.encode('hex'),s[0].encode('hex').encode('hex'),
                    s[0].encode('hex') + s[1].encode('hex'), (s[0] + '\x27').encode('hex'), (s[0] + '\x22').encode('hex'),
                    "chr".encode('hex'), str(ord(s[0])).encode('hex'), regex))
            else:
                print('TwinWave.EvilDoc.DOCXRSTRGOOD.{0}.{1};Engine:81-255,Target:2;(((0&1)|(0&(2|3|4|5|6|7|8|9)&10)));0:417474726962757465205642::i;{2}::i;{3}::i;{4}::i;{5}::i;{6}::i;{7}::i;{8}::i;{9};{10};(2|3|4|5|6|7|8|9)/{11}/si'.format(
                    s.upper().replace(';', '')[::-1] + ".REV", dstamp, sl.encode('hex'),sl[0].encode('hex').encode('hex'), su[0].encode('hex').encode('hex'),
                    s[0].encode('hex') + s[1].encode('hex'), (s[0] + '\x27').encode('hex'), (s[0] + '\x22').encode('hex'),
                    str(ord(sl[0])).encode('hex'), str(ord(su[0])).encode('hex'), "chr".encode('hex'), regex))                  
        else:            
            if su[0] == sl[0]:
                print('TwinWave.EvilDoc.DOCXSTRGOOD.{0}.{1};Engine:81-255,Target:2;(((0&1)|(0&(2|3|4|5|6|7)&8)));0:417474726962757465205642::i;(B){2}::i;(B){3}::i;(B){4}::i;(B){5}::i;(B){6}::i;(B){7}::i;(B){8};(2|3|4|5|6|7)/{9}/si'.format(
                    s.upper().replace(';', '')[::-1] + ".REV", dstamp, s.encode('hex'),s[0].encode('hex').encode('hex'),
                    s[0].encode('hex') + s[1].encode('hex'), (s[0] + '\x27').encode('hex'), (s[0] + '\x22').encode('hex'),
                    "chr".encode('hex'), str(ord(s[0])).encode('hex'), regex))
            else:
                print('TwinWave.EvilDoc.DOCXRSTRGOOD.{0}.{1};Engine:81-255,Target:2;(((0&1)|(0&(2|3|4|5|6|7|8|9)&10)));0:417474726962757465205642::i;(B){2}::i;(B){3}::i;(B){4}::i;(B){5}::i;(B){6}::i;(B){7}::i;(B){8}::i;(B){9};(B){10};(2|3|4|5|6|7|8|9)/{11}/si'.format(
                    s.upper().replace(';', '')[::-1] + ".REV", dstamp, sl.encode('hex'),sl[0].encode('hex').encode('hex'), su[0].encode('hex').encode('hex'),
                    s[0].encode('hex') + s[1].encode('hex'), (s[0] + '\x27').encode('hex'), (s[0] + '\x22').encode('hex'),
                    str(ord(sl[0])).encode('hex'), str(ord(su[0])).encode('hex'), "chr".encode('hex'), regex))            
    if options.x:
        continue 
    if options.i:
        smap = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in s)))
    else:
        smap = [s]
    hexstrings = []
    nstrings = []
    prefix_dict = {}
    prefix_list = []
    f = open("b64dump.txt", "w")
    for e in smap:
        string_to_encode = e  # put your string here
        for t in [3, 4, 5]:
            init_string1 = b64(os.urandom(t) + string_to_encode + os.urandom(6))  # initialize first string
            for i in range(100):
                init_string2 = b64(os.urandom(t) + string_to_encode + os.urandom(6))
                init_string1 = longest(init_string1, init_string2)
            hexstrings.append(init_string1[::-1].encode("hex"))
            nstrings.append(init_string1)
            if options.b64u:
                init_string1 = b64u(os.urandom(t) + string_to_encode + os.urandom(6))  # initialize first string
                for i in range(100):
                    init_string2 = b64u(os.urandom(t) + string_to_encode + os.urandom(6))
                    init_string1 = longest(init_string1, init_string2)
                hexstrings.append(init_string1[::-1].encode("hex"))
                nstrings.append(init_string1)

    nstrings2 = []
    nstrings = list(set(nstrings))
    nstrings.sort()
    f2 = open('scratch.txt', 'wb')
    for entry in nstrings:
        if not prefix_dict.get(entry[0:2], []):
            prefix_dict[entry[0:2]] = []
            prefix_dict[entry[0:2]].append(entry)
        else:
            prefix_dict[entry[0:2]].append(entry)
        f.write(entry + ",")
        f2.write("{0}\n".format(entry))
    f2.close()
    f.close()

    c, out, err = cmd_wrapper("{0} scratch.txt".format(options.reass_pl_path))
    i = 1
    for entry in prefix_dict:
        if len(prefix_dict[entry]) == 1:
            print('TwinWave.EvilDoc.DOCXRSTRGOOD.{0}.{1}B64.{2};Engine:81-255,Target:0;((0|(1&(2|3))|(4&(5|6)))&7);0:417474726962757465205642::i;0:D0CF11E0A1B11AE1;5c564245372e444c4c::aw;5c564245362e444c4c::aw;0,1:3c3f786d6c;2f7061636b6167652f323030362f6d657461646174612f636f72652d70726f70657274696573::i;2f6f6666696365446f63756d656e742f323030362f657874656e6465642d70726f70657274696573::i;{3}::aw'.format(
                s.upper().replace(';', ''), dstamp, i, prefix_dict[entry][0].encode('hex')))
        else:
            prefix_list.append(entry)
            f = open('scratch.txt', 'w')
            for m in prefix_dict[entry]:
                if options.b64w:
                    f.write("{0}\n".format("\\\x00?".join(list(m))))
                else:
                    f.write("{0}\n".format(m))
            f.close()
            c, out, err = cmd_wrapper("{0} scratch.txt".format(options.reass_pl_path))
            print('TwinWave.EvilDoc.DOCXRSTRGOOD.{0}.{1}B64.{2};Engine:81-255,Target:0;((0|(1&(2|3))|(4&(5|6)))&7&8);0:417474726962757465205642::i;0:D0CF11E0A1B11AE1;5c564245372e444c4c::aw;5c564245362e444c4c::aw;0,1:3c3f786d6c;2f7061636b6167652f323030362f6d657461646174612f636f72652d70726f70657274696573::i;2f6f6666696365446f63756d656e742f323030362f657874656e6465642d70726f70657274696573::i;{3}::aw;7/{4}/'.format(
                s.upper().replace(';', ''), dstamp, i, entry.encode('hex'), out.strip().replace("\?", "\\x00?")))
        i = i + 1
