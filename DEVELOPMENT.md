## Setting up the development environment

Once I've got automated testing working I will document the required setup in detail.

There's quite a lot of setup required.

I don't have access to Windows or Mac/OS, so these instructions assume a Linux environment.

1. You'll need to install freeplane. I'm using version 1.7.2; the test setup will need adjusting if you use another 
version
2. By default, the freeplane scripts are in /home/{user}/.config/freeplane/1.7.x/scripts; you'll need to symlink 
   this to `tests/freeplane/scripts`. The testing process will add a file `test-maps.py`to the init 
   sub-directory directory

