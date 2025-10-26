#include<iostream>
#include<cstring>
using namespace std;
const int N=1010;
int n,m;
char a[N],b[N];
int f[N][N];

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    cin>>n>>a+1>>m>>b+1;

    //初始化
    memset(f,0x3f,sizeof f);
    for(int i=0;i<=n;i++) f[i][0]=i;
    for(int i=0;i<=m;i++) f[0][i]=i;

    for(int i=1;i<=n;i++){
        for(int j=1;j<=m;j++){
            f[i][j]=min(f[i][j-1]+1,f[i-1][j]+1);//添加和删除
            f[i][j]=min(f[i][j],f[i-1][j-1]+1);//替换的操作
            if(a[i]==b[j]) f[i][j]=min(f[i][j],f[i-1][j-1]);//不操作的部分
        }
    }

    cout<<f[n][m]<<endl;
    return 0;
}