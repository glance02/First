#include <bits/stdc++.h>
using namespace std;

int n;
bool isPrime[40]; 

int dfs(int last, int mask, int fullMask) {
    if (mask == fullMask) {
       
        return isPrime[last + 1] ? 1 : 0;
    }
    int cnt = 0;
    for (int x = 2; x <= n; ++x) {
        int bit = 1 << (x - 1);
        if (!(mask & bit) && isPrime[last + x]) {
            cnt += dfs(x, mask | bit, fullMask);
        }
    }
    return cnt;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);

    fill(begin(isPrime), end(isPrime), false);
    vector<int> primeList = {2,3,5,7,11,13,17,19,23,29,31,37};
    for (int p : primeList) if (p < 40) isPrime[p] = true;

    while ( (cin >> n) ) {
        int fullMask = (1 << n) - 1;
        int startMask = 1 << 0;
        int ans = dfs(1, startMask, fullMask);
        cout << ans << "\n";
    }
    return 0;
}
