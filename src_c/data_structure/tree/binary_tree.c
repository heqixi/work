# include<stdio.h>
# include<stdlib.h>
# include "test.h"
Binary_Tree CreateBiTree(Binary_Tree T)
{
    char ch ;
    T = (Binary_Tree) malloc(sizeof(BiTree));
    if (!T)
        exit(OVERFLOW);
    scanf("%c",&ch);
    printf("%c",ch);
    printf("\n");
    if (ch == '0')
        T = NULL ;
    else 
    {
        T-> data = ch ;
        printf("Create a left node !!! \n");
        T-> Lchild = CreateBiTree(T->Lchild);
        printf("Create a right node !!!\n");
        T->Rchild  = CreateBiTree(T->Rchild);
    }
    return T ;

}

Status PreShowBitree (Binary_Tree T)
{
    if (T != NULL)
    {
        printf("%c",T->data);
        PreShowBitree(T->Lchild);
        PreShowBitree(T->Rchild);

    }
    return OK;
}

void iterInorder( Binary_Tree node)
{

    Stack* stack;
    stack = InitStack(stack);
    for (;;){
    
        for (;node;node = node->Lchild)
            Push (stack,node);
        node  = Pop(stack);
        if (!node) break;
        printf("%d\n",node->data);
        node = node->Rchild;
    }
}

Binary_Tree copy(Binary_Tree original){

    Binary_Tree  temp;
    if (original) {
        temp = (Binary_Tree) malloc(sizeof(*temp));
        temp->Lchild = copy(original->Lchild);
        temp->Rchild = copy(original->Rchild);
        temp->data = original->data;
        return temp;
        
    }
    return NULL;
}

int isEqual(Binary_Tree first,Binary_Tree second){
    return (!first && !second) || (first && second && first->data == second->data 
            && isEqual(first->Lchild,second->Lchild) && isEqual(first->Rchild,second->Rchild));
}


/*
int main()
{
    BiTree *T ;
    printf(" Please create a Binary Tree : \n");
    T = CreateBiTree(T);
    printf("PreShow BiTree !!!");
    PreShowBitree(T);
    iterInorder(T);
    Stack* stack ;
    stack = InitStack();
    Push(stack,1);
    PrintStack(stack);
}
*/
