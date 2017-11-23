 # include<iostream>
 #include<string>
 using namespace std;
 string::size_type find_char(const string &,char,string::size_type &);
 int main(){
  string::size_type ctr ;
  ctr = find_char("heqixixii",'i',ctr);
 cout<< ctr<<endl;
   }   

 
 string::size_type find_char(const string &s, char c ,string::size_type &occurs){
    auto ret = s.size();
    occurs = 0;
   for (decltype(ret) i = 0 ; i != s.size();++i)
      {   cout<<i<<endl;
     
          if (s[i] == c)  ret = i;
	  ++occurs;
         } 
	return ret;            
}
