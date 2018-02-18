# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

import sys
from diyidan.jobs import route

j = sys.argv[1]

job = route.get(j)

if __name__ == '__main__':
    if job:
        job().run()
    else:
        print 'not found'
