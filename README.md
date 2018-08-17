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
 python setup.py
 chsh -s $(which zsh)
 vim +PluginInstall +qall
 ```
Then logout and log back in! 
