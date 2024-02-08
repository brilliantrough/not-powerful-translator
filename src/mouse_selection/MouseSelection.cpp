//
// Created by pzy123 on 1/8/2024.
//

#include "mouse_selection/MouseSelection.h"
#include "mouse_selection/EncodeConvert.h"

MouseSelection::MouseSelection(QObject *parent) : QObject(parent) {
    a = 5;
    b = 10;
    num_of_selected_text = 0;
    if_mouse_select = true;
    last_selected_text = "";
    first_text_in_clipboard = GetClipboardText();
    end_flag = false;
    mouse_hook_thread = new std::thread(&MouseSelection::mouseHookThreadFunc, this);
}

MouseSelection::~MouseSelection() {
    end_flag = true;
    mouse_hook_thread->join();
}

void MouseSelection::test() {
    std::cout << "hello world this is in the mouse selector" << std::endl;
}

void MouseSelection::CheckMouseClick(){
    if((GetKeyState(VK_LBUTTON) & 0x8000) != 0) {
        std::cout << "left button is pressed" << std::endl;
    }
    else {
        std::cout << "left button is not pressed" << std::endl;
    }
}

void MouseSelection::SendCtrlIns() {
    if (!if_mouse_select)
        return;
    INPUT inputs[4] = {};
    // Set up inputs for Ctrl+ins
    // Press Ctrl
    inputs[0].type = INPUT_KEYBOARD;
    inputs[0].ki.wVk = VK_CONTROL;
    // Press insert
    inputs[1].type = INPUT_KEYBOARD;
    inputs[1].ki.wVk = VK_INSERT;
    // Release insert
    inputs[2] = inputs[1];
    inputs[2].ki.dwFlags = KEYEVENTF_KEYUP;
    // Release Ctrl
    inputs[3] = inputs[0];
    inputs[3].ki.dwFlags = KEYEVENTF_KEYUP;

    SendInput(ARRAYSIZE(inputs), inputs, sizeof(INPUT));
}

std::string MouseSelection::GetClipboardText() {
    if (!OpenClipboard(nullptr)) return "";
    HANDLE hData = GetClipboardData(CF_TEXT);
    if (hData == nullptr) return "";
    const char* pszText = static_cast<char*>(GlobalLock(hData));
    if (pszText == nullptr) return "";
    std::string utf8Text = gbk2utf8(pszText);
    GlobalUnlock(hData);
    CloseClipboard();
    return utf8Text;
}

void MouseSelection::mouseHookThreadFunc() {
    bool lFlagMouseDown = false;
    // listen the mouse, if it is clicked, then send ctrl+c to copy the text
    while (true) {
        if (end_flag) {
            std::cout << "the thread is going to end" << std::endl;
            break;
        }
        if((GetKeyState(VK_LBUTTON) & 0x8000) != 0) {
            if (!lFlagMouseDown)
            lFlagMouseDown = true;
        }
        else if (lFlagMouseDown) {
            SendCtrlIns();
            Sleep(100);
            if (!if_mouse_select)
                continue;
            current_selected_text = GetClipboardText();
            if (checkIfClipboardChanged()){
//                std::cout << "copied text: " << current_selected_text << std::endl;
                emit passSelectedText();
            }
            lFlagMouseDown = false;
        }
        Sleep(400);
    }
    std::cout << "the thread done" << std::endl;

}

bool MouseSelection::checkIfClipboardChanged() {
    if (num_of_selected_text == 0 && current_selected_text == first_text_in_clipboard) {
        return false;
    }
    if (current_selected_text == "") {
        return false;
    }
    if (current_selected_text != last_selected_text) {
        last_selected_text = current_selected_text;
        num_of_selected_text++;
        return true;
    } else {
        return false;
    }
}

void MouseSelection::setIfMouseSelect(bool if_mouse_select) {
    this->if_mouse_select = if_mouse_select;
}

