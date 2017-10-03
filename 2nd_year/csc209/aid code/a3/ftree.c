#include <stdio.h>
// Add your system includes here.
#include <dirent.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "sys/stat.h"
#include "unistd.h"
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include "ftree.h"
#include "hash.h"

// Helpers, you can find them after copy_ftree.
int check_existence(const char* path);
int file_size(const char* filename);
char* file_hash(const char* filename);
void file_overwrite(const char* src, const char* dest);
int is_same_file(const char* name1, const char* name2);
char* build_path(const char* path, const char* name);
const char* extract_path(const char* fname);

// Copy files from a source file tree to a destination file tree.
// Both src and dest should be unchangable path name.
int copy_ftree(const char* src, const char* dest) {

	// Get infomations form destination.
	struct stat dest_info;
	int dest_status = lstat(dest, &dest_info);

	// Get infomations form source.
	struct stat src_info;
	int src_status = lstat(src, &src_info);

	// Check existence.
	if (dest_status < 0 || src_status < 0) {
		perror("lstat");
		exit(1);
	}

    // I do not call helper for above is because I need these info for further
    // file/directory checking and permissions copy.

	// Check if destination is normal file.
    // Even prof assume that dest should be a directory,
    // I still try to handle this in case user giving a wrong input accidently.
	if (S_ISREG(dest_info.st_mode)) {
		printf("Destination cannot be a file.\n");
		exit(1);
	}

	// If destination is a directory and source is a file.
    // We do not include soft link checking by assignment requirments.
	if (S_ISREG(src_info.st_mode)) {

		DIR * dirp = opendir(dest);

		// Check if dest cannot open.
		if (dirp == NULL) {
			perror("opendir");
			exit(1);
		}

		// dest should be a path, src may be a path or just a name of a file.
        // For example, src can be "a" or "test/a".
        // So need to extract src to make sure it is a reasonable input.
        // For example, if there is an empty directory "dest", and a file "a"
        // under a directory "test". If we call "fcopy test/a dest", the result
        // should be an "a" in "dest" (i.e. dest/a), not "dest/test/a".
		char* dest_file = build_path(dest, extract_path(src));

        // If there are 2 files have same sizes and hash values,
        // then they are same files, we do not need to overwrite them.
        // Else (include file not existing case), we need to overwrite the one
        // under dest.
		if (!is_same_file(src, dest_file)) {
			file_overwrite(src, dest_file);
		}

		free(dest_file);

		// Single file copy success.
		return 1;

	// If source is a directory. Need recursion.
	} else {
		int count = 1;
		struct dirent *dp;
		DIR * dirp = opendir(src);

		// Check if src cannot open.
		if (dirp == NULL) {
			perror("opendir");
			exit(1);
		}

		int permissions = src_info.st_mode & 0777;
		// Make a directory named src in destination.
		// It should fail if the directory already exists.
		// Know this from stackoverflow.
		char* dest_dir = build_path(dest, extract_path(src));
		mkdir(dest_dir, permissions);

		// Get the first file (i.e. dp) in src.
		dp = readdir(dirp);

		// Go over all files in src.
		while (dp != NULL) {

			// If the file (i.e. dp) in src is a directory.
			if (dp->d_type == DT_DIR) {

                //Ignore all "." and ".."
				if (dp->d_name[0] != '.') {

					// Create process.
					int process = fork();
					// Check error.
					if (process < 0) {
						perror("fork");
						exit(1);
					}

					// If process is a child process.
					if (process == 0) {
						int c;
						char* src_dir = build_path(src, dp->d_name);
						c = copy_ftree(src_dir, dest_dir);
						free(src_dir);
						exit(c);

					// If process is a parent process.
					} else {
						int status;
						// check error, wait child process
						if (wait(&status) == -1) {
							perror("wait");
							exit(1);
						}
						count += WEXITSTATUS(status);
					}
				}

			// If the file (i.e. dp) in src is a regular file.
			} else {
				char* src_file = build_path(src, dp->d_name);
				copy_ftree(src_file, dest_dir);
				free(src_file);
			}
			dp = readdir(dirp);
		}
		free(dest_dir);
		return count;
	}
}


// A helper to check if this file exist.
int check_existence(const char* path) {

	// Get infomations form input.
	struct stat info;
	int status = lstat(path, &info);

	// Check existence.
	if (status < 0) {
		return 0;
	}

	return 1;
}

// A helper to get the size of a file.
int file_size(const char* filename) {

	struct stat buf;
	stat(filename, &buf);
	int size = buf.st_size;

	return size;
}

// A helper to get the hash value of a file.
char* file_hash(const char* filename) {

	FILE * file = fopen(filename, "r");

	// Check if file cannot open.
	if (file == NULL) {
		perror("openfile");
		exit(1);
	}

	char* result = hash(file);
	fclose(file);

	return result;
}

// A helper to overwrite one file to another.
void file_overwrite(const char* src, const char* dest) {

	FILE * src_file = fopen(src, "r");
	FILE * dest_file = fopen(dest, "w");

	// Check if file cannot open.
	if (src_file == NULL || dest_file == NULL) {
		perror("openfile");
		exit(1);
	}

    // // Check if the src cannot be wrote, then the dest should contain nothing.
    // if (access(src, W_OK) < 0) {
    //     return;
    // }

	char temp;
	int length = file_size(src);
	int i = 0;

	// Read from src and write to dest, one by one.
	for (; i < length; i++) {
		fread(&temp, 1, 1, src_file);
		fwrite(&temp, 1, 1, dest_file);
	}

	fclose(src_file);
	fclose(dest_file);
}

// A helper to check if two files are the same.
int is_same_file(const char* name1, const char* name2) {

    // If one of these 2 is not exist, they are definitly not same.
	if (!check_existence(name1) || !check_existence(name2)) {
		return 0;
	}

	int same_size_flag = (file_size(name1) == file_size(name2));
	int same_hash_flag = (file_hash(name1) == file_hash(name2));

    // They are same iff their sizes and hash values are same.
	return same_size_flag && same_hash_flag;
}

// A helper to build a path for the name. Like A2.
char* build_path(const char* path, const char* name) {

	char* path_name = malloc(strlen(path) + strlen(name) + 2);
	strcpy(path_name, path);
	strcat(path_name, "/");
	strcat(path_name, name);
	strcat(path_name, "\0");

	return path_name;
}

// A helper for getting a file name from a path. Like A2.
const char* extract_path(const char* fname) {
	char* last_slash = strrchr(fname, '/');
	return last_slash ? last_slash + 1 : fname;
}
