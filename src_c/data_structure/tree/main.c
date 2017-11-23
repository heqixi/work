#include"test.h"
#include<stdio.h>
int main(){
    // create a binary_tree
    BiTree *T;
    printf("Please create a Binary Tree : \n");
    T = CreateBiTree(T);
    printf("PreShowBitree !!!: \n");
    PreShowBitree(T);
    printf("IterInorder the tree !!\n");
    iterInorder(T);
    BiTree *T1 ;
    T1 = copy(T);
    printf("PreShowBitree T1 :\n");
    PreShowBitree(T1);
    // create a stack ;
    Stack* stack ;
    stack = InitStack(stack);
    Push(stack,T);
    int is_Equal = isEqual(T,T1);
    printf("%i",is_Equal);


    
    return 0 ;
}
