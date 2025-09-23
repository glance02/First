#include<iostream>
using namespace std;
const int N=1e5+10;
int n,p[N];

int lowbit(int x){
    return x&-x;
}

int main(){
    cin>>n;
    for(int i=0;i<n;i++){
        int x;cin>>x;
        int ans=0;
        while(x!=0){
            x-=lowbit(x);
            ans++;
        }
        cout<<ans<<" ";
    }
    return 0;
}