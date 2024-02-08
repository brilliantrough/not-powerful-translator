//
// Created by pzy123 on 1/8/2024.
//

#ifndef NOT_POWERFUL_TRANSLATOR_MOUSESELECTION_H
#define NOT_POWERFUL_TRANSLATOR_MOUSESELECTION_H
#include <Windows.h>
#include <thread>
#include <chrono>
#include <iostream>
#include <QObject>

class MouseSelection : public QObject {
Q_OBJECT
public:
    int a;
    int b;

    int num_of_selected_text;

    bool if_mouse_select;

    bool end_flag;

    std::string last_selected_text;

    std::string current_selected_text;

    std::string first_text_in_clipboard;

    std::thread* mouse_hook_thread;

    QString text;

signals:
    void passSelectedText();


public:
    explicit MouseSelection(QObject *parent = nullptr);

    ~MouseSelection();

    void test();

    void CheckMouseClick();

    void SendCtrlIns();

    std::string GetClipboardText();

    void mouseHookThreadFunc();

    bool checkIfClipboardChanged();

    void setIfMouseSelect(bool if_mouse_select);

};


#endif //NOT_POWERFUL_TRANSLATOR_MOUSESELECTION_H
