# Some nice dotfiles
Dotfiles (and submodules) for vim, git, and zsh. This works on all *nix OS and doesnt require any fancy dependencies (just python).

The objective here was to keep things nice, simple, and transparent. 

## Features
### vim
Uses [Vundle](https://github.com/VundleVim/Vundle.vim) as a plugin manager and comes with a few plugins. Comes with a nice skin, and logical defaults like using 4 spaces instead of a tab. Some of the normal vimrc config I stole from the [Ultimate Vim configuration](https://github.com/amix/vimrc)

Refer to [Vundle](https://github.com/VundleVim/Vundle.vim) on how to install more plugins (its super easy)

### zsh
Sets zsh to the default shell, and uses the [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh) zsh framework. Looks good, is more secure, and has some nice features. Take a look at the cheatsheet [here](https://github.com/robbyrussell/oh-my-zsh/wiki/Cheatsheet).

### git 
Just some per user specifications

## Follow these steps to get started 
Make sure you have the following things already installed
1. git
2. vim
3. python
4. zsh

Then run these commands...

 ```
 git clone --recurse-submodules https://github.com/SeanRice1/dotfiles ~/dotfiles
 cd ~/dotfiles
 ./setup.py
 chsh -s $(which zsh)
 vim +PluginInstall +qall
 ```
Then logout and log back in! 

When I get around to it, I will be adding dotfiles for VScode, linting, and others. Feel free to fork.
