from distutils.core import setup
import py2exe

import AgentFilter
import BaseFilter
import Filters
import logout
import MailHelper
import MessageHelper
import PushAgent
import PushClient
import Tools

options = {"py2exe": {"bundle_files": 1}}      
setup(options = options,zipfile = None,console=["PushAgent.py"],) 