# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import os
import ConfigParser

environment = os.getenv('HUADU_ENV')
base_dir = '%s%s%s%s%s' % (os.path.dirname(__file__), os.sep, '..', os.sep, 'conf')

if environment == 'prod':
    website_conf_file = 'website.conf'
else:
    website_conf_file = 'website_dev.conf'

cf = ConfigParser.ConfigParser()
cf.read(os.path.join(base_dir, website_conf_file))

website_config = dict(cf.items('app'))

website_config['process'] = int(website_config['process'])
website_config['debug'] = bool(int(website_config['debug']))
website_config['autoreload'] = bool(int(website_config['autoreload']))
website_config['xsrf_cookies'] = bool(int(website_config['xsrf_cookies']))
website_config['compress_response'] = bool(int(website_config['compress_response']))
