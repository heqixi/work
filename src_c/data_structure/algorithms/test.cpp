#include<iostream>
#include<vector>
#include<set>
#include<map>
#include<fstream>
using namespace std;
int main(){
typedef set<int>  Itemset;
typedef Itemset::iterator ItemsetIter;
Itemset s1;
int i ;
for( i = 0;i<100;i++){
    s1.insert(i);
}

for(ItemsetIter iter = s1.begin();iter != s1.end();iter++){
    printf("%i\t",*iter);
}
printf("!!!!!!!!!!!");
Itemset s2(s1.begin(),--s1.end());
int n1 = *(--s1.end());
printf("%i\n",n1);
for (ItemsetIter iter = s2.begin();iter != s2.end();iter++){
    printf("%i\n",*iter);
}
    return 0;
}
