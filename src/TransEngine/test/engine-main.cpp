//
// Created by pzy123 on 1/8/2024.
//
#include "OpenAIEngine.h"
#include "GoogleEngine.h"
#include <memory>
#include <iostream>
int main(int args, char** argv){
    system("chcp 65001");
    std::unique_ptr<BasicEngine> translator = std::make_unique<GoogleEngine>();
//    translator->setProxy("127.0.0.1", 7890, false);
    auto result = translator->en2zh("hello world");
    std::cout << std::get<1>(result) << " " << std::get<0>(result) << std::endl;
    result = translator->zh2en("你好世界");
    std::cout << std::get<1>(result) << " " << std::get<0>(result) << std::endl;
    return 0;
}

