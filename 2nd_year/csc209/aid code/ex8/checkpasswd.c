/* this solution needs error checking! */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

/* Read a user id and password from standard input,
   - create a new process to run the validate program
   - send 'validate' the user id and password on a pipe,
   - print a message
        "Password verified" if the user id and password matched,
        "Invalid password", or
        "No such user"
     depending on the return value of 'validate'.
*/

/* Use the exact messages defined below in your program." */

#define VERIFIED "Password verified\n"
#define BAD_USER "No such user\n"
#define BAD_PASSWORD "Invalid password\n"
#define OTHER "Error validating password\n"


int main(void) {
    char userid[10];
    char password[10];

    /* Read a user id and password from stdin */
    printf("User id:\n");
    scanf("%s", userid);
    printf("Password:\n");
    scanf("%s", password);

    int fd[2];

    // create a pipe and check error
    if (pipe(fd) == -1) {
        perror("pipe");
        exit(1);
    }

    // create a new process to run the validate program
    int process = fork();

    // check error
    if (process < 0){
        perror("fork");
        exit(1);

    // if process is a child process
    } else if (process == 0){

        // check error, close fd[1] for child process
        if (close(fd[1]) == -1){
            perror("close");
            exit(1);
        }

        // check error, copy fd[0] to STDIN_FILENO
        if (dup2(fd[0], STDIN_FILENO) == -1){
            perror("dup2");
            exit(1);
        }

        execlp("./validate", "./validate", NULL);
        fprintf(stderr, "ERROR: exec");

        // check error, close pipe
        if (close(fd[0]) == -1){
            perror("close");
            exit(1);
        }

    // if process is a parent process
    } else {

        // check error, close fd[0] for parent process
        if (close(fd[0]) == -1){
            perror("close");
            exit(1);
        }

        // check error, write info
        if (write(fd[1], userid, 10) != 10){
            perror("write");
            exit(1);
        }

        if (write(fd[1], password, 10) != 10){
            perror("write");
            exit(1);
        }

        // check error, close pipe
        if (close(fd[1]) == -1){
            perror("close");
            exit(1);
        }

        int status;

        // check error, wait process
        if (wait(&status) == -1){
            perror("wait");
            exit(1);
        }

        // check if child exit not normally
        if (WIFSIGNALED(status)){
            printf(OTHER);
            exit(1);
        }

        // get status
        int check = WEXITSTATUS(status);

        // if child exit normally
        if (WIFEXITED(status)){

            // check if there is an error
            if (check == 1){
                printf(OTHER);
                exit(1);

            // if there is no user
            } else if (check == 3){
                printf(BAD_USER);

            // if invalid password occur
            } else if (check == 2){
                printf(BAD_PASSWORD);

            // if both user and password are matched
            } else if (check == 0){
                printf(VERIFIED);
            }

        }
    }
    return 0;
}
