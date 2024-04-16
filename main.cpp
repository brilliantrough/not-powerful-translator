#include <QApplication>
#include <QPushButton>
#include <QResource>
#include "mainwindow.h"

class MainWindow;

int main(int argc, char *argv[]) {
//    system("chcp 65001");
    QApplication a(argc, argv);
	MainWindow w;
	w.show();
	return QApplication::exec();
}
