#include "ftree.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <arpa/inet.h>


/* Accept a connection. Note that a new file descriptor is created for
 * communication with the client. The initial socket descriptor is used
 * to accept connections, but the new socket is used to communicate.
 * Return the new client's file descriptor or -1 on error.
 */
int accept_connection(int fd, struct connection *connections) {
    int user_index = 0;
    while (user_index < MAX_CONNECTIONS && connections[user_index].sock_fd != -1) {
        user_index++;
    }

    int client_fd = accept(fd, NULL, NULL);
    if (client_fd < 0) {
        perror("server: accept");
        close(fd);
        exit(1);
    }

    if (user_index == MAX_CONNECTIONS) {
        fprintf(stderr, "server: max concurrent connections\n");
        close(client_fd);
        return -1;
    }

    connections[user_index].sock_fd = client_fd;
    connections[user_index].state = AWAITING_TYPE;
    return client_fd;
}

// read a int from fd, if read data bytes not equal to sizeof int,
// will return -1, else save data to the pointer and return num of bytes read
int read_int_from(int fd, int *data)
{
    uint32_t n_data = -1;
    int num_read = read(fd, &n_data, sizeof(uint32_t));
    if (num_read != sizeof(uint32_t)) {
        return -1;
    }

    *data = ntohl(n_data);
    return num_read;
}

// read len bytes data to the buffer,
// if can't get the data, return -1
// else return num of data read
int read_buffer_from(int fd, char *buf, int len)
{
    int num_read = read(fd, buf, len);
    if (num_read != len) {
        return -1;
    }
    return num_read;
}

// write buffer to file
int write_to_file(char *path, char *buf, int len) 
{
    FILE *fp = fopen(path, "w");
    int ret = -1;
    if (fp != NULL) {
        int num_write = fwrite(buf, 1, len, fp);
        if (num_write != len) {
            perror("error write");
        }
        ret = 0;
        fclose(fp);
    }

    return ret;
}

/* Read a message from client_index and echo it back to them.
 * Return the fd if it has been closed or 0 otherwise.
 */
int read_from(int client_index, struct connection *connections) 
{
    int fd = connections[client_index].sock_fd;
    int state = connections[client_index].state;

    switch (state) {
        case AWAITING_TYPE:
            if (read_int_from(fd, &connections[client_index].req.type) <= 0) {
                return fd;
            }
            break;
        case AWAITING_PATH:
            if (read_buffer_from(fd, connections[client_index].req.path, MAXPATH) < 0) {
                return fd;
            }
            break;
        case AWAITING_SIZE:
            if (read_int_from(fd, &connections[client_index].req.size) <= 0) {
                return fd;
            }
            break;
        case AWAITING_PERM:
            {
                int num_read = read(fd, &connections[client_index].req.mode, sizeof(mode_t));
                if (num_read != sizeof(mode_t)) {
                    return fd;
                }
                break;
            }
        case AWAITING_HASH:
            if (read_buffer_from(fd, connections[client_index].req.hash, BLOCKSIZE) < 0) {
                return fd;
            }
            break;
        case AWAITING_DATA:
            {
                // read data from client
                int ret = OK;
                char *buf = (char *) malloc(connections[client_index].req.size);
                int num_read = read(fd, buf, connections[client_index].req.size);

                // write to file
                char path[MAXPATH] = {0};
                sprintf(path, "./%s", connections[client_index].req.path);

                if (write_to_file(path, buf, num_read) < 0) {
                    ret = ERROR;
                }

                // chmod to the client mode
                if(chmod(path, connections[client_index].req.mode) == -1) {
                    perror("chmod");
                    ret = ERROR;
                }

                // send to client
                uint32_t n_ret = htonl(ret);
                int num_written = write(fd, &n_ret, sizeof(uint32_t));
                if (num_written != sizeof(uint32_t)) {
                    perror("error write");
                }

                free(buf);
                return fd;
                break;
            }
        default: 
            break;
    }

    return 0;
}

void request_init(struct request *req, char *path, struct stat *sb, int type)
{
    req->type = type;
    strcpy(req->path, path);
    req->mode = sb->st_mode;
    req->size = sb->st_size;

    FILE *fp = fopen(path, "r");
    if (fp != NULL) {
        hash(req->hash, fp);
        fclose(fp);
    }
}

// write data to file
int write_int_to(int fd, int data)
{
    uint32_t n_data = htonl(data);
    int num_written = write(fd, &n_data, sizeof(uint32_t));
    if (num_written != sizeof(uint32_t)) {
        perror("client: write");
        return -1;
    }
    return num_written;
}

// write buffer to file
int write_buf_to(int fd, char *buf, int len)
{
    int num_written = write(fd, buf, len);
    if (num_written != len) {
        perror("client: write");
        return -1;
    }
    return num_written;
}

