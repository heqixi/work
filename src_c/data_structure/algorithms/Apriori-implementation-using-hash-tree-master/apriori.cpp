#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <sstream>
#include <fstream>
#include <set>
#include <map>

#define m_p make_pair
#define p_b push_back

#define min(a,b) (((a)<(b))?(a):(b))
#define max(a,b) (((a)>(b))?(a):(b))

using namespace std;

#define HASHSIZE 90

struct HashTree{		// structure for hash tree
	int value;
	struct HashTree* child[HASHSIZE];
	int end;

	HashTree(){
		end=0;
		for(int i=0;i<HASHSIZE;i++)
			child[i]=NULL;
	}

};

typedef set<int> ItemSet;		//set of itemsets
typedef set<ItemSet> SuperItemSet;		//set of sets of itemsets
typedef ItemSet::iterator ItemSetIter;	//Itemset iterator
typedef SuperItemSet::iterator SuperItemSetIter;	

vector<int> transactions[10000];	//stores all the transactions 

map< ItemSet,int> support;		//counts the support of  itemsets

map<string,int> ItemToNo;		//Assigns each item to an ID
map<int,string> NoToItem;	   //Converts back each ID to a no.

map<pair<ItemSet,ItemSet>,int> rep;		//checks for duplicate rules

int transactionSize;				//Size of transactions
const double minSup = 0.05;			//Minimum support value
const double minConf = 0.1;			//Minimum confidence value


void readData();		//for reading the data from input file and storing it in a vector of transactions
vector<int> split(string s,char delim);		//for splitting the comma separated itemsets of the transaction
SuperItemSet makeL1();		// for making L1						
SuperItemSet generateCk( const SuperItemSet &L );	//generate itemsets with number of items one more than previous
void createHashTree(struct HashTree **head,const SuperItemSet &res,int k); 	//for creating the hash tree
void subsetHash(SuperItemSet &ret,struct HashTree *head,vector<int> arr,int data[],int start,int end,int index,int k); //for support counting using the generated hash tree
SuperItemSet genSubset( const ItemSet &itemset );	//for generating all the subsets of a set 
void showRule( ofstream &outfile, const SuperItemSet &L);	//for showing all the rules of a particular itemcount
void partition( ofstream &outfile,const ItemSet &itemset,ItemSet &P1,ItemSet &P2,ItemSetIter iter);	


