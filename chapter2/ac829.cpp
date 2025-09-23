#include<iostream>
using namespace std;
const int N=1e5+10;
int q[N],hh,tt=-1;
string empty(){
    if(hh<=tt) return "NO";
    else return "YES";
}

int main(){
    ios::sync_with_stdio(false);
    int n;cin>>n;
    while(n--){
        string s;cin>>s;
        int x;
        if(s=="push"){
            cin>>x;
            q[++tt]=x;
        }else if(s=="pop"){
            hh++;
        }else if(s=="empty"){
            cout<<empty()<<endl;;
        }else{
            cout<<q[hh]<<endl;
        }
    }
    return 0;
}