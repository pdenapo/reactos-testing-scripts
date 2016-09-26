#!/usr/bin/python
# -*- coding: utf-8 -*-

# Script to create a virtual machine for React OS under VirtualBox
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

# Dependencies: wget, 7z, VBoxManage

from __future__ import print_function
import subprocess
import os
import sys
import xml.etree.ElementTree as etree
import json
import virtualbox
from virtualbox import library as vbl
import argparse


def get_svn_info_xml_file():
    """This function runs the "svn info" command on the React OS subversion repository, with outpoot in xml format in the file svn_info.xml in the current directory."""

    svn_info_xml_file = open('svn_info.xml', 'w')
    print('Running svn info for getting the current React OS version')
    subprocess.call(['svn', 'info', '--xml',
                    'svn://svn.reactos.org/reactos'],
                    stdout=svn_info_xml_file)
    svn_info_xml_file.close()


def get_current_revision():
    """This function gets the current revision number from the React OS subversion repository."""

    get_svn_info_xml_file()
    tree = etree.parse('svn_info.xml')
    root = tree.getroot()
    entry = root.find('entry')
    revision = entry.get('revision')
    return revision


def get_iso_file(revision, dir):
    """
     This function gets the compressed iso image corresponding to a given revision from the official ReactOS build bot (using wget),
     to a given directory and uncompress it using 7z.
    """

    iso_filename = 'bootcd-' + revision + '-dbg.iso'
    iso_path = dir + '/' + iso_filename
    compressed_iso_filename = 'bootcd-' + str(revision) + '-dbg.7z'
    compressed_iso_path = dir + '/' + compressed_iso_filename
    iso_download_url = 'http://iso.reactos.org/bootcd/' \
        + compressed_iso_filename
    iso_file_already_exists = os.path.isfile(iso_path)
    if iso_file_already_exists:
        print('File', iso_path, 'already exists')
        if os.path.getsize(iso_path) == 0:
            print('File', iso_path, 'has zero size. Deleting!')
            os.remove(iso_path)
            iso_file_already_exists = False

    if not iso_file_already_exists:
        compressed_iso_file_already_exists = \
            os.path.isfile(compressed_iso_path)
        if compressed_iso_file_already_exists:
            print('Compressed iso file', compressed_iso_path,
                  'already exists')
            if os.path.getsize(compressed_iso_path) == 0:
                print('File', compressed_iso_path,
                      'has zero size. Deleting!')
                os.remove(compressed_iso_path)
                compressed_iso_file_already_exists = False

        if not compressed_iso_file_already_exists:
            print('Downloading compressed iso file ',
                  compressed_iso_path)
            try:
                subprocess.check_call(['wget', '--output-document='
                        + compressed_iso_path, iso_download_url])
            except subprocess.CalledProcessError:
                print('Downloading compressed iso file for revision '
                      + revision + ' failed.')
                sys.exit(1)
        print('Decompressing iso file')
        try:
            subprocess.check_call(['7z', '-o' + dir, 'e',
                                  compressed_iso_path])
        except subprocess.CalledProcessError:
            print('Uncompressing the iso file failed.')
            sys.exit(1)
        os.remove(compressed_iso_path)
    return iso_path


def create_virtual_disk(path, size):
    """ This function creates a virtual disk of a given size using VBoxManage """

    print('Creating a virtual disk at', path)
    subprocess.call([
        'VBoxManage',
        'createhd',
        '--filename=' + path,
        '--format',
        'vdi',
        '--size',
        str(size),
        '--variant',
        'fixed',
        ])


def create_virtual_machine(revision, iso_image):
    """Creates the virtual machine for a given revision."""

    vbox = virtualbox.VirtualBox()
    session = virtualbox.Session()
    vm_dir = \
        vbl.ISystemProperties.default_machine_folder.fget(vbox.system_properties)
    print('Default Machine Folder:', vm_dir)
    machine_name = 'React OS-r' + str(revision)
    machine_path = vm_dir + '/' + machine_name
    if os.path.exists(machine_path):
        print('The virtual machine already exists at', machine_path)
        sys.exit(4)
    print('Creating the new virtual machine at', machine_path)
    virtual_disk_path = machine_path + '/' + 'disk.vdi'
    create_virtual_disk(virtual_disk_path, config['disk_size'])
    try:
        vm = vbox.create_machine('', machine_name, [''], 'WindowsXP', ''
                                 )
    except vbl.VBoxErrorFileError:
        print('Virtual machine', machine_name, 'already exists !')
        sys.exit(2)
    vbox.register_machine(vm)
    vm = vbox.find_machine(machine_name)
    device_type = vbl.DeviceType.hard_disk
    access_mode = vbl.AccessMode.read_write
    force_new_uuid = False
    medium = vbox.open_medium(virtual_disk_path, device_type,
                              access_mode, force_new_uuid)
    device_type2 = vbl.DeviceType.dvd
    access_mode2 = vbl.AccessMode.read_only
    force_new_uuid2 = True
    medium2 = vbox.open_medium(iso_path, device_type2, access_mode2,
                               force_new_uuid2)
    vm.lock_machine(session, vbl.LockType.write)
    mutable = session.machine
    mutable.add_storage_controller('IDE', vbl.StorageBus.ide)
    mutable.memory_size = config['memory_size']
    mutable.attach_device('IDE', 0, 0, device_type, medium)
    mutable.attach_device('IDE', 0, 1, device_type2, medium2)
    mutable.save_settings()
    session.unlock_machine()
    print('The virtual machine is ready!')


if __name__ == '__main__':

    # We parse the command-line arguments

    parser = \
        argparse.ArgumentParser(description='Create a VirtualBox virtual machine for a given revision of React-OS.'
                                )
    parser.add_argument('--revision', dest='revision',
                        help='for which revision? [default=current revision]'
                        )
    parser.add_argument('--config', dest='config_file_name',
                        help='configuration file to read',
                        default='config.json')
    parser.add_argument('--iso-image', dest='iso_image',
                        help='iso-image for the CD-Rom of the virtual machine'
                        )

    args = parser.parse_args()

    # We use a configuration file with json format for several configuration parameters.

    if os.path.isfile(args.config_file_name):
        config = json.load(open(args.config_file_name))
    else:
        print('Configuration file', args.config_file_name,
              ' does not exist.')
        sys.exit(3)

    revision = args.revision

    if args.iso_image:
        iso_path = args.iso_image
        if revision == None:
            revision = 'Unknown'
    else:
        if revision == None:
            revision = get_current_revision()
        print('Creating a virtual machine for revision', revision)
        dir = config['iso_images_dir']
        iso_path = get_iso_file(revision, dir)

    create_virtual_machine(revision, iso_path)

