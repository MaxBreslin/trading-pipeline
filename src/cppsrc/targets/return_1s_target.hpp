#pragma once

#include "base_target.hpp"

#include <cmath>
#include <queue>

namespace intproj {

class ReturnOneS : public BaseTarget
{
  public:
    float compute_target(std::vector<std::tuple<float, float, bool>> const &data) override
    {
        float avgprice = compute_avgprice(data);

        if (last_avgprice == -1.0 || avgprice == -1.0) {
            last_avgprice = avgprice;
            return 0.0;
        }

        float return_one_s = avgprice - last_avgprice;
        last_avgprice = avgprice;
        return return_one_s;
    }

  private:
    float last_avgprice = -1.0;

    static float compute_avgprice(std::vector<std::tuple<float, float, bool>> data)
    {
        if (data.size() == 0) { return -1.0; }
        float sum = 0.0;
        for (auto &t : data) { sum += std::get<0>(t); }
        return sum / static_cast<float>(data.size());
    }
};


}// namespace intproj