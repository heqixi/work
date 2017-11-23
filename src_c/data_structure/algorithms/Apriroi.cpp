#include<iostream>
#include<vector>
#include<algorithm>
#include<string>
#include<sstream>
#include<fstream>
#include<set>
#include<map>

# define m_p make_pair
# define p_b push_back
# define min(a,b) ((a) < (b)? (a):(b))
# define max(a,b) ((a) > (b)? (a):(b))

using namespace std;

# define HASESIZE 90

struct HashTree{

    int value ;
    struct HashTree* child[HASESIZE];
    int end ;
    HashTree(){
            end = 0 ;
            for (int i = 0;i < HASESIZE;i++)
            child[i] = NULL;

    }
};

typedef set<int> Itemset;
typedef set<Itemset> SuperItemset;
typedef Itemset::iterator ItemsetIter;
typedef SuperItemset::iterator SuperItemsetIter;

vector<int>  transactions[10000]; // stores all the transactions 
map <Itemset,int> support;       // counts the support of itemsets 
map <string,int > ItemToNo;      // Assigns each item to an ID ;
map <int,string> NoToItem;

map <pair<Itemset,Itemset>,int > rep ; // checks for duplicate rules 
int transactionsSize;   // Size of transactions 
const double minSup = 0.05;
const double minConf = 0.1;

void readData();   // for reading the data from input file and store it in a vector of transactions
vector<int> split(string s,char delim); // for splitig the comma seperated itemsets of the transaction 
SuperItemset makeL1();
SuperItemset generateCk(const SuperItemset &L);
void createHashTree(struct HashTree **head,const SuperItemset &res, int k);
void subsetHash(SuperItemset &ret,struct HashTree *head,vector<int> arr,int data[],int start,
        int end ,int index ,int k); // for support counting using the generated Hash Tree
SuperItemset genSubset(const Itemset &itemset);
void showRule(ofstream &outfile,const SuperItemset &L); //for showing all the rules of a particular itemcount
void partition(ofstream &outfile,const ItemSet &Itemset,ItemSet &P1,Itemset &P2,ItemsetIter iter);


vector<int> split(string s ,char delim){

    stringstream ss(s);
    string item;
    static int temp = 1;
    vector<int> elems;
    while(getline(ss,item,delim)){
        if(!ItemToNo[item]]){
            ItemToNo[item] = temp;
            NoToItem[temp] = item;
            elems.p_b(ItemToNo[item]);
            ++temp;

        }
        else{
            elems.p_b(ItemToNo[item]);

        }
    }
    sort(elems.begin(),elems.end());
    return elems;

}

void readData(){
    freopen("groceries.csv","r",stdin);
    int i =  0 ;
    while(getline(cin,s)){
        transactions[i++] = split(s,'s');
        transactionsSize++;

    }
}

//generate  L1 from database 

