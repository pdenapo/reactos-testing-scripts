#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Script to checkout the React OS sources
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
import subprocess
import argparse

def checkout_reactos_trunk(revision):
    """ This function runs the "svn info" command on the React OS subversion repository, with outpoot in xml format in the file svn_info.xml in the current directory."""

    global config
    print('Running svn checkout for revision',revision,'into',config["reactos_src_dir"])
    subprocess.call(['svn', 'checkout','--revision',revision, 'svn://svn.reactos.org/reactos/trunk/reactos',config["reactos_src_dir"]])
    

if __name__ == '__main__':

    # We parse the command-line arguments

    parser = \
        argparse.ArgumentParser(description='Create a VirtualBox virtual machine for a given revision of React-OS.'
                                )
    parser.add_argument('--revision', dest='revision',
                        help='for which revision? [default=current revision]',
                        default='HEAD'
                        )
    parser.add_argument('--config', dest='config_file_name',
                        help='configuration file to read', default='config.json'
                        )

    args = parser.parse_args()
    
    # We use a configuration file with json format for several configuration parameters.

    if os.path.isfile(args.config_file_name):
        config = json.load(open(args.config_file_name))
    else:
        print('Configuration file',args.config_file_name,' does not exist.')
        sys.exit(3)
  
    revision = args.revision
     
    checkout_reactos_trunk(revision)
