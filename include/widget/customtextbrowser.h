//
// Created by pzy123 on 4/14/2024.
//

#ifndef NOT_POWERFUL_TRANSLATOR_CUSTOMTEXTBROWSER_H
#define NOT_POWERFUL_TRANSLATOR_CUSTOMTEXTBROWSER_H
#include <QTextBrowser>
#include <QPushButton>
#include <QScrollBar>

class CustomTextBrowser : public QTextBrowser {
Q_OBJECT
public:
    explicit CustomTextBrowser(QWidget *parent = nullptr);

protected:
    void enterEvent(QEvent *event) override;
    void leaveEvent(QEvent *event) override;
    void resizeEvent(QResizeEvent *event) override;
    void adjustCopyButtonPosition();

private slots:
    void copyText();

private:
    QPushButton *copyButton;
};

#endif //NOT_POWERFUL_TRANSLATOR_CUSTOMTEXTBROWSER_H
