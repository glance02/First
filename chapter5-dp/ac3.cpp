#include<iostream>
using namespace std;
const int N=1e3+10;
int n,m;
int v[N],w[N];
int f[N][N];

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    cin>>n>>m;
    for(int i=1;i<=n;i++) cin>>v[i]>>w[i];

    for(int i=1;i<=n;i++){
        for(int j=0;j<=m;j++){
            f[i][j]=f[i-1][j];
            if(j>=v[i])
                f[i][j]=max(f[i-1][j],f[i][j-v[i]]+w[i]);
        }
    }

    cout<<f[n][m]<<endl;
    return 0;
}