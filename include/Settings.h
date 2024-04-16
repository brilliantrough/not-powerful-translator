//
// Created by pzy123 on 4/14/2024.
//

#ifndef NOT_POWERFUL_TRANSLATOR_SETTINGS_H
#define NOT_POWERFUL_TRANSLATOR_SETTINGS_H
#include <fstream>
#include <iostream>
#include <filesystem>
#include "nlohmann/json.hpp"
#define SET_PROXY_FLAG(x) Settings::PROXY_FLAG = x;
#define SET_PROXY_ADDRESS(x) Settings::PROXY_ADDRESS = x;
#define SET_PROXY_PORT(x) Settings::PROXY_PORT = x;
#define SET_OPENAI_API_BASE(x) Settings::OPENAI_API_BASE = x;
#define SET_OPENAI_API_KEY(x) Settings::OPENAI_API_KEY = x;
#define SET_BAIDU_APPID(x) Settings::BAIDU_APPID = x;
#define SET_BAIDU_KEY(x) Settings::BAIDU_KEY = x;
#define SET_ON_TOP_FLAG(x) Settings::ON_TOP_FLAG = x;
#define SET_MINIMAL_FLAG(x) Settings::MINIMAL_FLAG = x;
#define SET_SIZE(x, y) Settings::SIZE = {x, y};
#define SET_PREFFERED_ENGINE(x) Settings::PREFFERED_ENGINE = x;
#define SET_HIDE_INPUT_FLAG(x) Settings::HIDE_INPUT_FLAG = x;

#define _PROXY_FLAG Settings::PROXY_FLAG
#define _PROXY_ADDRESS Settings::PROXY_ADDRESS
#define _PROXY_PORT Settings::PROXY_PORT
#define _OPENAI_API_BASE Settings::OPENAI_API_BASE
#define _OPENAI_API_KEY Settings::OPENAI_API_KEY
#define _BAIDU_APPID Settings::BAIDU_APPID
#define _BAIDU_KEY Settings::BAIDU_KEY
#define _ON_TOP_FLAG Settings::ON_TOP_FLAG
#define _MINIMAL_FLAG Settings::MINIMAL_FLAG
#define _SIZE_WIDTH Settings::SIZE.first
#define _SIZE_HEIGHT Settings::SIZE.second
#define _PREFFERED_ENGINE Settings::PREFFERED_ENGINE
#define _HIDE_INPUT_FLAG Settings::HIDE_INPUT_FLAG
#define _FIRST_FLAG Settings::first_flag

#define READ_SETTINGS Settings::read_settings
#define WRITE_SETTINGS Settings::write_settings
#define CHECK_OPENAI_API Settings::check_openai_api
#define CHECK_BAIDU_API Settings::check_baidu_api



namespace fs = std::filesystem;
using json = nlohmann::json;

class Settings { ;

public:
    static json data;

    static std::string PROXY_ADDRESS;
    static int PROXY_PORT;
    static std::string OPENAI_API_BASE;
    static std::string OPENAI_API_KEY;
    static std::string BAIDU_APPID;
    static std::string BAIDU_KEY;
    static bool first_flag;
    static bool PROXY_FLAG;
    static bool ON_TOP_FLAG;
    static bool MINIMAL_FLAG;
    static std::pair<int, int> SIZE;
    static std::string PREFFERED_ENGINE;
    static bool HIDE_INPUT_FLAG;
    static std::string SETTINGS_FILE;

    Settings() {}

    static void read_settings();

    static void write_settings();

    static bool check_openai_api();

    static bool check_baidu_api();

    ~Settings() {}
};


#endif //NOT_POWERFUL_TRANSLATOR_SETTINGS_H
