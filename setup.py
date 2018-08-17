#!/usr/bin/env python

import os
import glob
import shutil
import errno

HOME= os.path.expanduser('~')
SOURCE_DOTS = HOME + '/dotfiles/dots'
SOURCE_SUBS = HOME + '/dotfiles/subs'
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


def symlink_dots():
    os.chdir(os.path.expanduser(SOURCE_DOTS))
    for filename in [file for file in glob.glob('*') if file not in EXCLUDE]:
        dotfile = filename
        if filename not in NO_DOT_PREFIX:
            dotfile = '.' + dotfile
        if filename not in PRESERVE_EXTENSION:
            dotfile = os.path.splitext(dotfile)[0]
        dotfile = os.path.join(os.path.expanduser('~'), dotfile)
        source = os.path.join(SOURCE_DOTS, filename).replace('~', '.')
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
                archive(dotfile)

        os.symlink(source, dotfile)
        print "%s => %s" % (dotfile, source)

def symlink_subs():
    os.chdir(os.path.expanduser(SOURCE_SUBS))
    for filename in [file for file in glob.glob('*') if file not in EXCLUDE]:
        dotfile = filename
        if filename not in NO_DOT_PREFIX:
            dotfile = '.' + dotfile
        if filename not in PRESERVE_EXTENSION:
            dotfile = os.path.splitext(dotfile)[0]
        dotfile = os.path.join(os.path.expanduser('~'), dotfile)
        source = os.path.join(SOURCE_SUBS, filename).replace('~', '.')
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
                archive(dotfile)

        os.symlink(source, dotfile)
        print "%s => %s" % (dotfile, source)


def main():
    symlink_dots()
    symlink_subs()

if __name__ == '__main__':
    main()
