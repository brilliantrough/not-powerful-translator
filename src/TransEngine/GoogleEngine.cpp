//
// Created by pzy123 on 1/6/2024.
//
#include "TransEngine/GoogleEngine.h"

GoogleEngine::GoogleEngine() {
	url = "https://translate.googleapis.com/translate_a/single";
}

std::tuple<std::string, std::string> GoogleEngine::translate(const std::string& text, const std::string& src, const std::string& dst) {
	auto start = std::chrono::high_resolution_clock::now();

	cpr::Parameters parameters = cpr::Parameters{{"sl", src}, {"tl", dst}, {"client", "gtx"}, {"dt", "t"}, {"q", text}};
	for (int i = 0; i < retry_nums; ++i) {
		try {
            cpr::Response response;
            if (_PROXY_FLAG)
                response = cpr::Get(cpr::Url{url}, parameters, proxies, cpr::Timeout{10000});
            else
                response = cpr::Get(cpr::Url{url}, parameters, cpr::Timeout{10000});
			if (response.status_code == 200) {
				auto json = nlohmann::json::parse(response.text);
				std::string translated_text;
				for (auto& elem : json[0]) {
					translated_text += elem[0].get<std::string>();
				}
				auto end = std::chrono::high_resolution_clock::now();
				std::chrono::duration<double> elapsed = end - start;
				std::cout << "耗时: " << elapsed.count() << " 秒" << std::endl;
				return {translated_text, "成功"};
			} else {
				std::cout << "连接失败，状态码为 " << response.status_code << std::endl;
			}
		} catch (const cpr::Error& e) {
			std::cout << "连接失败，错误信息为 " << "nothin just error" << std::endl;
		}
	}
	return {"", "失败"};
}

void GoogleEngine::setAPI() {
    // do nothing
}

GoogleEngine::~GoogleEngine() = default;
