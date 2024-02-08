//
// Created by pzy123 on 2/1/2024.
//

#ifndef NOT_POWERFUL_TRANSLATOR_OPENAIENGINE_H
#define NOT_POWERFUL_TRANSLATOR_OPENAIENGINE_H
#include "TransEngine/BasicEngine.h"
class OpenAIEngine: public BasicEngine{
public:
    OpenAIEngine();

    ~OpenAIEngine() override;

    std::string key;

public:
    std::tuple<std::string, std::string> translate(const std::string& text, const std::string& src, const std::string& dst) override;


};

#endif //NOT_POWERFUL_TRANSLATOR_OPENAIENGINE_H
