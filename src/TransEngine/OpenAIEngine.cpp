//
// Created by pzy123 on 2/1/2024.
//
#include "TransEngine/OpenAIEngine.h"

std::string prompt_en2zh = "You should act as a Chinese translator, spelling corrector and improver. The user will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in Chinese. You should only reply the correction, the improvements and nothing else, do not write explanations. Your goal is to ensure that the translation is as smooth and natural as possible, while not changing the meaning of the text.";
std::string prompt_zh2en = "You should act as an English translator, spelling corrector and improver. The user will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. You should only reply the correction, the improvements and nothing else, do not write explanations. Your goal is to ensure that the translation is as smooth and natural as possible, while not changing the meaning of the text.";
OpenAIEngine::OpenAIEngine() {
    url = std::string(std::getenv("OPENAI_API_BASE")) + "/chat/completions";
    key = std::string(std::getenv("OPENAI_API_KEY"));
}


std::tuple<std::string, std::string> OpenAIEngine::translate(const std::string& text, const std::string& src, const std::string& dst) {
    auto start = std::chrono::high_resolution_clock::now();
    std::string prompt;
    if (src=="en") {
        prompt = prompt_en2zh;
    } else {
        prompt = prompt_zh2en;
    }
    nlohmann::json data = {
            {"model", "gpt-3.5-turbo"},
            {"messages", {
                              {{"role", "system"}, {"content", prompt}},
                              {{"role", "user"}, {"content", text}}
                      }}
    };
    std::string json_data = data.dump();

    for (int i = 0; i < retry_nums; ++i) {
        try {
            cpr::Response response;
            if (proxy_flag)
                response = cpr::Post(cpr::Url{url}, cpr::Body{json_data}, proxies, cpr::Timeout{10000}, cpr::Header{{"Content-Type", "application/json"}, {"Authorization", "Bearer " + key}});
            else
                response = cpr::Post(cpr::Url{url}, cpr::Body{json_data}, cpr::Timeout{10000}, cpr::Header{{"Content-Type", "application/json"}, {"Authorization", "Bearer " + key}});
            if (response.status_code == 200) {
                auto parsed_response = nlohmann::json::parse(response.text);
                std::string translated_text = parsed_response["choices"][0]["message"]["content"].get<std::string>();
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

OpenAIEngine::~OpenAIEngine() = default;
