#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    long long n;
    while ( (cin >> n) ) {
        if (n < 0) { cout << 0 << "\n"; continue; }
        if (n == 0) { cout << 0 << "\n"; continue; } 
        // dp[i][k]: 长度为i，末尾恰有k个连续0，且没有"000"
        unsigned long long dp_prev[3] = {0,0,0}, dp_next[3] = {0,0,0};
        dp_prev[0] = 1; // 长度0的空串视为末尾有0个0
        for (int i = 0; i < n; ++i) {
            dp_next[0] = dp_next[1] = dp_next[2] = 0;
            // 追加 '1' , 尾部变为 0 个连续0
            unsigned long long sum = dp_prev[0] + dp_prev[1] + dp_prev[2];
            dp_next[0] += sum;
            // 追加 '0'
            // 从尾部0个0 ,1个0
            dp_next[1] += dp_prev[0];
            // 从尾部1个0 ,2个0
            dp_next[2] += dp_prev[1];
            // 从尾部2个0 ,个0 不允许（会产生"000"），所以不转移
            dp_prev[0] = dp_next[0];
            dp_prev[1] = dp_next[1];
            dp_prev[2] = dp_next[2];
        }
        unsigned long long safe = dp_prev[0] + dp_prev[1] + dp_prev[2];
        unsigned long long total = (n < 64) ? (1ULL << n) : 0ULL; // n<=30 这里安全
        unsigned long long ans = total - safe;
        cout << ans << "\n";
    }
    return 0;
}
