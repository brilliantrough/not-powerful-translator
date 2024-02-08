//
// Created by pzy123 on 1/8/2024.
//
#include "MouseSelection.h"
#include <thread>

void CheckMouseClick(){
    if((GetKeyState(VK_LBUTTON) & 0x8000) != 0) {
        std::cout << "left button is pressed" << std::endl;
    }
    else {
        std::cout << "left button is not pressed" << std::endl;
    }
}

int main(int argc, char *argv[]) {
    auto *mouseSelection = new MouseSelection();
//    mouseSelection->test();
    std::cout << "waiting for the thread" << std::endl;
    Sleep(60000);
    delete mouseSelection;
    return 0;
}