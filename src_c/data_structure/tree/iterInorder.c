#include"test.h"

void iterInorder(Binary_Tree node){
    int top = -1;
    Stack* stack;
    stack = InitStack(stack);
    for (;;){
        for (;node;node = node->Lchild)
            Push(stack,node);
        node = Pop(stack);
    if (!node) break;
    printf("%d",node->data);
    node = node->Rchild;
    }
}
