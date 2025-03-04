#include "cppsrc/data_handlers/data_client.hpp"
#include "cppsrc/utils/trade.hpp"
#include "gtest/gtest.h"

TEST(DataClientTests, ParseMessageTest)
{
    intproj::DataClient data_client;
    cpr::Response response;
    response.status_code = 200;
    response.text =
      "[{\"timestamp\": 123456789, \"tid\": \"123456789\", \"price\": \"123.45\", \"amount\": \"0.12345678\", "
      "\"type\": \"buy\"}]";
    std::vector<intproj::Trade> trades = data_client.parse_message(response);
    ASSERT_EQ(trades.size(), 1);
    ASSERT_NEAR(trades[0].price, 123.45, 1e-4);
    ASSERT_NEAR(trades[0].volume, 0.12345678, 1e-4);
    ASSERT_EQ(trades[0].side, intproj::Side::BUY);
}
