#include<iostream>
#include<cstring>
#include<map>
using namespace std;
typedef pair<int,int> Dem;
const int N=105;
int f[N][N];
map<char,Dem> dem;
Dem p[N];
char cal[N];
int n,m;

bool check(int len){
    for(int i=1;i<len;i++){
        if(p[i].second!=p[i+1].first)
            return false;
    }   
    return true;
}

int fun(int len){
    // 初始化对角为0
    for(int i=1;i<=len;i++) f[i][i]=0;
    
    for(int l=2;l<=len;l++){  // l 表示区间长度
        for(int i=1;i+l-1<=len;i++){
            int L=i, R=i+l-1;
            f[L][R]=1e9;
            for(int k=L;k<R;k++){  // k<R 不是 k<=R-1
                int tmp=f[L][k]+f[k+1][R]+p[L].first*p[k].second*p[R].second;
                f[L][R]=min(f[L][R],tmp);
            }
        }
    }
    return f[1][len];
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    
    while(cin>>n>>m){  // 多组数据输入
        dem.clear();  // 清空上一组数据
        
        for(int i=1;i<=n;i++){
            char c;
            int x,y;
            cin>>c>>x>>y;
            dem[c]={x,y};
        }
        
        for(int i=1;i<=m;i++){  // 改用 for 循环更清晰
            cin>>(cal+1);
            int len=strlen(cal+1);
            
            // 构建 p 数组
            for(int j=1;j<=len;j++){
                p[j]=dem[cal[j]];
            }
            
            // 判断能否相乘
            if(!check(len)){
                cout<<"MengMengDa"<<endl;
            }
            else{
                // 计算最小连乘次数
                cout<<fun(len)<<endl;
            }
        }
    }
    return 0;
}