# reactos-testing-scripts

React OS is a free software project to develop a free clone of MS-Windows.

See: https://www.reactos.org

React OS is still in alpha state, although many things work right now. But it needs a lot of work. I no nothing about the Windows internals, so I try to help by testing it. These are some scripts that I am using to help to test React OS. I share them on github, just in case you find them useful.

* create_reactos_virtual_machine.py

In my opinion, the best way to test react os, is by using a virtual machine. However, downloading the iso file, decompressing it and setting the virtual machine is a rather tedious process. So have developed this script in order to automate it.

This script will atempt to download an official iso file from the React OS 
build bot, uncompress it and create a VirtualBox virtual machine for it. 
You can specify a revision using the --revision parameter. Otherwise it will 
try to get the current revision from the subversion repository.

Some parameters of the virtual machine (like memory_size and disk_size) should be
specified in the configuration file (by default: config.json), as long as
the directory where you want to download the React OS iso images
(iso_images_dir). You can use the command line parameter --config to specify
a different configuration file.