SuperItemset makeL1(){
    int i ,j ,k;
    SuperItemset L;
    for (i = 0;i<transactionsSize;i++)
    {
        for (j= 0;j<transactions[i].size();j++){
            ItemSet temp;
            k = transactions[i][j];
            temp.inset(k);
            support[temp] += 1 ;
            if(double ( support[temp] )/ transactionsSize >= minSup){
                L.insert(temp);
            }
        }
    }
    return L;

}
 // generate Ck from Lk-1 ;
 SuperItemset generateCk(const SuperItemset *L){
    
     SuperItemset ret ;
     for (SuperItemsetIter iter = L.begin();iter != L.end();++iter){
         SuperItemset t = iter;
            for (SuperItemset iter2 = ++t; iter2 != L.end();++iter2) {
                ItemSet s1 = ((*iter).begin(),--(*iter).end()) ;
                Itemset s2 = ((*iter2).begin(),--(*iter2).end());
                int n1 = *(--(*iter).end()), n2 = *(--(*iter2).end());
                if (s1 == s2 && n1 != n2)
                {
                    Itemset temp =*iter;
                    temp.insert(n2);
                    ret.insert(temp);
            }

     }
    return ret ;
 }

void createHashTree(struct HashTree**head,const SuperItemset &res,int k){
    struct HashTree *temp;
    for (SuperItemsetIter iter = res.begin();iter != res.end(); ++iter){
        Itemset item = *iter;
        temp = *head;
        int j = 0 ;
        for (ItemsetIter iter2 =*(iter).begin();iter2 != *(iter).end();++iter2,++j){
            int val = *iter2;
            if (temp->child[val%HASESIZE] == NULL){
                temp->child[val%HASESIZE] = new HashTree();
                temp->child[val%HASESIZE]->value = val;
                temp = temp->child[val%HASESIZE];
            }
            else {
                temp = temp->child[val%HASESIZE];
            }
        }    
        }
}

void subsetHash(SuperItemset &ret,struct HashTree *head,vector<int> arr,
        int data[],int start ,int end ,int index,int k){
    int j,i,val;
    if (index == k){
        ItemSet item;
        struct HashTree item;
        for (j=0;j<k;j++){
            if (temp->child[data[j]%HASESIZE] == NULL)
                break;
            eles{
                temp = temp->child[data[j]%HASESIZE];
                item.insert(data[j]);
            }
    }
    if(j==k){
        support[item] += 1;
        int val = support[item];
        if (double(val)/transactionsSize >= minSup && ret.find(item) == ret.end()){
            ret.insert(item);

        }
    }
    return ;
    for (i = start;i<end && end-i+1 > k-index;i++){
        data[index] = arr[i];
        subsetHash(ret,head,arr,data,i+1,end,index+1,k);

    }
}

/* Fuction to print the subset */ 
void genSubset(SuperItemset &ret,struct HashTree *head;vector<int> arr,int n ,int k ){
    int data[k];
    subsetHash(ret,head,arr,data,0,n-1,0,k);

}

SuperItemset supportCount(struct HashTree *head,int k){
    SuperItemset ret;
    ItemSet item;
    int i,j;
    for (i = 0;i<transactionsSize;i++){
        if (transactions[i].size() < k) {
            continue;
        }
        else {
            genSubset(ret,head,transactions[i],transactions[i].size(),k);
        }
    }
    return ret;
}

// show all rules 

void showRule(ofstream &outfile,const SuperItemset &L){
    for (SuperItemsetIter iter = L.begin();iter != L.end();++iter){
        int s = (*iter).size();
        // enumerate all partition 
        ItemSet P1 ,P2 ;
        partition(outfile,*iter,P1,P2,(*iter).begin());

    }
    
}

// enumerate to fine the rules 
void partition(ofstream &outfile,const ItemSet &itemset,ItemSet &P1,Itemset &P2,
        ItemSetIter iter){
    if (iter == itemset.end()){
        if (!P1.empty() && !P2.empty() && !rep[m_p(P1,P2)] && !rep[m_p(P2,P1)]){
            double p ;
            p = double (suport[itemset]) / support[P1];
            if (p>= minConf){
                string s = "{";
                for (ItemSetIter it = P1.begin();it != P1.end();++it){
                    s += NoToItem[*it];
                    s += ",";
                
            }
                s.erase(s.begin()+ s.size()-1);
                s += "}";
                s += "-->";
                s += "{";
                for (ItemSetIter it = P2.begin();it != P2.end();++it){
                    s += NoToItem[*it];

                }
                s += "}";
                outfile << s << endl;
           }
            p = double(support[itemset]) / support[P2];
            if (p >= minConf){
                string s = "{";
                for (ItemSetIter it = P2.begin();it != P2.end();++it){
                    s += NoToItem[*it];
                    s += ",";

                }
                s.erase(s.begin()+ s.size() -1);
                s += "}";
                s += "-->";
                s += "{";
                for (ItemSetIter it = P1.begin();it != P2.end();++it){
                    s += NoToItem[*it];

                }
                s += "}";
                outfile << s << endl;
             }

            rep[m_p(P1,P2)]= 1;
            rep[m_p(P2,P1)] = 1;
            
        }
        return ;
    }
    P1.insert(*iter);
    partition(outfile,Itemset,P1,P2,++iter);
    P1.erase(*(--iter));
    P2.insert(*iter);
    partition(outfile,itemset,P1,P2,++iter);
    P2.erase(*(iter));
}
int main(){
    readData();
    const char *outfile_filename = "out.txt";
    ofstream outfile(outfile_filename);

    SuperItemset L = makeL1();
    int k = 2 ;
    while(L.size()){
        SuperItemset res = generateCk(L);

        HashTree *root ,*temp ;
        root = new HashTree();

        createHashTree (&root,&res,k);

        L = supportCount(root,k);
        free(root);
        showRule(outfile,L);
        k++;
    }
    return 0;
}

