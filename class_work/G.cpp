#include<bits/stdc++.h>
using namespace std;
const int N=20;
char c[N];
char ori[N];

bool check(int n){
    for(int i=0;i<n;i++){
        if(c[i]!=ori[i])
            return false;
    }
    return true;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    cin>>c;
    //去掉最后一个逗号
    c[strlen(c)-1]='\0';
    int n=strlen(c);
    sort(c,c+n);
    for(int i=0;i<n;i++) ori[i]=c[i];
    cout<<ori<<" ";
    next_permutation(c,c+n);
    while(!check(n)){
        cout<<c<<" ";
        next_permutation(c,c+n);
        
    }
    return 0;
}