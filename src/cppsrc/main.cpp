#include "data_handlers/data_client.hpp"
#include "features/five_tick_volume_feature.hpp"
#include "features/n_trades_feature.hpp"
#include "features/percent_buy_feature.hpp"
#include "features/percent_sell_feature.hpp"
#include "targets/return_1s_target.hpp"
#include "targets/vwap_target.hpp"
#include "utils/trade.hpp"

#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

int main()
{
    std::cout << "hello\n";
}

int add(int a, int b)
{
    return a + b;
}

PYBIND11_MODULE(intern, m)
{
    m.def("add", &add, "Adds two numbers");

    pybind11::class_<intproj::BaseFeature>(m, "BaseFeature")
      .def("compute_feature", &intproj::BaseFeature::compute_feature, pybind11::arg("data"));

    pybind11::class_<intproj::NTradesFeature, intproj::BaseFeature>(m, "NTradesFeature").def(pybind11::init<>());
    pybind11::class_<intproj::PercentBuyFeature, intproj::BaseFeature>(m, "PercentBuyFeature").def(pybind11::init<>());
    pybind11::class_<intproj::PercentSellFeature, intproj::BaseFeature>(m, "PercentSellFeature")
      .def(pybind11::init<>());
    pybind11::class_<intproj::FiveTickVolumeFeature, intproj::BaseFeature>(m, "FiveTickVolumeFeature")
      .def(pybind11::init<>());

    pybind11::class_<intproj::BaseTarget>(m, "BaseTarget")
      .def("compute_target", &intproj::BaseTarget::compute_target, pybind11::arg("data"));

    pybind11::class_<intproj::VWAPTarget, intproj::BaseTarget>(m, "VWAPTarget")
      .def(pybind11::init<int>(), pybind11::arg("tick_window_size") = 5);
    pybind11::class_<intproj::ReturnOneS, intproj::BaseTarget>(m, "ReturnOneS").def(pybind11::init<>());

    pybind11::enum_<intproj::Side>(m, "Side").value("BUY", intproj::Side::BUY).value("SELL", intproj::Side::SELL);

    pybind11::class_<intproj::Trade>(m, "Trade")
      .def(pybind11::init<float, float, intproj::Side>(),
        pybind11::arg("price"),
        pybind11::arg("volume"),
        pybind11::arg("side"))
      .def_readwrite("price", &intproj::Trade::price)
      .def_readwrite("volume", &intproj::Trade::volume)
      .def_readwrite("side", &intproj::Trade::side);

    pybind11::class_<intproj::DataClient>(m, "DataClient")
      .def(pybind11::init<std::string, std::string, unsigned long, unsigned long, unsigned long, unsigned long>(),
        pybind11::arg("base_url") = "https://api.gemini.com/v1",
        pybind11::arg("query") = "/trades/btcusd",
        pybind11::arg("timestamp") = 0,
        pybind11::arg("since_tid") = 0,
        pybind11::arg("limit_trades") = 50,
        pybind11::arg("with_timestamp") = 0)
      .def("get_data", &intproj::DataClient::get_data)
      .def_readwrite("timestamp", &intproj::DataClient::timestamp)
      .def_readwrite("with_timestamp", &intproj::DataClient::with_timestamp);
}
