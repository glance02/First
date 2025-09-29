#include<iostream>
#include<vector>
using namespace std;

//减法要有一定的前提，A>=B，A>0,B>0
vector<int> sub(vector<int>&A,vector<int>&B){
    vector<int>C;
    int t=0;

    for(int i=0;i<A.size();i++){
        //先减借位,再减B
        t=A[i]-t;
        if(i<B.size()) t-=B[i];
        //处理C
        C.push_back((t+10)%10);
        //处理t
        if(t<0) t=1;
        else t=0;
    }
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    
    return 0;
}