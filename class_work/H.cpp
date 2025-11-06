#include<iostream>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    int num;
    cin>>num;
    //天下竟有此等取巧之法
    cout<<oct<<num;
    return 0;
}