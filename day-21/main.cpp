#include <cstdio>
#include <map>
#include <vector>
#include <cstdint>

using u64 = std::uint64_t;


struct State {
    int score0;
    int score1;
    int pos0;
    int pos1;
    int turn;

    std::weak_ordering operator<=>(const State&) const = default;

    void Roll(int value) {
        if (turn == 0) {
            pos0 += value;
            pos0 = ((pos0 - 1) % 10) + 1;
            score0 += pos0;
        }
        else {
            pos1 += value;
            pos1 = ((pos1 - 1) % 10) + 1;
            score1 += pos1;
        }
        turn ^= 1;
    }
};

/*
 * from collections import Counter
 * rolls = [(i, j, k) for i in range(1, 4) for j in range(1, 4) for k in range(1, 4)]
 *
 * print(Counter([sum(roll) for roll in rolls]).most_common())
 * */

const std::vector<std::pair<u64, u64>> rolls = {
        {3, 1}, {4, 3}, {5, 6}, {6, 7}, {7, 6}, {8, 3}, {9, 1}
};


int main() {
    std::map<State, u64> state_counts{};

    // starting input:
    state_counts.emplace(State{0, 0, 6, 10, 0}, 1);
    u64 win0 = 0;
    u64 win1 = 0;

    while (!state_counts.empty()) {
        const auto [state, statecount] = *state_counts.begin();
        state_counts.erase(state_counts.begin());

        for (auto [roll, rollcount] : rolls) {
            auto next = state;

            next.Roll(roll);
            if (next.score0 >= 21) {
                win0 += statecount * rollcount;
            }
            else if (next.score1 >= 21) {
                win1 += statecount * rollcount;
            }
            else {
                if (!state_counts.contains(next)) {
                    state_counts.emplace(next, statecount * rollcount);
                }
                else {
                    state_counts[next] += statecount * rollcount;
                }
            }
        }
    }

    std::printf("%llu / %llu\n", win0, win1);

    return 0;
}
