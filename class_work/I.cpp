#include<iostream>
using namespace std;

const int MOD = 1000000007;
const int MAXN = 105;
long long dp[MAXN];

void init(){
    // 预处理所有可能的结果
    dp[0] = 1;
    dp[1] = 1;
    for(int i = 2; i <= 100; i++){
        dp[i] = (dp[i-1] + dp[i-2]) % MOD;
    }
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0); cout.tie(0);
    
    init();  // 预处理
    
    int n;
    while(cin >> n){
        cout << dp[n] << endl;
    }
    
    return 0;
}