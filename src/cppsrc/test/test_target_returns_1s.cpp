#include "cppsrc/targets/return_1s_target.hpp"
#include "gtest/gtest.h"

TEST(TargetTests, ReturnOneSTest)
{
    intproj::ReturnOneS r1;
    EXPECT_EQ(r1.compute_target({}), 0);
    EXPECT_EQ(r1.compute_target({ { 2, 1, false } }), 0);
    EXPECT_EQ(r1.compute_target({ { 1, 1, false } }), -1);
    EXPECT_EQ(r1.compute_target({ { 3, 2, false }, { 1, 1, true } }), 1);
    EXPECT_EQ(r1.compute_target({ { 2, 5, false }, { 2, 1, true }, { 2, 1, true }, { 2, 1, true } }), 0);
    EXPECT_EQ(r1.compute_target({ { 2, 1, false }, { 1, 1, true }, { 6, 1, true } }), 1);
    EXPECT_EQ(r1.compute_target({ { 1, 1, false }, { 1, 1, false }, { 1, 1, true }, { 1, 1, true } }), -2);
    EXPECT_EQ(r1.compute_target({}), 0.0);
}
