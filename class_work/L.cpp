#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);

    int T;cin >> T;
    while (T--) {
        string s;
        cin >> s;

        if (s.empty()) {
            cout << 0 << "\n";
            continue;
        }

        vector<int> freq(26, 0);
        for (char c : s) freq[c - 'a']++;

        priority_queue<int, vector<int>, greater<int>> pq;
        for (int f : freq) {
            if (f > 0) pq.push(f);
        }

        // 如果只有一种字符，哈夫曼长度 = 该字符数量
        if (pq.size() == 1) {
            cout << pq.top() << "\n";
            continue;
        }

        long long ans = 0;
        while (pq.size() > 1) {
            int a = pq.top(); pq.pop();
            int b = pq.top(); pq.pop();
            int sum = a + b;
            ans += sum;
            pq.push(sum);
        }

        cout << ans << "\n";
    }

    return 0;
}
