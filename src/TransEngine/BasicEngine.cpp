//
// Created by pzy123 on 1/7/2024.
//

#include "TransEngine/BasicEngine.h"

BasicEngine::BasicEngine(): retry_nums(3){
    read_settings();
    if (first_flag){
        first_flag = false;
        // if Settings::data has proxy, set proxy
        if (_PROXY_FLAG){
            proxy_flag = true;
            proxy_address = _PROXY_ADDRESS;
            proxy_port = _PROXY_PORT;
            std::string http_proxy = "http://" + _PROXY_ADDRESS + ":" + std::to_string(_PROXY_PORT);
            proxies = {{"http", http_proxy}, {"https", http_proxy}};
        }
    }
}

void BasicEngine::setProxy(const std::string &address, int port, bool unset) {
    SET_PROXY_FLAG(!unset);
    proxy_flag = !unset;
    if (unset) {
        std::cout << "nothing serious, just no proxy" << std::endl;
        proxy_address = "";
        proxy_port = 0;
    } else {
        std::string proxy = "http://" + address + ":" + std::to_string(port);
        proxy_address = address;
        proxy_port = port;
        proxies = {{"https", proxy}, {"http", proxy}};
    }
}
std::tuple<std::string, std::string> BasicEngine::en2zh(const std::string &text) {
	return translate(text, "en", "zh");
}

std::tuple<std::string, std::string> BasicEngine::zh2en(const std::string &text) {
	return translate(text, "zh", "en" );
}

bool BasicEngine::first_flag = true;
bool BasicEngine::read_flag = false;
bool BasicEngine::proxy_flag = false;
std::string BasicEngine::proxy_address = "";
int BasicEngine::proxy_port = 0;
cpr::Proxies BasicEngine::proxies = {{"http", ""}, {"https", ""}};

void BasicEngine::read_settings() {
    if (read_flag && !_FIRST_FLAG)
        return;
    READ_SETTINGS();
    read_flag = true;
}

std::string BasicEngine::getProxy() {
    if (proxy_flag)
        return proxy_address + ":" + std::to_string(proxy_port);
    else
        return "no proxy";
}

