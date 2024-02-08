//
// Created by pzy123 on 1/8/2024.
//

#include "mouse_selection/EncodeConvert.h"
#include <Windows.h>
#include <string>
#include <iostream>
#include <memory>

std::string gbk2utf8(const char* gbkStr) {
    // Convert GBK to UTF-16
    int len = MultiByteToWideChar(936, 0, gbkStr, -1, NULL, 0);
    if (len == 0) {
        throw std::runtime_error("Failed to convert GBK to UTF-16");
    }

    auto wstr = std::make_unique<wchar_t[]>(len);
    if (MultiByteToWideChar(936, 0, gbkStr, -1, wstr.get(), len) == 0) {
        throw std::runtime_error("Failed to convert GBK to UTF-16");
    }

    // Convert UTF-16 to UTF-8
    int utf8Len = WideCharToMultiByte(CP_UTF8, 0, wstr.get(), -1, NULL, 0, NULL, NULL);
    if (utf8Len == 0) {
        throw std::runtime_error("Failed to convert UTF-16 to UTF-8");
    }

    auto utf8Str = std::make_unique<char[]>(utf8Len);
    if (WideCharToMultiByte(CP_UTF8, 0, wstr.get(), -1, utf8Str.get(), utf8Len, NULL, NULL) == 0) {
        throw std::runtime_error("Failed to convert UTF-16 to UTF-8");
    }
    return std::string(utf8Str.get());
}
