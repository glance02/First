#include<iostream>
#include<cstring>
using namespace std;
const int N=510,INF=1e9;//INF表示无穷大，-INF表示无穷小
int n;
int a[N][N],f[N][N];

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    cin>>n;
    for(int i=1;i<=n;i++){
        for(int j=1;j<=i;j++)
            cin>>a[i][j];
    }
    //初始化一下f数组
    memset(f,128,sizeof f);//输入128的时候是初始化为一个很小的数字

    //开始计算
    f[1][1]=a[1][1];//第一层的最短路径长度一定是其本身
    for(int i=2;i<=n;i++){
        for(int j=1;j<=i;j++){
            f[i][j]=max(f[i-1][j-1]+a[i][j],f[i-1][j]+a[i][j]);
        }
    }

    int ans=-INF;
    for(int i=1;i<=n;i++){
        ans=max(f[n][i],ans);
    }

    cout<<ans<<endl;
    return 0;
}