#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <unordered_map>
#include <vector>
#include <cmath>
#include <functional> // For std::hash and std::size_t

namespace py = pybind11;

struct pair_hash {
    template <class T1, class T2>
    std::size_t operator () (const std::pair<T1,T2> &pair) const {
        auto hash1 = std::hash<T1>{}(pair.first);
        auto hash2 = std::hash<T2>{}(pair.second);
        return hash1 ^ hash2;  // Combine the two hash values.
    }
};

std::unordered_map<std::pair<std::string, std::string>, double, pair_hash> calculate_npmi(
    const std::vector<std::vector<std::string>>& documents,
    int window_size,
    double minimum_pmi,
    int min_count
) {
    std::unordered_map<std::string, int> word_freq;
    // word_freq.reserve(1000); // Example reservation size
    std::unordered_map<std::pair<std::string, std::string>, int, pair_hash> pair_count;
    // pair_count.reserve(5000); // Example reservation size
    int total_words = 0;

    for (const auto& doc : documents) {
        std::unordered_set<std::string> seen;
        for (size_t i = 0; i < doc.size(); ++i) {
            if (seen.insert(doc[i]).second) {
                ++word_freq[doc[i]];
            }
            for (size_t j = i + 1; j < std::min(i + window_size, doc.size()); ++j) {
                if (doc[i] == doc[j]) continue;
                auto pair = std::make_pair(doc[i], doc[j]);
                if (pair.first > pair.second) std::swap(pair.first, pair.second);
                pair_count[pair]++;
            }
        }
        total_words += doc.size();
    }

    // Calculate NPMI using optimized algorithms or approximations where necessary
    std::unordered_map<std::pair<std::string, std::string>, double, pair_hash> npmi;
    for (auto& pair : pair_count) {
        if (pair.second >= min_count) {
            double p_x = double(word_freq[pair.first.first]) / total_words;
            double p_y = double(word_freq[pair.first.second]) / total_words;
            double p_xy = double(pair.second) / total_words;
            double pmi = std::log(p_xy / (p_x * p_y));
            double npmi_value = pmi / -std::log(p_xy);
            if (npmi_value > minimum_pmi) {
                npmi[pair.first] = npmi_value;
            }
        }
    }

    return npmi;
}

PYBIND11_MODULE(pynpmi, m) {
    m.def("calculate_npmi", &calculate_npmi, "A function to calculate normalized PMI",
          py::arg("documents"), py::arg("window_size"), py::arg("minimum_pmi"), py::arg("min_count"));
}
