#include "cppsrc/features/percent_sell_feature.hpp"
#include "gtest/gtest.h"

TEST(FeatureTests, PctSellTest)
{
    intproj::PercentSellFeature psf;

    EXPECT_EQ(psf.compute_feature({ { 1, 1, false } }), 1);
    EXPECT_EQ(psf.compute_feature({ { 1, 1, false }, { 1, 1, true } }), 0.5);
    EXPECT_EQ(psf.compute_feature({ { 1, 1, true }, { 1, 1, true }, { 1, 2, true } }), 0);
    EXPECT_NEAR(psf.compute_feature({ { 1, 1, false }, { 1, 1, true }, { 1, 2, false } }), 0.67, 1e-2);
}
