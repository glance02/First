#include<iostream>
#include<cstring>
using namespace std;
const int N=1e5+3;
int h[N],e[N],ne[N],idx;

//插入一个数x
void insert(int x){
    int k=(x%N+N)%N;
    //这边使用头插
    e[idx]=x;
    ne[idx]=h[k];
    h[k]=idx++;
}

//查找有没有x
bool find(int x){
    int k=(x%N+N)%N;

    for(int i=h[k];i!=-1;i=ne[i]){
        if(e[i]==x) return true;
    }

    return false;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    memset(h,-1,sizeof h);//原来memset是cstring头文件里面的函数

    int n;cin>>n;
    while(n--){
        string s;cin>>s;
        if(s=="I"){
            int x;cin>>x;
            insert(x);
        }else{
            int x;cin>>x;
            if(find(x)) cout<<"Yes"<<endl;
            else cout<<"No"<<endl;
        }
    }
    return 0;
}