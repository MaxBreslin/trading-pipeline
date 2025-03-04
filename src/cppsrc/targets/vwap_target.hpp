#pragma once

#include "base_target.hpp"

#include <queue>

namespace intproj {

class VWAPTarget : public BaseTarget
{
  public:
    VWAPTarget(int tick_window_size = 5) : BaseTarget(), tick_window_size(tick_window_size) {}

    float compute_target(std::vector<std::tuple<float, float, bool>> const &data) override
    {
        if (price_volumes.size() >= tick_window_size) {
            five_tick_price_volume -= price_volumes.front();
            price_volumes.pop();
            five_tick_volume -= volumes.front();
            volumes.pop();
        }

        float price_volume = 0.0;
        for (auto &t : data) { price_volume += std::get<0>(t) * std::get<1>(t); }
        five_tick_price_volume += price_volume;
        price_volumes.push(price_volume);

        float volume = 0.0;
        for (auto &t : data) { volume += std::get<1>(t); }
        five_tick_volume += volume;
        volumes.push(volume);

        if (five_tick_volume == 0.0) { return 0.0; }
        return five_tick_price_volume / five_tick_volume;
    }

    int tick_window_size;

  private:
    std::queue<float> price_volumes = {};
    float five_tick_price_volume = 0.0;
    std::queue<float> volumes = {};
    float five_tick_volume = 0.0;
};


}// namespace intproj