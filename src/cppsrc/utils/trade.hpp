#pragma once

namespace intproj {

enum Side { SELL, BUY };

struct Trade
{
    float price;
    float volume;
    Side side;
};

}// namespace intproj