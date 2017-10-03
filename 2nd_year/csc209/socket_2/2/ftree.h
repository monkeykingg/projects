#ifndef _FTREE_H_
#define _FTREE_H_

#include "hash.h"

#define MAXPATH 128
#define MAXDATA 256

// Input states
#define AWAITING_TYPE 0
#define AWAITING_PATH 1
#define AWAITING_SIZE 2
#define AWAITING_PERM 3
#define AWAITING_HASH 4
#define AWAITING_DATA 5

// Request types
#define REGFILE 1
#define REGDIR 2
#define TRANSFILE 3

#define OK 0
#define SENDFILE 1
#define ERROR 2

#ifndef PORT
    #define PORT 30100
#endif

#define MAX_BACKLOG 5
#define BUF_SIZE 128
#define MAX_CONNECTIONS 512

struct request {
    int type;           // Request type is REGFILE, REGDIR, TRANSFILE
    char path[MAXPATH];
    mode_t mode;
    char hash[BLOCKSIZE];
    int size;
};

struct connection {
    int sock_fd;
    int state;
    struct request req;
};

int rcopy_client(char *source, char *host, unsigned short port);
void rcopy_server(unsigned short port);

#endif // _FTREE_H_
