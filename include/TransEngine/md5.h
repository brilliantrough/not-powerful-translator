//
// Created by pzy123 on 4/16/2024.
//

#ifndef NOT_POWERFUL_TRANSLATOR_MD5_H
#define NOT_POWERFUL_TRANSLATOR_MD5_H
#include <windows.h>
#include <Wincrypt.h>
#include <iostream>
#include <vector>
#define MD5LEN 16

std::string bytesToHexString(const BYTE* bytes, DWORD length);
std::string computeMD5(const std::string& input);
#endif //NOT_POWERFUL_TRANSLATOR_MD5_H
