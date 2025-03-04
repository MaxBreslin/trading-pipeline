#pragma once

#include <tuple>
#include <vector>

namespace intproj {

class BaseTarget
{
  public:
    virtual float compute_target(std::vector<std::tuple<float, float, bool>> const &data) = 0;

    virtual ~BaseTarget() = default;
};


}// namespace intproj
