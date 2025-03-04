#pragma once

#include "base_feature.hpp"

#include <queue>

namespace intproj {

class FiveTickVolumeFeature : public BaseFeature
{
  public:
    float compute_feature(std::vector<std::tuple<float, float, bool>> const &data) override
    {
        if (volumes.size() >= 5) {
            five_tick_volume -= volumes.front();
            volumes.pop();
        }
        float volume = 0.0;
        for (auto &t : data) { volume += std::get<1>(t); }
        five_tick_volume += volume;
        volumes.push(volume);
        return five_tick_volume;
    }

  private:
    std::queue<float> volumes = {};
    float five_tick_volume = 0.0;
};


}// namespace intproj