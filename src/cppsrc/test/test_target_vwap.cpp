#include "cppsrc/targets/vwap_target.hpp"
#include "gtest/gtest.h"

TEST(TargetTests, VWAPTest)
{
    intproj::VWAPTarget vw;
    EXPECT_EQ(vw.compute_target({}), 0);
    EXPECT_EQ(vw.compute_target({ { 2, 1, false } }), 2);
    EXPECT_EQ(vw.compute_target({ { 1, 1, false } }), 3. / 2);
    EXPECT_EQ(vw.compute_target({ { 3, 2, false }, { 1, 1, true } }), 2);
    EXPECT_NEAR(vw.compute_target({ { 1, 5, false }, { 2, 1, true } }), 17. / 11, 1e-5);
    EXPECT_NEAR(vw.compute_target({ { 2, 1, false }, { 1, 1, true } }), 20. / 13, 1e-5);
    EXPECT_NEAR(vw.compute_target({ { 1, 1, false }, { 1, 1, true } }), 10. / 7, 1e-5);
    EXPECT_NEAR(vw.compute_target({}), 19. / 13, 1e-5);
}
