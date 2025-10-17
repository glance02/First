#include<iostream>
using namespace std;
typedef unsigned long long ULL;
const int N=1e5+10,P=131;

char s[N];
int h[N],p[N];

ULL getans(int l,int r){
    return h[r]-h[l-1]*p[r-l+1];
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    int n,m;cin>>n>>m;
    cin>>s+1;

    //处理一下p次方和h，这里把ASCII码值当作每个字母的值
    p[0]=1;//p的0次方等于1
    for(int i=1;i<=n;i++){
        p[i]=p[i-1]*P;
        h[i]=h[i-1]*P+s[i];
    }
    while(m--){
        int l1,r1,l2,r2;
        cin>>l1>>r1>>l2>>r2;

        if(getans(l1,r1)==getans(l2,r2)) cout<<"Yes\n";
        else cout<<"No\n";
    }
    return 0;
}