"hard links" will build a same inode for a file and links to a the
file (hard node cannot link a directory). i.e. Processes are unique but
hard links are same in system. So if there is a hard link in the directory,
then some processes will still detect the same contents when both hard
links or the original file show up. It is hard to make differentiate
between the original file and hard links because we cannot check the
differentiation of inodes between different process.
