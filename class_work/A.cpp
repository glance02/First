#include<iostream>
#include<queue>
#include<algorithm>
using namespace std;
#define LL long long 
priority_queue<LL,vector<LL>,greater<LL>>q;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    int n,l;cin>>n>>l;
    for(int i=0;i<n;i++){
        LL x;cin>>x;
        q.push(x);
    }
    
    LL ans=0;
    LL a,b;
    while(q.size()>1){
        a=q.top();q.pop();
        b=q.top();q.pop();
        ans=ans+a+b;
        q.push(a+b);
    }

    cout<<ans;
    return 0;
}