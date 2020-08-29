#include <string.h>
#include <stdlib.h>
#include <stdio.h>
char * longestPalindrome(char * s);

int main(int argc, char *argv[]) {
  char* s = argv[1];
  char* s_ = longestPalindrome(s);
  printf("%s\n", s_);
  free(s_);
}

char * longestPalindrome(char * s){
  int slen = strlen(s);
  #define VALID(i) (i >= 0 && i < slen)
  #define UNINIT 0
  #define TRUE 1
  #define FALSE 2
  char table[slen][slen];
  for (int i=0; i<slen;i++) {
    for (int j=0; j<slen; j++) {
      table[i][j] = UNINIT;
    }
  }
  int i_ = -1;
  int j_ = -1;

  for (int i = 0; i < slen; i++) {
    table[i][i] = TRUE;
    i_ = i;
    j_ = i;
  }
  for (int l = 1; l <= slen; l++) {
    for (int i = 0; i < slen-l; i++) {
      int j = i + l;
      int has_smaller = FALSE;
      if (l == 1 || (VALID(i+1) && VALID(j-1) && table[i+1][j-1] == TRUE))
      {
        has_smaller = TRUE;
      }
      table[i][j] = (has_smaller == TRUE && s[i] == s[j])? TRUE: FALSE;
      if (table[i][j] == TRUE) {
        i_ = i;
        j_ = j;
      }
      // printf("(%d,%d, %d), i_ %d j_ %d\n", i, j, table[IND(i,j)], i_, j_);
    }
  }
  if (i_ >= 0) {
    char* new_s = malloc(sizeof(char) * (j_-i_+2));
    stpncpy(new_s, s+i_, j_-i_+1);
    return new_s;
  }
  else {
    char* new_s = malloc(sizeof(char));
    new_s[0] = '\0';
    return new_s;
  }
}
