#include<iostream>
using namespace std;
const int N=1e5+10;
int stk[N],tt;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    //初始化一下stk，让第一个数等于-1
    stk[++tt]=-1;

    int n;cin>>n;
    for(int i=0;i<n;i++){
        int x;cin>>x;
        //每次都先维护这个单调栈
        while(tt>1&&stk[tt]>=x) tt--;

        cout<<stk[tt]<<" ";

        //最后再把这个数加到栈顶
        stk[++tt]=x;
    }
    return 0;
}