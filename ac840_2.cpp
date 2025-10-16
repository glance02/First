#include<iostream>
#include<cstring>
using namespace std;
const int N=2e5+3;

//0x3f3f3f3f是一个比1e9大的数
int h[N],null=0x3f3f3f3f;

//核心方法，如果有x则返回x的位置，没有则返回x应该插入的位置
int find(int x){
    int k=(x%N+N)%N;

    while(h[k]!=null&&h[k]!=x){//如果k处有数并不等于x，则去下一个位置
        k++;
        if(k==N) k=0;
    }

    return k;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    memset(h,0x3f,sizeof h);

    int n;cin>>n;
    while(n--){
        string s;cin>>s;
        int x;cin>>x;

        int k=find(x);
        if(s=="I"){
            h[k]=x;
        }else{
            if(h[k]==x) cout<<"Yes"<<endl;
            else cout<<"No"<<endl;
        }
    }

    return 0;
}