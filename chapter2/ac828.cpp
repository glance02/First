#include<iostream>
using namespace std;
const int N=1e5+10;

int stk[N],tt;

void push(int x){
    stk[++tt]=x;
}
void pop(){
    tt--;
}
string empty(){
    if(tt>0) return "NO";
    else return "YES";
}
int query(){
    return stk[tt];
}
int main(){
    ios::sync_with_stdio(false);
    int n;cin>>n;
    while(n--){
        string s;cin>>s;
        int x;
        if(s=="push"){
            cin>>x;
            push(x);
        }else if(s=="pop"){
            pop();
        }else if(s=="empty"){
            cout<<empty()<<endl;
        }else{
            cout<<query()<<endl;
        }
    }
    return 0;
}