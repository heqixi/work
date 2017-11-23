#include<iostream>
#include<vector>
using namespace std;

vector<int> doubleValues (const vector<int>& v)

{ 
    vector <int> new_values (v.size());
    for (auto itr = new_values.begin(),end_itr = new_values.end();
            itr != end_itr; ++ itr)
    
    {  new_values.push_back(2 **itr);

     }
    return new_values ;

}

int main (){
    vector <int> v;
    for (int i = 0;i < 2 ;i++){
    
        v.push_back(i);

    }
    cout << v.size()<< endl;
    v = doubleValues(v);
    for(auto x :v )
        cout <<x << endl; 

}
