#include<iostream>
#include<vector>
using namespace std;

vector<int> mul(vector<int>&A,int b){
    int t=0;
    vector<int>C;

    for(int i=0;i<A.size();i++){
        t+=A[i]*b;
        C.push_back(t%10);
        t/=10;
    }
    //另外处理进位
    while(t){
        C.push_back(t%10);
        t/=10;
    }

    //去除前导零
    while(C.size()>1&&C.back()==0) C.pop_back();

    return C;
}

int main(){
    vector<int>A;
    int b;string a;
    cin>>a>>b;

    for(int i=a.size()-1;i>=0;i--) A.push_back(a[i]-'0');

    vector<int>C=mul(A,b);

    for(int i=C.size()-1;i>=0;i--) cout<<C[i];
    return 0;
}