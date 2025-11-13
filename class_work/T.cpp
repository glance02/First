#include <iostream>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);

    int T;
    if (!(cin >> T)) return 0;

    while (T--) {
        string S;
        long long k;
        cin >> S >> k;

        // 解密需要反向偏移
        k = ((-k) % 26 + 26) % 26;

        for (char &c : S) {
            if (c >= 'A' && c <= 'Z') {
                c = (char)('A' + (c - 'A' + k) % 26);
            } else if (c >= 'a' && c <= 'z') {
                c = (char)('a' + (c - 'a' + k) % 26);
            }
            // 其他字符保持不变
        }
        cout << S << '\n';
    }

    return 0;
}
