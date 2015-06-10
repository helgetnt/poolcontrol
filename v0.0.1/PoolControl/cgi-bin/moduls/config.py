#!/usr/bin/env python
settings = dict(
                mf = '',
                datum = '',
                data = '',
                data_file = '',
                data_dir = '/ramfs/tp/',
                filelist = '',
                menulist = '',
                Pumpe_an   = "40",
                Pumpe_aus  = "1",
                Pumpe_auto = "20",
                V0   = "1",
                V50  = "5",
                V100 = "10"
               )
table=''
chart=''

global dat
global plog
global vlog
dat  = sorted([fn for fn in os.listdir(settings['data_dir']) if any([fn.endswith('.dat')])])
plog = sorted([fn for fn in os.listdir(settings['data_dir']) if any([fn.endswith('.plf')])])
vlog = sorted([fn for fn in os.listdir(settings['data_dir']) if any([fn.endswith('.vlf')])])
