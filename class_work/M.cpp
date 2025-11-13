#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);

    vector<int> cost(11);
    for (int i = 1; i <= 10; ++i) {
        if (!(cin >> cost[i])) return 0;
    }
    int n;
    cin >> n;

    const int INF = 1e9;
    vector<int> dp(n + 1, INF);
    dp[0] = 0;
    for (int i = 1; i <= n; ++i) {
        for (int k = 1; k <= 10; ++k) {
            if (k <= i) dp[i] = min(dp[i], dp[i - k] + cost[k]);
        }
    }

    cout << dp[n] << "\n";
    return 0;
}
