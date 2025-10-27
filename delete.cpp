#include<iostream>
#include<cstring>
#include<algorithm>
using namespace std;
char s[100][10];
bool cmp(int a,int b){
    return a<b;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    int a[]={2,1,4,5,6,1};
    sort(a,a+6,cmp);
    for(int i=0;i<6;i++) cout<<a[i]<<" ";
    return 0;
}