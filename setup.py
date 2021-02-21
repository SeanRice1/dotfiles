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
SOURCE_DOTS = pathlib.Path(HOME, 'dotfiles/dots')
SOURCE_SUBS = pathlib.Path(HOME, 'dotfiles/subs')
SOURCES = [SOURCE_DOTS, SOURCE_SUBS]
DOT_ARCHIVE = pathlib.Path(HOME, '.dotArchive/')
EXCLUDE = [".git", ".gitignore", ".gitmodules"]
NO_DOT_PREFIX = []
PRESERVE_EXTENSION = []
HOST_OS = None


def force_remove(path):
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path, False)
    else:
        os.unlink(path)


def is_link_to(link, dest):
    resolved_link = os.readlink(link)

    if resolved_link == dest:
        return True
    return False


def archive(path):
    DOT_ARCHIVE.mkdir(exist_ok=True)
    archived_path = pathlib.Path(DOT_ARCHIVE, path.name) 
    print ("Archiving %s to %s" % (path, archived_path))
    shutil.move(path, archived_path)

def _add_dot(path):
    if path.name not in NO_DOT_PREFIX:
        return pathlib.Path(path.parent, "." + path.name)
    else:
        return path

def _safe_link(source_path, dest_path):
    dest_path = _add_dot(dest_path)

    if dest_path.exists():
        # Path exists, and its a sym link
        if os.path.islink(dest_path):
            if is_link_to(dest_path, source_path):
                # Its a sym link created by this program, already linked
                return
             
            response = input("Overwrite symbolic link for '%s'? [y/N] " % dest_path)
            if response.lower().startswith('y'):
                # Remove sym link in HOME dir
                force_remove(dest_path)
            else:
                print ("Skipping `%s'..." % source_path)
                return
        else:
            response = input("Archive '%s' to '%s'? [y/N] " %(dest_path, DOT_ARCHIVE))
            if response.lower().startswith('y'):
                archive(dest_path)
            else:
                print ("Archiving `%s'..." % dest_path)
                return

    # Files archived, should be safe to avoid overwriting anything
    if not dest_path.exists():
        dest_path.symlink_to(source_path)
        print ("%s => %s" % (source_path, dest_path))
    else:
        print("There was an error linking %s" % source_path)


def  link(dots_arr, subs_arr):
    # Link dot files
    for filename in dots_arr:
        source_dotfile_path = pathlib.Path(SOURCE_DOTS, filename)
        if source_dotfile_path.exists():
            home_dot_path = pathlib.Path(HOME, filename)
            _safe_link(source_path=source_dotfile_path, dest_path=home_dot_path)
        else:
            print("%s doesnt exist, maybe there is a typo?" %(source_dotfile_path))

    # Link sub dirs 
    for dir_name in subs_arr:
        source_dir_path = pathlib.Path(SOURCE_SUBS, dir_name)
        if source_dir_path.exists():
            dest_path = pathlib.Path(HOME, source_dir_path.stem)
            _safe_link(source_path=source_dir_path, dest_path=dest_path)
        else:
            print("%s doesnt exist, maybe there is a typo?" %(source_dir_path))

    print("Done linking files")

def unlink():
    if os.path.exists(os.path.expanduser(DOT_ARCHIVE)):
        # TODO: This does not restore dotfiles that were initially symbolic linked to $HOME
        # TODO: This doesnt remove files that didnt exist initially 

        # Remove symlinks in HOME for files in archive, then move archived files back to HOME
        objects_in_archive = DOT_ARCHIVE.glob("*")
        for obj in objects_in_archive:
            home_obj = pathlib.Path(HOME, obj.name)
            if home_obj.exists():
                if os.path.islink(home_obj):
                    #if is_link_to(home_obj, source): TODO
                    force_remove(home_obj)
                    # Move original archived object back HOME
                    print ("Moving '%s' back to '%s'" %(obj, home_obj))
                    shutil.move(obj, home_obj)
                else:
                    print("Looks like %s is no longer a symlink. Maybe something changed? You have to manually de-archive this file" % obj)
            else:
                print("Looks like %s no longer links to the dotfile directory. Maybe something changed? You have to manually de-archive this file" % obj)
        
        print("Removing dotArchive directory")
        os.rmdir(os.path.expanduser(DOT_ARCHIVE))
    else:
        print(os.path.expanduser(DOT_ARCHIVE) + " Doesnt exist! Maybe you didnt have any dotfiles before setting up?")


def setup():
    print("Files available to link: ")
    dot_files_included = SOURCE_DOTS.glob("*")
    dot_files_stem_arr = []
    for file_obj in dot_files_included:
        print(file_obj.stem)
        dot_files_stem_arr.append(file_obj.stem)

    files_wanted_to_link = input("Which files do you want to link (type filenames with spaces between)? If all, type 'A'\n")
    # TODO this is lazy, fix this
    if files_wanted_to_link.lower().startswith('a'):
        arr_files_to_link = dot_files_stem_arr
    else:
        arr_files_to_link = files_wanted_to_link.split()

    dot_files_included = SOURCE_SUBS.glob("*")
    dot_dir_stem_arr = []
    for file_obj in dot_files_included:
        print(file_obj.stem)
        dot_dir_stem_arr.append(file_obj.stem)

    dirs_wanted_to_link = input("Which directories do you want to link (type names with spaces between)? If all, type 'A'\n")
    if dirs_wanted_to_link.lower().startswith('a'):
        arr_dirs_to_link = dot_dir_stem_arr 
    else:
        arr_dirs_to_link = dirs_wanted_to_link.split()

    link(dots_arr=arr_files_to_link, subs_arr=arr_dirs_to_link)

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