// send requst to server
void send_request_to(int sock_fd, char *source, struct request *req)
{
    // send type
    if (write_int_to(sock_fd, req->type) < 0) {
        close(sock_fd);
        exit(1);
    }

    // send path
    char basename[MAXPATH] = {0};
	if (strcmp(source, req->path) != 0) {
		strcpy(basename, req->path + strlen(source) + 1);
	}
	else {
		char * beg = strrchr(req->path, '/');
		if (beg == NULL) {
			beg = req->path;
		}
		strcpy(basename, beg);
	}
    if (write_buf_to(sock_fd, basename, MAXPATH) < 0) {
        close(sock_fd);
        exit(1);
    }

    // send size
    if (write_int_to(sock_fd, req->size) < 0) {
        close(sock_fd);
        exit(1);
    }

    // send mode
    int num_written = write(sock_fd, &(req->mode), sizeof(mode_t));
    if (num_written != sizeof(mode_t)) {
        perror("client: write");
        close(sock_fd);
        exit(1);
    }

    // send hash
    if (write_buf_to(sock_fd, req->hash, BLOCKSIZE) < 0) {
        close(sock_fd);
        exit(1);
    }
}

// connecto to host and return the sock fd
int connect_to_server(char *host, unsigned short port)
{
    // Create the socket FD.
    int sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd < 0) {
        perror("client: socket");
        return -1;
    }

    // Set the IP and port of the server to connect to.
    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    if (inet_pton(AF_INET, host, &server.sin_addr) < 1) {
        perror("client: inet_pton\n");
        close(sock_fd);
        return -1;
    }

    // Connect to the server.
    if (connect(sock_fd, (struct sockaddr *)&server, sizeof(server)) == -1) {
        perror("client: connect");
        close(sock_fd);
        return -1;
    }

    return sock_fd;
}

// transfer a file to server
int trans_file_to_server(char *source, char *host, unsigned short port, struct request *req)
{
    // Create the socket FD.
    int sock_fd = -1;
    if ((sock_fd = connect_to_server(host, port)) < 0) {
        perror("client: socket");
        return ERROR;
    }

    // send file
    req->type = TRANSFILE;
    send_request_to(sock_fd, source, req);

    // get file info
    struct stat sb;
    if (stat(req->path, &sb) < 0) {
        return ERROR;
    }

    // REGFILE, send the file to server
    int ret = OK;
    if (!S_ISDIR(sb.st_mode)) {
        FILE *fp = fopen(req->path, "r");
        if (fp == NULL) {
			return ERROR;
        }

        // read file and write to server
        char *buf = (char *) malloc(req->size);
        if (buf == NULL) {
			return ERROR;
		}
		int read_size = fread(buf, 1, req->size, fp);
		if (write_buf_to(sock_fd, buf, read_size) < 0) {
			perror("client: write");
			ret = ERROR;
		}

        fclose(fp);
		free(buf);

        // read result from server
        int result = ERROR;
        if (read_int_from(sock_fd, &result) < 0) {
            perror("client: read result");
            ret = ERROR;
        }

        // server return ERROR
        if (result == ERROR) {
            ret = ERROR;
        }
    }

    // send finish, close the socket and exit the process
    close(sock_fd);

    return ret;
}

int client_process_request(int sock_fd, char *source, char *host, unsigned short port, struct request *req)
{
    // send request
    send_request_to(sock_fd, source, req);

    // read result from server
    int ret = ERROR;
    if (read_int_from(sock_fd, &ret) < 0) {
        perror("client: read ret");
        close(sock_fd);
        exit(1);
    }

    // if need to send this file, send it
    if (ret == SENDFILE) {
        pid_t pid = fork();
        if (pid < 0) {
            perror("client: fork");
        }
        else if (pid == 0) {
            // child, will exit after send the file
            int ret = trans_file_to_server(source, host, port, req);
            exit(ret);
        }
    }

    return 0;
}

int walk_dir(char *path, char *source, char *host, unsigned short port, int sock_fd)
{
    DIR *d;
    struct dirent *file;
    struct stat sb;
    char name[MAXPATH] = {0};

    if (!(d = opendir(path))) {
        perror("error opendir");
        return -1;
    }

    while ((file = readdir(d)) != NULL) {
        if (strcmp(file->d_name, ".") == 0 || strcmp(file->d_name, "..") == 0) {
            continue;
        }

        sprintf(name, "%s/%s", path, file->d_name);
        if (stat(name, &sb) < 0) {
            perror("error stat");
        }

        // make request, and process
        struct request req;
        request_init(&req, name, &sb, S_ISDIR(sb.st_mode) ? REGDIR : REGFILE);
        client_process_request(sock_fd, source, host, port, &req);

        if (S_ISDIR(sb.st_mode)) {
            walk_dir(name, source, host, port, sock_fd);
        }
    }

    closedir(d);
    return 0;
}

