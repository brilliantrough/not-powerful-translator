//
// Created by pzy123 on 4/15/2024.
//
#include "customtextbrowser.h"

CustomTextBrowser::CustomTextBrowser(QWidget *parent) : QTextBrowser(parent) {
    setStyleSheet("QScrollBar:vertical { width: 15px; }");
    copyButton = new QPushButton(this);
    copyButton->setStyleSheet("QPushButton {"
                              "image: url(:/copy);"
                              "}"
                              "QPushButton:hover {"
                              "background-color: rgb(115,210,22);"
                              "}");
    copyButton->setFixedSize(QSize(25, 25));
    connect(copyButton, &QPushButton::clicked, this, &CustomTextBrowser::copyText);
    copyButton->hide(); // Initially hide the button
//    setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
}

void CustomTextBrowser::adjustCopyButtonPosition() {
    int margin = 5; // Margin from the edge
    int buttonXPosition;

    QScrollBar *vScrollBar = this->verticalScrollBar();
    if (vScrollBar->isVisible()) {
        // If the vertical scroll bar is visible, position the button taking into account the scroll bar's width
        buttonXPosition = this->width() - copyButton->width() - vScrollBar->width() - margin;
    } else {
        // If the vertical scroll bar is not visible, position the button at the edge
        buttonXPosition = this->width() - copyButton->width() - margin;
    }

    // Adjust the button's position. Assuming the button's Y position is fixed or determined elsewhere
    copyButton->move(buttonXPosition, copyButton->y());
}
void CustomTextBrowser::enterEvent(QEvent *event) {
    QTextBrowser::enterEvent(event);
    adjustCopyButtonPosition();
    copyButton->show();
}

void CustomTextBrowser::leaveEvent(QEvent *event) {
    QTextBrowser::leaveEvent(event);
    copyButton->hide();
}

void CustomTextBrowser::resizeEvent(QResizeEvent *event) {
    QTextBrowser::resizeEvent(event);
    adjustCopyButtonPosition();
}

void CustomTextBrowser::copyText() {
    selectAll();
    copy();
    moveCursor(QTextCursor::End);
}
