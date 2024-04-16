//
// Created by pzy123 on 1/7/2024.
//

#ifndef NOT_POWERFUL_TRANSLATOR_GOOGLEENGINE_H
#define NOT_POWERFUL_TRANSLATOR_GOOGLEENGINE_H
#include "TransEngine/BasicEngine.h"
class GoogleEngine: public BasicEngine{
public:
	GoogleEngine();

    ~GoogleEngine() override;

public:
	std::tuple<std::string, std::string> translate(const std::string& text, const std::string& src, const std::string& dst) override;

    void setAPI() override;


};

#endif //NOT_POWERFUL_TRANSLATOR_GOOGLEENGINE_H
