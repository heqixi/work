#include<stdio.h>
#include<stdlib.h>
#include"test.h"


// the data structure of stack contain a 1-d array 
// and a variable which record the top element of stack 


// initialize the stack
Stack *InitStack(){
    Stack* stack;
    stack = (Stack*)malloc(sizeof(Stack));
    if (!stack)
    
    {
        printf("InitStack Fail !!,can't not allocate a memory space !");
        return NULL;
    }
    stack->top = -1 ;
    return stack;
}
int isFull(Stack* stack)
{

    if (stack->top == MAX_STACK_SIZE -1)
    {
        printf("The Stack is full!!!! \n");
        return 1 ;

    }
    return 0 ;
}

int IsEmpty(Stack* stack)
{

    if (stack->top == -1){
        printf("The Stack is empty !!!! \n");
        return 1 ;
    }
    return 0 ;
}

// push to the stack 
void Push(Stack* stack,ElementType item)
{ if (isFull(stack))
    { return ;
    }
    stack->data[++stack->top] = item;
    printf("The node's data is: \n");
    printf("%c",item->data);
}

ElementType Pop (Stack* stack){ 
if (IsEmpty(stack)){
return NULL;
}
return stack->data[stack->top--]; }
/*
void PrintStack(Stack* stack){

    printf("The current element in the stack: \n");
    int i ;
    for (i = stack->top;i >= 0;i--){
        printf("%d\n",stack->data[i]);

    }

}
*/
/*
int main(int argc,const char* argv[]){

    Stack* stack;
    stack = InitStack();
    Push(stack,1);
    Push(stack,2);
    Push(stack,3);
    PrintStack(stack);
    Pop(stack);
    Pop(stack);
    PrintStack(stack);
    return 0 ;
}
 
*/
