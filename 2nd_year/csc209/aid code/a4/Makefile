PORT=30000
FLAGS = -DPORT=$(PORT) -g -Wall -std=gnu99
DEPENDENCIES = ftree.h hash.h

all: rcopy_server rcopy_client

rcopy_server: rcopy_server.o ftree.o hash_functions.o
	gcc ${FLAGS} -o $@ $^

rcopy_client: rcopy_client.o ftree.o hash_functions.o
	gcc ${FLAGS} -o $@ $^

%.o: %.c ${DEPENDENCIES}
	gcc ${FLAGS} -c $<

clean:
	rm *.o rcopy_server rcopy_client
