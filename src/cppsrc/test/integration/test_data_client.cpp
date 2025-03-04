#include "cppsrc/data_handlers/data_client.hpp"
#include "cppsrc/utils/trade.hpp"
#include "gtest/gtest.h"

TEST(DataClientIntegrationTests, GetDataTest)
{
    intproj::DataClient data_client("https://api.gemini.com/v1", "/trades/btcusd", 1740757948, 100, 50, 0);
    std::vector<intproj::Trade> trades = data_client.get_data();
    ASSERT_FALSE(trades.empty());
    ASSERT_EQ(trades.size(), 50);

    data_client.with_timestamp = 1;
    trades = data_client.get_data();
    ASSERT_TRUE(trades.empty());
}
