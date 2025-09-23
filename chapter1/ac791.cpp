#include<iostream>
#include<vector>
using namespace std;

//A位数大于B的位数
vector<int> add(vector<int>&A,vector<int>&B){
    if(A.size()<B.size()) return add(B,A);
    //声明需要用到的变量
    int t=0;
    vector<int>C;

    for(int i=0;i<A.size();i++){
        t+=A[i];
        if(i<B.size()) t+=B[i];
        C.push_back(t%10);
        t/=10;
    }

    if(t) C.push_back(t);

    return C;
}

int main(){
    string a,b;
    cin>>a>>b;
    
    vector<int>A,B;
    for(int i=a.size()-1;i>=0;i--) A.push_back(a[i]-'0');
    for(int i=b.size()-1;i>=0;i--) B.push_back(b[i]-'0');

    vector<int>C=add(A,B);

    for(int i=C.size()-1;i>=0;i--) cout<<C[i];
    return 0;
}