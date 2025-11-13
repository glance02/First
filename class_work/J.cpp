#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = (1LL<<60);

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    
    int n, m, start, end;
    if (!(cin >> n >> m >> start >> end)) return 0;
    vector<ll> score(n);
    for (int i = 0; i < n; ++i) cin >> score[i];
    
    vector<vector<pair<int,int>>> adj(n);
    for (int i = 0; i < m; ++i) {
        int x, y, z;
        cin >> x >> y >> z;
        // 无向图
        adj[x].push_back({y, z});
        adj[y].push_back({x, z});
    }
    
    vector<ll> dist(n, INF);
    dist[start] = 0;
    priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<pair<ll,int>>> pq;
    pq.push({0, start});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dist[u]) continue;
        for (auto &e : adj[u]) {
            int v = e.first;
            int w = e.second;
            if (dist[v] > d + w) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
        }
    }
    
    vector<int> order;
    order.reserve(n);
    for (int i = 0; i < n; ++i) if (dist[i] < INF) order.push_back(i);
    sort(order.begin(), order.end(), [&](int a, int b){
        if (dist[a] != dist[b]) return dist[a] < dist[b];
        return a < b;
    });
    
    vector<ll> f(n, -INF);
    f[start] = score[start];
    for (int u : order) {
        if (f[u] == -INF) continue; // 无法到达 u 的最短路径上取得有效分数
        for (auto &e : adj[u]) {
            int v = e.first;
            int w = e.second;
            if (dist[u] + w == dist[v]) {
                // 可以从 u 转到 v 且仍然保持到 v 的最短距离
                f[v] = max(f[v], f[u] + score[v]);
            }
        }
    }
    
    cout << dist[end] << " " << f[end] << "\n";
    return 0;
}
