#include<iostream>
using namespace std;
const int N=1e4+10,M=1e6+10;
int n,m;
char s[M], p[N];
int ne[N];

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    cin >>n>>p+1>>m>>s+1;

    //求ne数组
    for(int i=2,j=0;i<=n;i++){//i为主
        while(j&&p[i]!=p[j+1]) j=ne[j];
        if(p[i]==p[j+1]) j++;
        ne[i]=j;
    }
    
    for(int i=1,j=0;i<=n;i++){
        while(j&&s[i]!=p[j+1]) j=ne[j];
        if(s[i]==p[j+1]) j++;
        if(j==n){
            cout<<i-n<<" ";
            j=ne[j];//匹配成功之后，再回退一步进行下一次匹配
        }
    }
    return 0;
}