int rcopy_client(char *source, char *host, unsigned short port)
{
    // check parameters
    if (source == NULL || host == NULL) {
        return -1;
    }
    if (source[strlen(source) - 1] == '/') {
        source[strlen(source) - 1] = '\0';
    }

    int sock_fd = -1;
    if ((sock_fd = connect_to_server(host, port)) < 0) {
        perror("client: socket");
        return ERROR;
    }

    struct stat st;
    stat(source, &st);
    if (S_ISDIR(st.st_mode)) {
        walk_dir(source, source, host, port, sock_fd);
    }
    else {
        // make request, and process
        struct request req;
        request_init(&req, source, &st, S_ISDIR(st.st_mode) ? REGDIR : REGFILE);
        client_process_request(sock_fd, source, host, port, &req);
    }

    // close socket
    close(sock_fd);

    // wait all child process
    while (wait(NULL) != -1) {}

    return 0;
}

// compare two file
int compare_file(int index, struct connection *connections)
{
    struct request *req = &connections[index].req;
    struct stat sb;
    if (stat(req->path, &sb) < 0) {
        return SENDFILE;
    }

    // check if the types are incompatible
    if ((S_ISDIR(sb.st_mode) && req->type != REGDIR) || (!S_ISDIR(sb.st_mode) && req->type == REGDIR)) {
        return ERROR;
    }

    // get hash of this file
    char hash_val[BLOCKSIZE] = {0};
    FILE *fp = fopen(req->path, "r");
    if (fp != NULL) {
        hash(hash_val, fp);
        fclose(fp);
    }

    if (check_hash(hash_val, req->hash)) {
        return SENDFILE;
    }

    // change the permission of this file
    if (chmod(req->path, req->mode) == -1) {
        perror("server: chmod");
    }

    return OK;
}

// make a dir at server with path and mode
int copy_dir(char *path, mode_t mode)
{
    if (mkdir(path, 0700) == -1){
        perror("server: mkdir");
    }
    if(chmod(path, mode) == -1) {
        perror("server: chmod");
    }
    return 0;
}

// process a request
int process_request(struct connection *connections, int index)
{
    // read data
    int client_closed = read_from(index, connections);

    // the HASH is last step of info of a file
    if (connections[index].state == AWAITING_HASH) {
        if (connections[index].req.type == TRANSFILE) {
            connections[index].state = AWAITING_DATA;
        }
        else {
            connections[index].state = AWAITING_TYPE;
            int ret = compare_file(index, connections);

            // compare_file result an error
            if (ret == ERROR) {
                perror("ERROR: incompatible type");
            }
            else if (ret == SENDFILE){
                // if it is a dir, just make a dir
                if (connections[index].req.type == REGDIR) {
                    ret = ERROR;
                    if (copy_dir(connections[index].req.path, connections[index].req.mode) == 0) {
                        ret = OK;
                    }
                }
            }
            write_int_to(connections[index].sock_fd, ret);
        }
    }
    else if (connections[index].state != AWAITING_DATA) {
        // next step
        connections[index].state++;
    }

    return client_closed;
}

void rcopy_server(unsigned short port)
{
    struct connection connections[MAX_CONNECTIONS];
    for (int index = 0; index < MAX_CONNECTIONS; index++) {
        connections[index].sock_fd = -1;
        connections[index].state = AWAITING_TYPE;
    }

    // Create the socket FD.
    int sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd < 0) {
        perror("server: socket");
        exit(1);
    }

    // Set information about the port (and IP) we want to be connected to.
    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    server.sin_addr.s_addr = INADDR_ANY;

    // This should always be zero. On some systems, it won't error if you
    // forget, but on others, you'll get mysterious errors. So zero it.
    memset(&server.sin_zero, 0, 8);

    // Bind the selected port to the socket.
    if (bind(sock_fd, (struct sockaddr *)&server, sizeof(server)) < 0) {
        perror("server: bind");
        close(sock_fd);
        exit(1);
    }

    // Announce willingness to accept connections on this socket.
    if (listen(sock_fd, MAX_BACKLOG) < 0) {
        perror("server: listen");
        close(sock_fd);
        exit(1);
    }

    // The client accept - message accept loop. First, we prepare to listen to multiple
    // file descriptors by initializing a set of file descriptors.
    int max_fd = sock_fd;
    fd_set all_fds, listen_fds;
    FD_ZERO(&all_fds);
    FD_SET(sock_fd, &all_fds);

    while (1) {
        // select updates the fd_set it receives, so we always use a copy and retain the original.
        listen_fds = all_fds;
        int nready = select(max_fd + 1, &listen_fds, NULL, NULL, NULL);
        if (nready == -1) {
            perror("server: select");
            exit(1);
        }

        // Is it the original socket? Create a new connection ...
        if (FD_ISSET(sock_fd, &listen_fds)) {
            int client_fd = accept_connection(sock_fd, connections);
            if (client_fd > max_fd) {
                max_fd = client_fd;
            }
            FD_SET(client_fd, &all_fds);
        }

        // Next, check the clients.
        // NOTE: We could do some tricks with nready to terminate this loop early.
        for (int index = 0; index < MAX_CONNECTIONS; index++) {
            if (connections[index].sock_fd > -1 && FD_ISSET(connections[index].sock_fd, &listen_fds)) {
                int client_closed = process_request(connections, index);
                if (client_closed > 0) {
                    FD_CLR(client_closed, &all_fds);
                }
            }
        }
    }
}

