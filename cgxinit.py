#!/usr/bin/env python
import sys
import os
import argparse

####
#
# Enter other desired optional system modules here.
#
####

import json

####
#
# End other desired system modules.
#
####

# Import CloudGenix Python SDK
try:
    import cloudgenix
    jdout = cloudgenix.jdout
    jd = cloudgenix.jd
except ImportError as e:
    cloudgenix = None
    sys.stderr.write("ERROR: 'cloudgenix' python module required. (try 'pip install cloudgenix').\n {0}\n".format(e))
    sys.exit(1)

# Check for cloudgenix_settings.py config file in cwd.
sys.path.append(os.getcwd())
try:
    from cloudgenix_settings import CLOUDGENIX_AUTH_TOKEN

except ImportError:
    # if cloudgenix_settings.py file does not exist,
    # Get AUTH_TOKEN/X_AUTH_TOKEN from env variable, if it exists. X_AUTH_TOKEN takes priority.
    if "X_AUTH_TOKEN" in os.environ:
        CLOUDGENIX_AUTH_TOKEN = os.environ.get('X_AUTH_TOKEN')
    elif "AUTH_TOKEN" in os.environ:
        CLOUDGENIX_AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
    else:
        # not set
        CLOUDGENIX_AUTH_TOKEN = None

try:
    # Also, seperately try and import USERNAME/PASSWORD from the config file.
    from cloudgenix_settings import CLOUDGENIX_USER, CLOUDGENIX_PASSWORD

except ImportError:
    # will get caught below
    CLOUDGENIX_USER = None
    CLOUDGENIX_PASSWORD = None


# Handle differences between python 2 and 3. Code can use text_type and binary_type instead of str/bytes/unicode etc.
if sys.version_info < (3,):
    text_type = unicode
    binary_type = str
else:
    text_type = str
    binary_type = bytes


####
#
# Start custom modifiable code
#
####

GLOBAL_MY_SCRIPT_NAME = "Example Script"
GLOBAL_MY_SCRIPT_VERSION = "v1.0"


def my_function(sdk):
    """
    Example of a custom function. Gets sites object and jdout to str, then print.
    :param sdk: Authenticated CloudGenix SDK Constructor.
    :return: No Return
    """

    print(jdout(sdk.get.sites()))
    return


def my_function_lower(sdk):
    """
    Example of a custom function. Gets sites object jdout to str, call .lower(), and print.
    :param sdk: Authenticated CloudGenix SDK Constructor.
    :return: No Return
    """

    print(jdout(sdk.get.sites()).lower())
    return

####
#
# End custom modifiable code
#
####


# Start the script.
def go():
    """
    Stub script entry point. Authenticates CloudGenix SDK, and gathers options from command line to run do_site()
    :return: No return
    """

    # Parse arguments
    parser = argparse.ArgumentParser(description="{0} ({1})".format(GLOBAL_MY_SCRIPT_NAME, GLOBAL_MY_SCRIPT_VERSION))

    ####
    #
    # Add custom cmdline argparse arguments here
    #
    ####

    custom_group = parser.add_argument_group('custom_args', 'SIP ALG')
    custom_group.add_argument("--enable", help="enable SIP ALG",
                              default=None, action="store_true",dest="enable_alg")
    custom_group.add_argument("--disable", help="disable SIP ALG",
                              default=None, action="store_false",dest="enable_alg")
    custom_group.add_argument("--all", help="apply to all IONs",
                              default=None, action="store_true",dest="scope_all")
    custom_group.add_argument("--list", help="list ALGs on all IONs",
                              default=None, action="store_true",dest="list")
    custom_group.add_argument("--site", help="site name",
                              default=None, action="store",dest="site_name")
    custom_group.add_argument("--element", help="ion name",
                              default=None, action="store",dest="element_name")

    ####
    #
    # End custom cmdline arguments
    #
    ####

    # Standard CloudGenix script switches.
    controller_group = parser.add_argument_group('API', 'These options change how this program connects to the API.')
    controller_group.add_argument("--controller", "-C",
                                  help="Controller URI, ex. https://api.elcapitan.cloudgenix.com",
                                  default=None)

    login_group = parser.add_argument_group('Login', 'These options allow skipping of interactive login')
    login_group.add_argument("--email", "-E", help="Use this email as User Name instead of cloudgenix_settings.py "
                                                   "or prompting",
                             default=None)
    login_group.add_argument("--password", "-PW", help="Use this Password instead of cloudgenix_settings.py "
                                                       "or prompting",
                             default=None)
    login_group.add_argument("--insecure", "-I", help="Do not verify SSL certificate",
                             action='store_true',
                             default=False)
    login_group.add_argument("--noregion", "-NR", help="Ignore Region-based redirection.",
                             dest='ignore_region', action='store_true', default=False)

    debug_group = parser.add_argument_group('Debug', 'These options enable debugging output')
    debug_group.add_argument("--sdkdebug", "-D", help="Enable SDK Debug output, levels 0-2", type=int,
                             default=0)

    args = vars(parser.parse_args())

    sdk_debuglevel = args["sdkdebug"]

    # Build SDK Constructor
    if args['controller'] and args['insecure']:
        sdk = cloudgenix.API(controller=args['controller'], ssl_verify=False)
    elif args['controller']:
        sdk = cloudgenix.API(controller=args['controller'])
    elif args['insecure']:
        sdk = cloudgenix.API(ssl_verify=False)
    else:
        sdk = cloudgenix.API()

    

    # check for region ignore
    if args['ignore_region']:
        sdk.ignore_region = True

    # SDK debug, default = 0
    # 0 = logger handlers removed, critical only
    # 1 = logger info messages
    # 2 = logger debug messages.

    if sdk_debuglevel == 1:
        # CG SDK info
        sdk.set_debug(1)
    elif sdk_debuglevel >= 2:
        # CG SDK debug
        sdk.set_debug(2)

    # login logic. Use cmdline if set, use AUTH_TOKEN next, finally user/pass from config file, then prompt.
    # figure out user
    if args["email"]:
        user_email = args["email"]
    elif CLOUDGENIX_USER:
        user_email = CLOUDGENIX_USER
    else:
        user_email = None

    # figure out password
    if args["password"]:
        user_password = args["password"]
    elif CLOUDGENIX_PASSWORD:
        user_password = CLOUDGENIX_PASSWORD
    else:
        user_password = None

    # check for token
    if CLOUDGENIX_AUTH_TOKEN and not args["email"] and not args["password"]:
        sdk.interactive.use_token(CLOUDGENIX_AUTH_TOKEN)
        if sdk.tenant_id is None:
            print("AUTH_TOKEN login failure, please check token.")
            sys.exit(1)

    else:
        while sdk.tenant_id is None:
            sdk.interactive.login(user_email, user_password)
            # clear after one failed login, force relogin.
            if not sdk.tenant_id:
                user_email = None
                user_password = None

    ####
    #
    # Do your custom work here, or call custom functions.
    #
    ####

    return sdk,args

    ####
    #
    # End custom work.
    #
    ####


if __name__ == "__main__":
    go()
