#include<iostream>
using namespace std;
const int N=2e5+10;
int f[N];
int n,a[N];

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    cin>>n;
    int ans=0;
    for(int i=1;i<=n;i++) cin>>a[i];
    for(int i=1;i<=n;i++){
        if(f[i-1]>0) f[i]=f[i-1]+a[i];
        else f[i]=a[i];

        ans=max(ans,f[i]);
    }
    cout<<ans;
    return 0;
}