vector<int> split(string s,char delim){
    stringstream ss(s);
    string item;
    static int temp=1;
    vector<int> elems;
    while (getline(ss,item,delim)) {
        if(!ItemToNo[item]){
        	ItemToNo[item]=temp;
        	NoToItem[temp]=item;
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
	int i=0,j;
	string s;
	while(getline(cin,s)){
		transactions[i++]=split(s,',');
		transactionSize++;
	}
}

// generate L1 from database
SuperItemSet makeL1(){
	int i,j,k;
	SuperItemSet L;
	for (i=0;i<transactionSize;i++) {
		for (j=0;j<transactions[i].size();j++){
			ItemSet temp;
			k=transactions[i][j];
			temp.insert(k);
			support[temp]+=1;
			if ( double(support[temp]) /transactionSize >= minSup){
				L.insert(temp);
			}

		}
	}
	return L;
}

// generate Ck from Lk-1
SuperItemSet generateCk( const SuperItemSet &L ) {
	SuperItemSet ret;
	for ( SuperItemSetIter iter = L.begin(); iter != L.end(); ++iter ) {
		SuperItemSetIter t = iter;
		for ( SuperItemSetIter iter2 = ++t; iter2 != L.end(); ++iter2 ) {
			ItemSet s1( (*iter).begin(), --(*iter).end() ), s2( (*iter2).begin(), --(*iter2).end() );
			int n1 = *( --(*iter).end() ), n2 = *( --(*iter2).end() );
			if ( s1 == s2 && n1 != n2 ) {
				ItemSet temp = *iter;
				temp.insert( n2 );
				ret.insert( temp );
			}
		}
	}
	return ret;
}

void createHashTree(struct HashTree **head,const SuperItemSet &res,int k){
	struct HashTree *temp;

	for ( SuperItemSetIter iter=res.begin();iter!=res.end();++iter){
		ItemSet item=*iter;
		temp=*head;
		int j=0;
		for(ItemSetIter iter2=item.begin();iter2!=item.end();++iter2,++j){
			int val=*iter2;
			if(temp->child[val%HASHSIZE]==NULL){
				temp->child[val%HASHSIZE]=new HashTree();
				temp->child[val%HASHSIZE]->value=val;
				temp=temp->child[val%HASHSIZE];
			}
			else{
				temp=temp->child[val%HASHSIZE];
			}
		}
	}
}

void subsetHash(SuperItemSet &ret,struct HashTree *head,vector<int> arr,int data[],int start,int end,int index,int k){
    int j,i,val;
    if (index==k){
    	ItemSet item;
    	struct HashTree *temp=head;
        for (j=0;j<k;j++){
        	if(temp->child[data[j]%HASHSIZE]==NULL)
        		break;
        	else{
        		temp=temp->child[data[j]%HASHSIZE];
        		item.insert(data[j]);
        	}
        }
        
        if(j==k){
        	support[item]+=1;
        	int val=support[item];
	        if(double(val)/transactionSize>=minSup&&ret.find(item)==ret.end()){
	        	ret.insert(item);
	        }        	
        }

        return;
    }
    for (i=start;i<=end&&end-i+1>=k-index;i++){
        data[index]=arr[i];
        subsetHash(ret,head,arr,data,i+1,end,index+1,k);
    }
}
 
/*  Function to print the subset  */ 
void genSubset(SuperItemSet &ret,struct HashTree *head,vector<int> arr,int n,int k){
    int data[k];
    subsetHash(ret,head,arr,data,0,n-1,0,k);
}

SuperItemSet supportCount(struct HashTree *head,int k){
	SuperItemSet ret;
	ItemSet item;
	int i,j;

	for(i=0;i<transactionSize;i++){
		if(transactions[i].size()<k){
			continue;
		}
		else{
			genSubset(ret,head,transactions[i],transactions[i].size(),k);
		}
	}

	return ret;
}

// show all rules
void showRule( ofstream &outfile, const SuperItemSet &L) {
	for ( SuperItemSetIter iter = L.begin(); iter != L.end(); ++iter ) {
		int s = (*iter).size();
		// enumerate all partition
		ItemSet P1, P2;
		partition( outfile, *iter, P1, P2, (*iter).begin());
	}
}

// enumerate to find the rule
void partition(ofstream &outfile,const ItemSet &itemset,ItemSet &P1,ItemSet &P2,ItemSetIter iter){
	if ( iter == itemset.end() ) {
		if ( !P1.empty() && !P2.empty() && !rep[m_p(P1,P2)] && !rep[m_p(P2,P1)]) {
			double p;

			p=double(support[itemset])/support[P1];

			if(p>=minConf) {
				string s="{";
				for (ItemSetIter it=P1.begin();it!=P1.end();++it ){
					s+=NoToItem[*it];
					s+=",";
				}
				s.erase(s.begin()+s.size()-1);
				s+="}";
				s+=" --> ";
				s+="{";
				for (ItemSetIter it=P2.begin();it!=P2.end();++it){
					s+=NoToItem[*it];				
				}
				s+="}";
				outfile<<s<<endl;
//				outfile<<'('<<p<<')'<<endl;
			}
		
			p=double(support[itemset])/support[P2];

			if (p>=minConf) {
				string s="{";
				for (ItemSetIter it=P2.begin();it!=P2.end();++it ){
					s+=NoToItem[*it];
					s+=",";
				}
				s.erase(s.begin()+s.size()-1);
				s+="}";
				s+=" --> ";
				s+="{";
				for (ItemSetIter it=P1.begin();it!=P1.end();++it){
					s+=NoToItem[*it];					
				}
				s+="}";
				outfile<<s<<endl;
//				outfile<<'('<<p<<')'<<endl;
			}
			rep[m_p(P1,P2)]=1;
			rep[m_p(P2,P1)]=1;
		}
		return;
	}
	P1.insert(*iter);
	partition(outfile,itemset,P1,P2,++iter);
	P1.erase(*(--iter));
	P2.insert(*iter);
	partition(outfile,itemset,P1,P2,++iter);
	P2.erase(*(--iter));
}

int main(){

	readData();
	const char *output_filename = "output.txt";	
	ofstream outfile(output_filename);
	
	SuperItemSet L = makeL1();
	
	int k=2;

	while ( L.size() ) {
//		cout<<L.size()<<endl;
		SuperItemSet res=generateCk(L);

		HashTree *root,*temp;
		root=new HashTree();

		createHashTree(&root,res,k);

		L=supportCount(root,k);	

		free(root);
		showRule(outfile,L);
		k++;
	}

	return 0;
}