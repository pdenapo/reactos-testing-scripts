#!/usr/bin/python
# -*- coding: utf-8 -*-

# rts: React OS Testing Script
# Script to checkout the React OS sources and compile them
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
import os
import json
import sys
import xml.etree.ElementTree as etree


def svn_checkout_reactos_trunk(revision,src_dir):
    """ This function runs the "svn ckeckout" command to get the React OS sources """

    print('Running svn checkout for revision', revision, 'into', src_dir)
    subprocess.call([
        'svn',
        'checkout',
        '--revision',
        revision,
        'svn://svn.reactos.org/reactos/trunk/reactos',
        src_dir,
        ])

def svn_update_reactos_trunk(revision,src_dir):
    """ This function runs the "svn update" to update the React OS sources to a given revision """

    print('Running svn update for revision', revision, 'into', src_dir)
    subprocess.call([
        'svn',
        'upate',
        '--revision',
        revision,
        src_dir,
        ])


def get_svn_info_xml_file():
    """ This function runs the "svn info" command on the React OS subversion repository, with outpoot in xml format in the file svn_info.xml in the current directory. """

    svn_info_xml_file = open('svn_info.xml', 'w')
    print('Running svn info for getting the current React OS version')
    subprocess.call(['svn', 'info', '--xml',
                    'svn://svn.reactos.org/reactos'],
                    stdout=svn_info_xml_file)
    svn_info_xml_file.close()


def get_current_revision():
    """ This function gets the current revision number from the React OS subversion repository."""

    get_svn_info_xml_file()
    tree = etree.parse('svn_info.xml')
    root = tree.getroot()
    entry = root.find('entry')
    revision = entry.get('revision')
    return revision


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
                        
    #parser.add_argument('command')
    
    args = parser.parse_args()

    # We use a configuration file with json format for several configuration parameters.

    if os.path.isfile(args.config_file_name):
        config = json.load(open(args.config_file_name))
    else:
        print('Configuration file', args.config_file_name,
              ' does not exist.')
        sys.exit(3)

    revision = args.revision

    if revision == None:
        revision = get_current_revision()
        
    src_dir = config['reactos_src_dir']    
    if os.path.exists(config['reactos_src_dir']+'/trunk'):
       svn_update_reactos_trunk(revision,src_dir)
    else:
       svn_checkout_reactos_trunk(revision,src_dir)
