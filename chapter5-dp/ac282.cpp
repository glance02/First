#include<iostream>
#include<cstring>
using namespace std;
const int N=310;

int n;
int s[N];
int f[N][N];

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    cin>>n;
    //把数组换成前缀和，加快计算速度
    for(int i=1;i<=n;i++){
        cin>>s[i];
        s[i]+=s[i-1];
    }

    memset(f,0x3f,sizeof f);//初始化f数组为最大值
    for(int i=1;i<=n;i++) f[i][i]=0;//当len=1的时候，花费的代价是0，这里因为用mem覆盖了，所以重新设置一下

    //要保证计算当前状态的时候，使用到的状态都已经计算过了，所以使用区间长度来推进计算
    for(int len=2;len<=n;len++){//len=1的时候，花费的代价是0，这个在全局定义的变量中已经设置为0了
        for(int i=1;i+len-1<=n;i++){
            int l=i,r=i+len-1;
            // f[l][r]=1e8;//为什么在这里初始化，不使用memset，因为计算的时候会用到1那一层
            for(int k=l;k<r;k++){
                f[l][r]=min(f[l][r],f[l][k]+f[k+1][r]+s[r]-s[l-1]);
            }
        }
    }

    cout<<f[1][n];
    return 0;
}