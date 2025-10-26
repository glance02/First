#include<iostream>
using namespace std;
const int N=1010;
int f[N],a[N];
int n;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    cin>>n;
    for(int i=1;i<=n;i++) cin>>a[i];

    //复杂度是n^2
    for(int i=1;i<=n;i++){
        f[i]=1;
        for(int j=1;j<i;j++){
            if(a[j]<a[i])
                f[i]=max(f[i],f[j]+1);
        }
    }

    int ans=0;
    for(int i=1;i<=n;i++) ans=max(ans,f[i]);

    cout<<ans;
    return 0;
}