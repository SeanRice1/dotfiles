#!/usr/bin/env python

import os
import glob
import shutil
import errno
import subprocess
import sys

# Check python version, requires python 3
if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
        sys.exit(1)

import pathlib


HOME= os.path.expanduser('~')
HOST_OS = None
SOURCE_DOTS = HOME + '/dotfiles/dots'
SOURCE_SUBS = HOME + '/dotfiles/subs'
SOURCES = [SOURCE_DOTS, SOURCE_SUBS]
DOT_ARCHIVE = HOME + '/.dotArchive/'
EXCLUDE = [".git", ".gitignore", ".gitmodules"]
NO_DOT_PREFIX = []
PRESERVE_EXTENSION = []


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
    
    print ("Archiving %s to %s" % (dest, DOT_ARCHIVE + os.path.basename(dest)))
    shutil.move(dest, DOT_ARCHIVE + os.path.basename(dest))


def  link():
    for source_dir in SOURCES:
        if source_dir == SOURCE_DOTS:
            print ("Linking dotfiles to ~/ ...")
        else: 
            print ("Linking submodules to ~/ ...")

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

                    response = input("Overwrite symbolic link for '%s'? [y/N] " % dotfile)
                    if not response.lower().startswith('y'):
                        print ("Skipping `%s'..." % dotfile)
                        continue

                    force_remove(dotfile)
                else:
                    response = input("Archive '%s' to '%s'? [y/N] " %(dotfile, DOT_ARCHIVE))
                    if not response.lower().startswith('y'):
                        print ("Archiving `%s'..." % dotfile)
                        continue

                    archive(dotfile)

            os.symlink(source, dotfile)
            print ("%s => %s" % (dotfile, source))

def unlink():
    if os.path.exists(os.path.expanduser(DOT_ARCHIVE)):
        # TODO: This does not restore dotfiles that were initially symbolic linked to $HOME
        for source_dir in SOURCES:
           if source_dir == SOURCE_DOTS:
               print ("Removing symlinks to dotfiles in ~/ ...")
           else: 
               print ("Removing symlinks to submodules in ~/ ...")

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

        print("Moving archived files back")
        os.chdir(os.path.expanduser(DOT_ARCHIVE))
        file_refs = pathlib.Path(".").glob("*")
        for file_obj in file_refs:
            archive_path = os.path.join(DOT_ARCHIVE, os.path.basename(str(file_obj)))
            moved_path = os.path.join(HOME, os.path.basename(str(file_obj)))
            print ("Moving '%s' back to '%s'" %(archive_path, moved_path))
            shutil.move(str(file_obj), moved_path)
        
        print("Removing dotArchive directory")
        os.rmdir(os.path.expanduser(DOT_ARCHIVE))
    else:
        print(os.path.expanduser(DOT_ARCHIVE) + " Doesnt exist! Maybe you didnt have any dotfiles before setting up?")


def setup():
    link();

    # Test for vim clipboard 
    if (subprocess.run("vim --version | grep '+clipboards;'", shell=True)).returncode == 1:
        print("To enable clipboard copy and paste within vim, you must have the +clipboards flag enabled within vim")

    #subprocess.run("chsh -s $(which zsh)", shell=True, check=True)
    print("To change your default shell, run: sudo chsh $(which zsh). Remeber you need to restart your shell for this to take effect!")
    subprocess.run("vim +PluginInstall +qall", shell=True, check=True)
    

def main():
    print("======================== Welcome to the dotfile configure-er ========================")
    print("Commands: ")
    print("setup - make sym links within ~/ for all dotfiles and submodules, pre appending a dot. Run setup scripts.")
    print("unlink - remove all symlinks from ~/ to any resources contained in this directory.")
    print("exit - exit the dotfile helper")
    print("=====================================================================================")

    print("OS types: macOS, linux, windows")
    response = input("Please enter which OS you are using: \n")
    print("OS selected: " + response.lower())

    if  response.lower() == "windows":
        print("Sorry windows is not supported yet. Quitting...")
        sys.exit(0)
    elif response.lower() != "macos" and response.lower() != "linux":
        print("Unsupported OS. Qutting...")
        sys.exit(1)
    else:
        HOST_OS=response.lower()

    response = input("What would you like to do? \n")

    while 1:
        if response.lower() == "exit":
            sys.exit(1)
        elif response.lower() == "setup":
            setup()
        elif response.lower() == "unlink":
            unlink()
        else:
            print("Valid options are unlink, setup and exit")

        response = input("Would you like to do anything else? If not, enter exit \n")

if __name__ == '__main__':
    main()
