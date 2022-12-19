#!/usr/bin/env python3

""" 
MFA TOTP code generation

Code tested with python3
python3 ./getTotp.py --help

The first time you roll this code it will ask you to enter the OTP key
For more information see

You need to have the following libraries installed pyotp, keyring and pyperclip

    pip3 install --user pyotp keyring pyperclip


@Author: Mike Naso
@Date: Mar 11, 2022
@version: 0.5.4

"""
__author__="Mike Naso"
__license__="GPL"
__version__="0.5.4"
__maintainer__="Mike Naso"
__date__="2022-03-11"


import keyring
import pyotp
import datetime, time
import argparse 
import pyperclip
import os

def enter_key( args ):
    _key=input('Enter the TOTP KEY =>')
    keyring.set_password("system", "gettotp_code_%s" % args.service, _key)
    return _key

def range_limit_loop(arg):
    try:
        _value=int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Value must be an integer")
    if _value < 2 or _value > 30:
        raise argparse.ArgumentTypeError("Value must be between 2 and 30")
    return _value

parser = argparse.ArgumentParser(add_help=False)
for grp in parser._action_groups:
    if grp.title == 'optional arguments':
        grp.title = 'arguments'

parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help="This help")
parser.add_argument('-n', '--new_code', action="store_true", help="Asked to enter a new code" )
parser.add_argument('-l', '--loop', default=-1, help="Value between 2 and 30 seconds", type=range_limit_loop )
parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
parser.add_argument('-o', '--only_code', action="store_true", help="Display only the code" )
parser.add_argument('-c', '--clipboard', action="store_true", help="Copy to clipboard" )
parser.add_argument('-s', '--service', help="Choose the service description in one word no accent, can remain empty", type=str, default='default')
parser.add_argument('-b', '--beep', action="store_true", help="Beep only if -c option is used" )
args = parser.parse_args()


# Reading code from the system password manager, this will not work if keyring is not installed
try:
    _key=keyring.get_password("system", "gettotp_code_%s" % args.service)
except keyring.errors.KeyringError:
    print( "I did not find a keyring manager")
    exit()
except:
    _key=enter_key( args )

if None is _key or args.new_code :
    _key=enter_key( args )
    
totp = pyotp.TOTP( _key )
while True:
    _time_remaining = totp.interval - datetime.datetime.now().timestamp() % totp.interval

    # S'il reste moins de 2 secondes, lire le prochain code
    if _time_remaining<2:
        _code=totp.at(datetime.datetime.now().timestamp()+2)
        _time_remaining=30
    else:
        try:
            _code=totp.now()
        except:
            print("Sorry the code is not valid")
            keyring.delete_password("system", "gettotp_code_%s" % args.service)
            exit(1)

    if args.only_code:
        print(_code, end="\r")
    elif args.clipboard:
	# If fail we are try the xclip command, I saw some problem on some linux distrubution
        try:
            pyperclip.copy( _code )
        except:
            os.system("""echo %s | xclip -sel c""" %(_code))
        if args.beep:
            os.system("echo '\a'") #;sleep 0.2;" * x)
            #beep(3)
    else:
        print("Current OTP key: %s Time left %d " % (_code, _time_remaining), end='\r')
        if -1 == args.loop:
            print("\n");
            break;
    if args.loop > 2:
        time.sleep(args.loop)
    else:
        break
