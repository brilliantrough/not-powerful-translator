//
// Created by pzy123 on 2/12/2024.
//

#ifndef NOT_POWERFUL_TRANSLATOR_SCREENSHOT_H
#define NOT_POWERFUL_TRANSLATOR_SCREENSHOT_H
#include <QWidget>

class frmScreen : QWidget {
Q_OBJECT
public:
    explicit frmScreen(QWidget *parent = 0);
    ~frmScreen();

};

class ScreenAPI
{
public:
    enum STATUS {SELECT, MOV, SET_W_H};
    ScreenAPI() {}
    ScreenAPI(QSize size);

    void setStart(QPoint pos);//设置开启坐标
    void setEnd(QPoint pos);//设置结束坐标
    QPoint getStart()   ;
    QPoint getEnd();

    QPoint getLeftUp();
    QPoint getRightDown();

    STATUS getStatus();
    void setStatus(STATUS status);

    int width();
    int height();
    bool isInArea(QPoint pos);          // 检测pos是否在截图区域内
    void move(QPoint p);                // 按 p 移动截图区域

private:
    QPoint leftUpPos, rightDownPos;     //记录 截图区域 左上角、右下角
    QPoint startPos, endPos;            //记录 鼠标开始位置、结束位置
    int maxWidth, maxHeight;            //记录屏幕大小
    STATUS status;                      //三个状态: 选择区域、移动区域、设置width height

    void cmpPoint(QPoint &s, QPoint &e);//比较两位置，判断左上角、右下角
};

class frmAPI : public QWidget {
Q_OBJECT
    explicit frmAPI(QWidget *parent = 0);
    ~frmAPI();
    void on_btnScreenAPI_clicked();
#endif //NOT_POWERFUL_TRANSLATOR_SCREENSHOT_H
};