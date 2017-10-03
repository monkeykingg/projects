#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <sys/time.h>
#include <time.h>

// Init counter, seconds, microseconds.
static int c = 0;
double ms = 0;
int seconds;

// A handler for info printing.
void handler(int code) {
    fprintf(stderr, "Caught signal: %d\n", code);
    printf("Reads: %d, Seconds: %d\n", c, seconds);
    exit(1);
}

int main(int argc, char ** argv) {

    // Open file
    FILE * f = fopen(argv[1], "rb");

    // check if file cannot open
    if (f == NULL) {
        perror("fopen");
        exit(1);
    }

    // argc cannot be 3
    if (argc != 3) {
        printf("Wrong input");
        exit(1);
    }

    // Init variables
	seconds = strtol(argv[2], NULL, 10);
    int x;
    int count;

    // set timer
    struct itimerval value;
    value.it_value.tv_sec = seconds;
    value.it_value.tv_usec = 0;
    value.it_interval.tv_usec = 0;
    value.it_interval.tv_sec = 0;

    // check error
    if (setitimer(ITIMER_REAL, &value, NULL)) {
        perror("setitimer");
        exit(1);
    }

    // set sigaction
    struct sigaction newact;
    newact.sa_handler = handler;
    newact.sa_flags = 0;
    sigemptyset(&newact.sa_mask);
    sigaction(SIGALRM, &newact, NULL);

    signal(SIGALRM, handler);

    for (;;) {
        x = random() % 100;
        fseek(f, sizeof(int)*x, SEEK_SET);
        fread(&count, sizeof(int), 1, f);
        printf("Number: %d\n", count);
        c++;
    }

    fclose(f);

    return 0;
}
