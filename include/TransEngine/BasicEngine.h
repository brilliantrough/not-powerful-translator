//
// Created by pzy123 on 1/7/2024.
//

#ifndef NOT_POWERFUL_TRANSLATOR_BASICENGINE_H
#define NOT_POWERFUL_TRANSLATOR_BASICENGINE_H
#include "cpr/cpr.h"
#include <fstream>
#include "nlohmann/json.hpp"
#include <iostream>
#include <chrono>
#include <map>
#include <tuple>
#include "Settings.h"
using json = nlohmann::json;


class BasicEngine {
protected:
	std::string url;
	int retry_nums;
public:
	BasicEngine();

    virtual ~BasicEngine() = default;

	static void setProxy(const std::string& address, int port, bool unset);

    static std::string getProxy();

	virtual std::tuple<std::string, std::string> translate(const std::string& text, const std::string& src, const std::string& dst) = 0;

    virtual void setAPI() = 0;

	std::tuple<std::string, std::string> en2zh(const std::string& text);

	std::tuple<std::string, std::string> zh2en(const std::string& text);

    static void read_settings();

    static bool first_flag;

    static bool read_flag;

    static bool proxy_flag;

    static std::string proxy_address;

    static int proxy_port;

    static cpr::Proxies proxies;
};

#endif //NOT_POWERFUL_TRANSLATOR_BASICENGINE_H
