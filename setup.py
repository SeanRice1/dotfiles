#!/usr/bin/env python

import os
import glob
import shutil
import errno
import subprocess


HOME= os.path.expanduser('~')
SOURCE_DOTS = HOME + '/dotfiles/dots'
SOURCE_SUBS = HOME + '/dotfiles/subs'
SOURCES = [SOURCE_DOTS, SOURCE_SUBS]
DOT_ARCHIVE = HOME + '/.dotArchive/'
EXCLUDE = [".git", ".gitignore", ".gitmodules"]
NO_DOT_PREFIX = []
PRESERVE_EXTENSION = [
]


def force_remove(path):
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path, False)
    else:
        os.unlink(path)


def is_link_to(link, dest):
    is_link = os.path.islink(link)
    is_link = is_link and os.readlink(link).rstrip('/') == dest.rstrip('/')
    return is_link


def archive(dest):
    try:
        os.mkdir(DOT_ARCHIVE)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    
    print "Archiving %s to %s" % (dest, DOT_ARCHIVE + os.path.basename(dest))
    shutil.move(dest, DOT_ARCHIVE + os.path.basename(dest))


def  link():
    for source_dir in SOURCES:
        if source_dir == SOURCE_DOTS:
            print "Linking dotfiles to ~/ ..."
        else: 
            print "Linking submodules to ~/ ..."

        os.chdir(os.path.expanduser(source_dir))
        for filename in [file for file in glob.glob('*') if file not in EXCLUDE]:
            dotfile = filename
            if filename not in NO_DOT_PREFIX:
                dotfile = '.' + dotfile
            if filename not in PRESERVE_EXTENSION:
                dotfile = os.path.splitext(dotfile)[0]
            dotfile = os.path.join(os.path.expanduser('~'), dotfile)
            source = os.path.join(source_dir, filename).replace('~', '.')

            # Check that we aren't overwriting anything
            if os.path.lexists(dotfile):
                
                if os.path.islink(dotfile):
                    if is_link_to(dotfile, source):
                        continue

                    response = raw_input("Overwrite file `%s'? [y/N] " % dotfile)
                    if not response.lower().startswith('y'):
                        print "Skipping `%s'..." % dotfile
                        continue

                    force_remove(dotfile)
                else:
                    response = raw_input("Archive `%s'? [y/N] " % dotfile)
                    if not response.lower().startswith('y'):
                        print "Archiving `%s'..." % dotfile
                        continue

                    archive(dotfile)

            os.symlink(source, dotfile)
            print "%s => %s" % (dotfile, source)

def unlink():
    for source_dir in SOURCES:
        if source_dir == SOURCE_DOTS:
            print "Removing symlinks to dotfiles in ~/ ..."
        else: 
            print "Removing symlinks to submodules in ~/ ..."

        os.chdir(os.path.expanduser(source_dir))
        for filename in [file for file in glob.glob('*') if file not in EXCLUDE]:
            dotfile = filename
            if filename not in NO_DOT_PREFIX:
                dotfile = '.' + dotfile
            if filename not in PRESERVE_EXTENSION:
                dotfile = os.path.splitext(dotfile)[0]
            dotfile = os.path.join(os.path.expanduser('~'), dotfile)
            source = os.path.join(source_dir, filename).replace('~', '.')

            if os.path.lexists(dotfile):
                if os.path.islink(dotfile):
                    if is_link_to(dotfile, source):
                        force_remove(dotfile)


def setup():
    subprocess.Popen("chsh -s $(which zsh)")
    subprocess.Popen("vim +PluginInstall +qall")
    print("Logout and log back in for changes to take effect!")
    

def main():
    print("link - make sym links within ~/ for all dotfiles and submodules, pre appending a dot.")
    print("unlink - remove all symlinks from ~/ to any resources contained in this directory.")
    print("setup - run script to set up dotfile requirements and dependencies.")
    print("exit - exit the dotfile helper")
    response = raw_input("What would you like to do? \n")

    while 1:
        if response.lower() == "exit":
            break
        elif response.lower() == "setup":
            setup()
        elif response.lower() == "link":
            link()
        else:
            print("Valid options are link, unlink, setup and exit")

        response = raw_input("Would you like to do anything else? If not, enter exit \n")

if __name__ == '__main__':
    main()
