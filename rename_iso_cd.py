#!/usr/bin/python2
# -*- coding: utf-8 -*-

# rename_iso_cd.py: rename the cd image and move it to the iso images dir
# Copyright (C) 2016  Pablo De Nápoli <pdenapo@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Dependencies: svn

from __future__ import print_function

import argparse
import json
import os
import re
import subprocess

if __name__ == '__main__':

    # We parse the command-line arguments

    parser = \
        argparse.ArgumentParser(description='Checkout the ReactOS sources.'
                                )
    parser.add_argument('--revision', dest='revision',
                        help='for which revision? [default=current revision]'
                        )
    parser.add_argument('--config', dest='config_file_name',
                        help='configuration file to read',
                        default='config.json')

    #parser.add_argument('--compile', action='store_const', const=True,
    #                    help='Compile React OS from the sources')

    args = parser.parse_args()

    # We use a configuration file with json format for several configuration parameters.

    if os.path.isfile(args.config_file_name):
        try:
            config = json.load(open(args.config_file_name))
        except ValueError:
            print('Error parsing the configuration file',
                  args.config_file_name)
            sys.exit(3)
    else:
        print('Configuration file', args.config_file_name,
              ' does not exist.')
        sys.exit(4)
        
    build_dir = os.path.abspath(config['reactos_build_dir'])
    src_dir = os.path.abspath(config['reactos_src_dir'])
    iso_images_dir = os.path.abspath(config['iso_images_dir'])
    p = subprocess.Popen(["svnversion",src_dir+"/reactos"], stdout = subprocess.PIPE,stderr = subprocess.PIPE)
    p.wait()
    m = re.match(r'(|\d+M?S?):?(\d+)(M?)S?', p.stdout.read())
    rev = int(m.group(2))
    new_name="bootcd-compiled-"+str(rev)+".iso"
    print(new_name)
    os.rename(build_dir+"/reactos/bootcd.iso",iso_images_dir+"/"+new_name)       

