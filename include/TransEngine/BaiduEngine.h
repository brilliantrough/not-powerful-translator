//
// Created by pzy123 on 4/16/2024.
//

#ifndef NOT_POWERFUL_TRANSLATOR_BAIDUENGINE_H
#define NOT_POWERFUL_TRANSLATOR_BAIDUENGINE_H
#define MD5LEN 16
#include "BasicEngine.h"
#include "md5.h"
#include <cpr/cpr.h>
#include <nlohmann/json.hpp>
#include <random>
#include <chrono>
#include <string>
#include <iostream>
#include <sstream>
#include <windows.h>
#include <wincrypt.h>
#include <string>
#include <vector>
#include <iomanip>


class BaiduEngine: public BasicEngine {
public:
    BaiduEngine();

    ~BaiduEngine() override;

    std::tuple<std::string, std::string> translate(const std::string& text, const std::string& src, const std::string& dst);

private:
    std::string appid, appkey, endpoint, path, url;

    int random_int(int min, int max);

    void setAPI() override;
};

#endif //NOT_POWERFUL_TRANSLATOR_BAIDUENGINE_H
