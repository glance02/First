#include <bits/stdc++.h>
using namespace std;

int board[8][8];
bool colUsed[8];
bool diag1[15]; // r + c
bool diag2[15]; // r - c + 7
int best;

void dfs(int row, int sum) {
    if (row == 8) {
        best = max(best, sum);
        return;
    }
    for (int c = 0; c < 8; ++c) {
        int d1 = row + c;
        int d2 = row - c + 7;
        if (!colUsed[c] && !diag1[d1] && !diag2[d2]) {
            colUsed[c] = diag1[d1] = diag2[d2] = true;
            dfs(row + 1, sum + board[row][c]);
            colUsed[c] = diag1[d1] = diag2[d2] = false;
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    
    int k;
    if (!(cin >> k)) return 0;
    for (int t = 0; t < k; ++t) {
        for (int i = 0; i < 8; ++i)
            for (int j = 0; j < 8; ++j)
                cin >> board[i][j];
        memset(colUsed, 0, sizeof(colUsed));
        memset(diag1, 0, sizeof(diag1));
        memset(diag2, 0, sizeof(diag2));
        best = 0;
        dfs(0, 0);
        cout << best << "\n";
    }
    return 0;
}
