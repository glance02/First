#include<iostream>
#include<cstring>
using namespace std;
const int N=1010;
int s[N];
int f[N][N];

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    int n;cin>>n;
    //初始化f
    memset(f,0x3f,sizeof f);
    for(int i=1;i<=n;i++){
        cin>>s[i];
        s[i]+=s[i-1];//计算前缀和数组
        f[i][i]=0;
    }

    for(int len =2;len<=n;len++){
        for(int i=1;i+len-1<=n;i++){
            int l=i,r=i+len-1;
            // f[l][r]=1e9;
            for(int k=l;k<=r-1;k++){
                int tmp=f[l][k]+f[k+1][r]+s[r]-s[l-1];
                f[l][r]=min(f[l][r],tmp);
            }
        }
    }

    cout<<f[1][n];
    return 0;
}