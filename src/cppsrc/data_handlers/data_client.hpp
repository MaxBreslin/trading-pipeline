#pragma once

#include "../utils/trade.hpp"

#include <cpr/cpr.h>
#include <iostream>
#include <nlohmann/json.hpp>
#include <string>

namespace intproj {

class DataClient
{
  public:
    DataClient(std::string base_url = "https://api.gemini.com/v1",
      std::string query = "/trades/btcusd",
      unsigned long timestamp = 0,
      unsigned long since_tid = 0,
      unsigned long limit_trades = 50,
      unsigned long with_timestamp = 0)
      : base_url(base_url), query(query), timestamp(timestamp), since_tid(since_tid), limit_trades(limit_trades),
        with_timestamp(with_timestamp)
    {}
    ~DataClient() = default;

    std::vector<Trade> get_data()
    {
        cpr::Response response = query_api();
        return parse_message(response);
    }

    cpr::Response query_api()
    {
        std::string request_url = base_url + query;
        if (timestamp) { request_url += "?timestamp=" + std::to_string(timestamp); }
        if (since_tid) { request_url += "?since_tid=" + std::to_string(since_tid); }
        if (limit_trades) { request_url += "?limit_trades=" + std::to_string(limit_trades); }

        cpr::Response response = cpr::Get(cpr::Url{ request_url }, cpr::VerifySsl{ false });

        if (response.status_code != 200) {
            std::cerr << "Error: " << response.error.message << std::endl;
            throw std::runtime_error("Error: " + std::to_string(response.status_code));
        }

        return response;
    }


    std::vector<Trade> parse_message(cpr::Response const &message)
    {
        std::vector<Trade> trades;
        if (message.status_code != 200) {
            std::cerr << "Error: " << message.status_code << std::endl;
            return trades;
        }

        nlohmann::json json_response = nlohmann::json::parse(message.text);

        for (auto &trade : json_response) {
            if (with_timestamp && std::to_string((unsigned long)trade["timestamp"]) != std::to_string(with_timestamp)) {
                continue;
            }
            Side side = trade["type"] == "sell" ? Side::SELL : Side::BUY;
            trades.push_back(
              Trade{ std::stof(std::string(trade["price"])), std::stof(std::string(trade["amount"])), side });
        }

        return trades;
    }

    unsigned long timestamp;
    unsigned long with_timestamp;

  private:
    std::string base_url;
    std::string query;
    unsigned long since_tid;
    unsigned long limit_trades;
};

}// namespace intproj