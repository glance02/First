#include<iostream>
#include<cstring>
using namespace std;
const int N=1010;
int n,m;
char a[N],b[N];
int f[N][N];
char s[N][15];


int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    cin>>n>>m;
    for(int i=1;i<=n;i++) cin>>s[i]+1;

    while(m--){
        char str[15];int op;
        // scanf("%s%d",str+1,&op);
        cin>>str+1>>op;
        int cnt=0;
        //每次都计算一下s里的n个字符串变成str需要的次数
        for(int k=1;k<=n;k++){
            //计算s[k]->str需要的最少的操作次数
            int x=strlen(s[k]+1),y=strlen(str+1);

            //初始化
            // memset(f,0x3f,sizeof f);//我其实还是有点不理解为什么不需要初始化一下这个数组
            for(int i=0;i<=x;i++) f[i][0]=i;
            for(int i=0;i<=y;i++) f[0][i]=i;
            
            for(int i=1;i<=x;i++){
                for(int j=1;j<=y;j++){
                    f[i][j]=min(f[i-1][j],f[i][j-1])+1;
                    f[i][j]=min(f[i][j],f[i-1][j-1]+(s[k][i]!=str[j]));
                }
            }
            //判断一下是否可以转换
            if(f[x][y]<=op) cnt++;
        }
        cout<<cnt<<"\n";
    }

    return 0;
}