#include<iostream>
using namespace std;
const int N=1e5+10;

//head指的是头节点的下标，idx表示当前已经用到了哪个点
int head,e[N],ne[N],idx;

void init(){
    head=-1;
    idx=1;//我这边改成从1开始了，yxc写的是从0开始，我感觉我这样好理解一点
}

void add_to_head(int x){
    e[idx]=x;
    ne[idx]=head;
    head=idx++;
}

void add_to_k(int k,int x){//将x插入到k后面
    e[idx]=x;
    ne[idx]=ne[k];
    ne[k]=idx++;
}

void remove(int k){//将下标是k的后面的点删除
    if(k==0){
        head=ne[head];
    }else{
        ne[k]=ne[ne[k]];
    }
}

int main(){
    ios::sync_with_stdio(false);
    int n;cin>>n;

    init();
    while(n--){
        int k,x;
        string op;
        cin>>op;
        if(op=="H"){
            cin>>x;
            add_to_head(x);
        }else if(op=="D"){
            cin>>k;
            remove(k);
        }else{
            cin>>k>>x;
            add_to_k(k,x);
        }
    }
    
    for(int i=head;i!=-1;i=ne[i])
        cout<<e[i]<<" ";
    return 0;
}