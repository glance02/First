#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);

    string key, cipher;
    cin >> key >> cipher;

    string plain;
    int keyLen = key.size();
    int j = 0; // 指向密钥的下标

    for (int i = 0; i < (int)cipher.size(); ++i) {
        char c = cipher[i];
        char k = key[j % keyLen];
        int shift = tolower(k) - 'a';  // 密钥偏移量 0-25

        if (isalpha(c)) {
            if (isupper(c)) {
                int val = (c - 'A' - shift + 26) % 26;
                plain += char('A' + val);
            } else {
                int val = (c - 'a' - shift + 26) % 26;
                plain += char('a' + val);
            }
            ++j; // 只在遇到字母时密钥前进（本题密文仅有字母）
        } else {
            plain += c; // 非字母原样输出
        }
    }

    cout << plain << "\n";
    return 0;
}
