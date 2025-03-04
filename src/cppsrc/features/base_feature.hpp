#pragma once

#include <tuple>
#include <vector>

namespace intproj {

class BaseFeature
{
  public:
    virtual float compute_feature(std::vector<std::tuple<float, float, bool>> const &data) = 0;

    virtual ~BaseFeature() = default;
};


}// namespace intproj
