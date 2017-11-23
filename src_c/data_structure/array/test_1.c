# include<stdio.h>

void print1(int [],int rows);
void main(){
    int list[3] = {1,2,4};
    printf("%5d",list[1]);
    int rows = 3;
    print1(list,rows);
}
void print1 (int *ptr,int rows ){
    int i ;
    printf("Address Contents \n");
    for (i = 0;i < rows; i++)
        printf("%p%5d\n",ptr+i,*(ptr+i));
    printf("\n");
}
