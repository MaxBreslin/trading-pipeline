#include "cppsrc/features/percent_buy_feature.hpp"
#include "gtest/gtest.h"

TEST(FeatureTests, PctBuyTest)
{
    intproj::PercentBuyFeature ptf;

    EXPECT_EQ(ptf.compute_feature({ { 1, 1, false } }), 0);
    EXPECT_EQ(ptf.compute_feature({ { 1, 1, false }, { 1, 1, true } }), 0.5);
    EXPECT_EQ(ptf.compute_feature({ { 1, 1, true } }), 1);
    EXPECT_NEAR(
      ptf.compute_feature({ { 1, 1, false }, { 1, 1, true }, { 1, 1, false }, { 1, 1, false }, { 1, 1, true } }),
      0.4,
      1e-5);
}
