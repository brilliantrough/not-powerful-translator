//
// Created by pzy123 on 2/12/2024.
//

#include "ScreenShot.h"

ScreenAPI::ScreenAPI(QSize size)
{
    maxWidth = size.width();//获得整个屏幕的大小
    maxHeight = size.height();

    startPos = QPoint(-1, -1);//开始坐标
    endPos = startPos;//结束坐标
    leftUpPos = startPos;//左上角坐标
    rightDownPos = startPos;//右下角坐标
    status = SELECT;
}

//显示窗口Widget发出事件被调用
void frmScreen::showEvent(QShowEvent *)
{
    QPoint point(-1, -1);
    screen->setStart(point);//设置开启坐标点
    screen->setEnd(point);//设置结束坐标点

    //全屏图像，抓取窗体
    *fullScreen = QPixmap::grabWindow(QApplication::desktop()->winId(), 0, 0, screen->width(), screen->height());

    //设置透明度实现模糊背景
    QPixmap pix(screen->width(), screen->height());
    pix.fill((QColor(160, 160, 160, 200)));//模糊颜色填充
    bgScreen = new QPixmap(*fullScreen);
    QPainter p(bgScreen);
    p.drawPixmap(0, 0, pix);
}

//重绘事件  update调用
void frmScreen::paintEvent(QPaintEvent *)
{
    int x = screen->getLeftUp().x();
    int y = screen->getLeftUp().y();
    int w = screen->getRightDown().x() - x;//宽度
    int h = screen->getRightDown().y() - y;//高度

    QPainter painter(this);

    QPen pen;
    pen.setColor(Qt::green);
    pen.setWidth(2);
    pen.setStyle(Qt::DotLine);//虚线样式
    painter.setPen(pen);

    QFont font;
    font.setFamily("Microsoft YaHei");
    font.setPointSize(10);
    painter.setFont(font);

    //截屏思想：点击截屏工具的时候，截取全屏的像素，并且将全屏保存到一个全局的变量pixmap中。
    //然后，在点击鼠标移动，截取一个相应的矩形。将其绘制出来。
    painter.drawPixmap(0, 0, *bgScreen);//

    if (w != 0 && h != 0) {
        painter.drawPixmap(x, y, fullScreen->copy(x, y, w, h));//绘制选择截屏的区域
    }

    painter.drawRect(x, y, w, h);//绘制截图矩形

    pen.setColor(Qt::yellow);
    painter.setPen(pen);
    painter.drawText(x + 2, y - 8, tr("截图范围：( %1 x %2 ) - ( %3 x %4 )  图片大小：( %5 x %6 )")
            .arg(x).arg(y).arg(x + w).arg(y + h).arg(w).arg(h));
}

//鼠标按下事件
void frmScreen::mousePressEvent(QMouseEvent *e)
{
    int status = screen->getStatus();//获取状态

    if (status == ScreenAPI::SELECT) {
        screen->setStart(e->pos());
    } else if (status == ScreenAPI::MOV) {
        if (screen->isInArea(e->pos()) == false) {
            screen->setStart(e->pos());
            screen->setStatus(ScreenAPI::SELECT);
        } else {
            movPos = e->pos();
            this->setCursor(Qt::SizeAllCursor);
        }
    }

    update();
}
//鼠标移动事件
void frmScreen::mouseMoveEvent(QMouseEvent *e)
{
    if (screen->getStatus() == ScreenAPI::SELECT) {//选择区域
        screen->setEnd(e->pos());//得到结束点坐标
    } else if (screen->getStatus() == ScreenAPI::MOV) {//移动区域
        QPoint p(e->x() - movPos.x(), e->y() - movPos.y());
        screen->move(p);
        movPos = e->pos();
    }

    update();
}
//鼠标释放事件
void frmScreen::mouseReleaseEvent(QMouseEvent *)
{
    if (screen->getStatus() == ScreenAPI::SELECT) {
        screen->setStatus(ScreenAPI::MOV);
    } else if (screen->getStatus() == ScreenAPI::MOV) {
        this->setCursor(Qt::ArrowCursor);
    }
}

frmAPI::frmAPI(){
    QPushButton *btnScreenAPI = new QPushButton(this);

}

frmAPI::~frmAPI() = default;

void frmAPI::on_btnScreenAPI_clicked()
{
    frmScreen::Instance()->showFullScreen();//显示全屏widget
}