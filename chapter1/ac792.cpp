#include<iostream>
#include<vector>
using namespace std;
//A>=B的比较
bool cmp(vector<int>&A,vector<int>&B){
    if(A.size()!=B.size()) return A.size()>B.size();
    for(int i=A.size()-1;i>=0;i--){
        if(A[i]!=B[i]) return A[i]>B[i];
    }
    return true;
}
vector<int> sub(vector<int>&A,vector<int>&B){
    int t=0;
    vector<int>C;

    for(int i=0;i<A.size();i++){
        t=A[i]-t;
        if(i<B.size()) t-=B[i];
        C.push_back((t+10)%10);
        //处理t
        if(t<0) t=1;//需要进位
        else t=0;
    }

    //减法需要去掉前导零
    while(C.size()>1&&C.back()==0) C.pop_back();

    return C;
}

int main(){
    string a,b;
    cin>>a>>b;
    
    vector<int>A,B;
    for(int i=a.size()-1;i>=0;i--) A.push_back(a[i]-'0');
    for(int i=b.size()-1;i>=0;i--) B.push_back(b[i]-'0');
    vector<int>C;
    if(cmp(A,B)){
        C=sub(A,B);
    }else{
        cout<<'-';
        C=sub(B,A);
    }
    
    for(int i=C.size()-1;i>=0;i--) cout<<C[i];

    return 0;
}