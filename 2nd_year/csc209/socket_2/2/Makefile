PORT=30001
CFLAGS = -DPORT=$(PORT) -g -Wall -std=gnu99

all: rcopy_server rcopy_client

rcopy_server: rcopy_server.o ftree.o hash_functions.o
	gcc ${CFLAGS} -o $@ rcopy_server.o ftree.o hash_functions.o

rcopy_client: rcopy_client.o ftree.o hash_functions.o
	gcc ${CFLAGS} -o $@ rcopy_client.o ftree.o hash_functions.o

%.o: %.c
	gcc ${CFLAGS} -c $<

clean:
	rm *.o rcopy_server rcopy_client
