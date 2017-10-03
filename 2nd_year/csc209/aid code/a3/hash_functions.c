#include <stdio.h>
#include <stdlib.h>
#include "hash.h"

char* hash(FILE *f) {

    char *hash_val = malloc(BLOCK_SIZE);
    // init all block_size bytes of the hash_val to 0
    int i;
    for (i = 0; i < BLOCK_SIZE; i++){
        hash_val[i] = '\0';
    }

    char val;
    int count = 0;

    // read input one char a time and xor it with values in hash_val
    while (fread(&val, 1, 1, f) == 1){
        hash_val[count] = hash_val[count] ^ val;
        count++;
        if (count >= BLOCK_SIZE){
            count = 0;
        }
    }
    return hash_val;
}
