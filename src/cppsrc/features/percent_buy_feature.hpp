#pragma once

#include "base_feature.hpp"

#include <cmath>

namespace intproj {

class PercentBuyFeature : public BaseFeature
{
  public:
    float compute_feature(std::vector<std::tuple<float, float, bool>> const &data) override
    {
        if (data.empty()) { return 0.0; }
        float count = 0.0;
        for (auto &t : data) { count += static_cast<float>(std::get<2>(t)); }
        return count / static_cast<float>(data.size());
    }
};


}// namespace intproj