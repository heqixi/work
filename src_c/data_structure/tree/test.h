# include<stdio.h>
#include<stdlib.h>
// The Binary Tree declaration 
#define OVERFLOW 0 
#define OK 1 
typedef int Status;
typedef char ElemType;
typedef struct BiTree
{
    ElemType data ;
    struct BiTree *Lchild;
    struct BiTree *Rchild;
} BiTree,*Binary_Tree;
//Create a Binary Tree 
Binary_Tree CreateBiTree(Binary_Tree);
// show the status of Binary Tree
Status PreShowBitree(Binary_Tree);
//IterInorder 
void iterInorder(Binary_Tree);
//copy a binary tree 
Binary_Tree copy(Binary_Tree);
// determined whether two tree is equal
int isEqual(Binary_Tree,Binary_Tree);



// The stack data struct and methods
#define ERROR 99
#define ElementType Binary_Tree
#define MAX_STACK_SIZE 1024
typedef struct {
    ElementType data[MAX_STACK_SIZE] ;
    int top;
}Stack,*StackPointer;
void Push(Stack* ,ElementType );
Stack *InitStack();
ElementType Pop(Stack* );
//void PrintStack(Stack*);



