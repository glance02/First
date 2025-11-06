#include<iostream>
using namespace std;
const int m=100000007;

long long quickpow(long long a, long long b) {
   long long sum = 1;
   while (b > 0) {
       if (b & 1) // 判断b的最低位是否为1
           sum = sum * a % m; // 累乘当前项并取模
       a = a * a % m; // 底数翻倍并取模
       b >>= 1; // 指数右移一位，相当于除以2
   }
   return sum;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    int n;
    while(cin>>n){
        long long ans=0;
        for(int i=1;i<=n;i++){
            ans+=quickpow(i,i);
        }

        cout<<(ans+1)%m<<endl;
    }
    return 0;
}