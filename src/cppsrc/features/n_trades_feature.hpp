#pragma once

#include "base_feature.hpp"

namespace intproj {

class NTradesFeature : public BaseFeature
{
  public:
    float compute_feature(std::vector<std::tuple<float, float, bool>> const &data) override
    {
        return static_cast<float>(data.size());
    }
};


}// namespace intproj