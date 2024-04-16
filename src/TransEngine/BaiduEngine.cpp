//
// Created by pzy123 on 4/16/2024.
//
#include "TransEngine/BaiduEngine.h"

BaiduEngine::BaiduEngine() {
    endpoint = "https://api.fanyi.baidu.com";
    path = "/api/trans/vip/translate";
    url = endpoint + path;
    setAPI();
}

void BaiduEngine::setAPI() {
    appid = _BAIDU_APPID;
    appkey = _BAIDU_KEY;
}

int BaiduEngine::random_int(int min, int max) {
    std::random_device rd;
    std::mt19937 eng(rd());
    std::uniform_int_distribution<> distr(min, max);
    return distr(eng);
}

std::tuple<std::string, std::string> BaiduEngine::translate(const std::string& text, const std::string& src, const std::string& dst) {
    auto salt = std::to_string(random_int(32768, 65536));
    auto sign = computeMD5((appid + text + salt + appkey).c_str());
    std::cout << sign << std::endl;
    cpr::Payload payload = {{"appid", appid}, {"q", text}, {"from", src}, {"to", dst}, {"salt", salt}, {"sign", sign}};

    cpr::Response r = cpr::Post(cpr::Url{url},
                                payload,
                                cpr::Header{{"Content-Type", "application/x-www-form-urlencoded"}});

    auto result_json = nlohmann::json::parse(r.text);
    std::string result_str;
    if (result_json.contains("error_code")) {
        return {result_json["error_msg"].get<std::string>(), "失败 " + std::to_string(r.status_code)};
    } else {
        for (auto& result : result_json["trans_result"]) {
            result_str += result["dst"].get<std::string>() + "\n";
        }
        return {result_str, "成功"};
    }
}

BaiduEngine::~BaiduEngine() = default;
