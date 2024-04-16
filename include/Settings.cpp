//
// Created by pzy123 on 4/15/2024.
//
#include "Settings.h"

std::string Settings::PROXY_ADDRESS = "";
int Settings::PROXY_PORT = 0;
std::string Settings::OPENAI_API_BASE = "";
std::string Settings::OPENAI_API_KEY = "";
std::string Settings::BAIDU_APPID = "";
std::string Settings::BAIDU_KEY = "";
bool Settings::first_flag = true;
json Settings::data = {};
bool Settings::PROXY_FLAG = false;
bool Settings::ON_TOP_FLAG = false;
bool Settings::MINIMAL_FLAG = false;
std::pair<int, int> Settings::SIZE = {900, 400};
std::string Settings::PREFFERED_ENGINE = "";
bool Settings::HIDE_INPUT_FLAG = false;
std::string Settings::SETTINGS_FILE = getenv("USERPROFILE") + std::string("\\AppData\\Roaming\\not powerful translator\\settings.json");

void extract_string(std::string &s) {
    s.erase(remove(s.begin(), s.end(), '\"'), s.end());
}

void Settings::read_settings() {
    if (first_flag) {
        fs::path dirPath = fs::path(SETTINGS_FILE).parent_path();

        // Create the directories if they don't exist
        try {
            if(fs::create_directories(dirPath)) {
                std::cout << "Directories created successfully.\n";
            } else {
                std::cout << "Directories already exist or cannot be created.\n";
            }
        } catch (fs::filesystem_error& e) {
            std::cerr << "Error creating directories: " << e.what() << '\n';
            return; // Exit if failed to create directories
        }
        if (!fs::exists(SETTINGS_FILE)) {
            std::ofstream o(SETTINGS_FILE);
            o << "{\n"
                 "  \"PROXY_ADDRESS\": \"\",\n"
                 "  \"PROXY_PORT\": 0,\n"
                 "  \"OPENAI_API_BASE\": \"\",\n"
                 "  \"OPENAI_API_KEY\": \"\",\n"
                 "  \"BAIDU_APPID\": \"\",\n"
                 "  \"BAIDU_KEY\": \"\",\n"
                 "  \"SIZE\": {\"width\": 900, \"height\": 400},\n"
                 "  \"MINIMAL_FLAG\": false,\n"
                 "  \"PROXY_FLAG\": false,\n"
                 "  \"ON_TOP_FLAG\": false,\n"
                 "  \"PREFFERED_ENGINE\": \"\",\n"
                 "  \"HIDE_INPUT_FLAG\": false\n"
                 "}";
            o.close();
        }
        std::ifstream i(SETTINGS_FILE);
        i >> data;
        if (data.contains("PROXY_ADDRESS")) {
            PROXY_ADDRESS = data["PROXY_ADDRESS"];
            extract_string(PROXY_ADDRESS);
            PROXY_PORT = data["PROXY_PORT"];
        }
        if (data.contains("OPENAI_API_BASE") && data.contains("OPENAI_API_KEY")) {
            OPENAI_API_BASE = data["OPENAI_API_BASE"];
            extract_string(OPENAI_API_BASE);
            OPENAI_API_KEY = data["OPENAI_API_KEY"];
            extract_string(OPENAI_API_KEY);
        }
        if (data.contains("BAIDU_APPID") && data.contains("BAIDU_KEY")){
            BAIDU_APPID = data["BAIDU_APPID"];
            extract_string(BAIDU_APPID);
            BAIDU_KEY = data["BAIDU_KEY"];
            extract_string(BAIDU_KEY);
        }
        PROXY_FLAG = data["PROXY_FLAG"];
        ON_TOP_FLAG = data["ON_TOP_FLAG"];
        MINIMAL_FLAG = data["MINIMAL_FLAG"];
        SIZE = {data["SIZE"]["width"], data["SIZE"]["height"]};
        PREFFERED_ENGINE = data["PREFFERED_ENGINE"];
        HIDE_INPUT_FLAG = data["HIDE_INPUT_FLAG"];
        first_flag = false;
        i.close();
    }
}

void Settings::write_settings() {
    std::ofstream o(SETTINGS_FILE);
    data["PROXY_ADDRESS"] = PROXY_ADDRESS;
    data["PROXY_PORT"] = PROXY_PORT;
    data["OPENAI_API_BASE"] = OPENAI_API_BASE;
    data["OPENAI_API_KEY"] = OPENAI_API_KEY;
    data["BAIDU_APPID"] = BAIDU_APPID;
    data["BAIDU_KEY"] = BAIDU_KEY;
    data["PROXY_FLAG"] = PROXY_FLAG;
    data["ON_TOP_FLAG"] = ON_TOP_FLAG;
    data["MINIMAL_FLAG"] = MINIMAL_FLAG;
    data["SIZE"]["width"] = SIZE.first;
    data["SIZE"]["height"] = SIZE.second;
    data["PREFFERED_ENGINE"] = PREFFERED_ENGINE;
    data["HIDE_INPUT_FLAG"] = HIDE_INPUT_FLAG;
    o << data;
    o.close();
}

bool Settings::check_openai_api() {
    return !OPENAI_API_BASE.empty() && !OPENAI_API_KEY.empty();
}

bool Settings::check_baidu_api() {
    return !BAIDU_APPID.empty() && !BAIDU_KEY.empty();
}