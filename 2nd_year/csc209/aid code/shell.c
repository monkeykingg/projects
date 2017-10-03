#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#define MAX_LINE 256
char line[MAX_LINE];

char* dupstr(char* s) {char* r = malloc(strlen(s)+1);strcpy(r,s);return r;}

void run(const char* s) {
	int cnt = 0;
	char* t = dupstr(s);
	t[strlen(t)-1] = 0;
	for(const char* p=s;*p;p++) cnt += (*p == ' ' ? 1 : 0);
	char** argv = malloc(sizeof(char*)*(cnt+1+1));
	char* path = t;
	for(char** p=argv+1;*t;t++) if(*t == ' ') {
		*p++ = t+1; *t = 0;
	}
	argv[0] = dupstr(path);
	argv[cnt+1] = NULL;

	int fd = open("mu", O_WRONLY | O_APPEND | O_CREAT);
	dup2(fd, 1);
	close(fd);

	execv(path, argv);
	printf("[%s]", path);
	perror("exec");
}

int main() {
	printf("$");
	while (fgets(line, MAX_LINE, stdin)!=NULL) {
		int f = fork();
		if ( f < 0 ) exit(-1);
		if ( f != 0 ) {
			int ret;
			wait(&ret);
		} else {
			run(line);
			return -1;
		}
		printf("$");
	}
}
