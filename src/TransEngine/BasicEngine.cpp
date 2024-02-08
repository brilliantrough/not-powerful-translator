//
// Created by pzy123 on 1/7/2024.
//

#include "TransEngine/BasicEngine.h"

BasicEngine::BasicEngine(): retry_nums(3){
    read_settings();
    if (!first_flag){
        first_flag = true;
        // if data has proxy, set proxy
        if (data.contains("proxy")){
            proxy_flag = true;
            std::string s = to_string(data["proxy"]);
            s.erase(remove( s.begin(), s.end(), '\"' ),s.end());
            std::string http_proxy = "http://" + s;
            proxies = {{"http", http_proxy}, {"https", http_proxy}};
        }
    }
}

void BasicEngine::setProxy(const std::string &address, int port, bool unset) {
    if (unset) {
        std::cout << "nothing serious, just no proxy" << std::endl;
//        remove proxy from data
        data.erase("proxy");
        proxy_flag = false;
    } else {
        std::string proxy = "http://" + address + ":" + std::to_string(port);
        proxies = {{"https", proxy}, {"http", proxy}};
        proxy_flag = true;
//         add proxy to data
        data["proxy"] = address + ":" + std::to_string(port);
    }
}
std::tuple<std::string, std::string> BasicEngine::en2zh(const std::string &text) {
	return translate(text, "en", "zh-CN");
}

std::tuple<std::string, std::string> BasicEngine::zh2en(const std::string &text) {
	return translate(text, "zh-CN", "en" );
}

json BasicEngine::data = {};
bool BasicEngine::first_flag = false;
bool BasicEngine::read_flag = false;
bool BasicEngine::proxy_flag = false;
cpr::Proxies BasicEngine::proxies = {{"http", ""}, {"https", ""}};

void BasicEngine::read_settings() {
    if (read_flag)
        return;
    std::ifstream f("engine_settings.json");
    f >> data;
    read_flag = true;
}

std::string BasicEngine::getProxy() {
    if (proxy_flag)
        return to_string(data["proxy"]);
    else
        return "no proxy";
}

