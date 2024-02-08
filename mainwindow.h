//
// Created by pzy123 on 1/6/2024.
//

#ifndef NOT_POWERFUL_TRANSLATOR_MAINWINDOW_H
#define NOT_POWERFUL_TRANSLATOR_MAINWINDOW_H

#include <QMainWindow>
#include <QClipboard>
#include <QThread>
#include <memory>
#include <QTextCursor>
#include <QMessageBox>
#include <QLabel>
#include "TransEngine/GoogleEngine.h"
#include "TransEngine/OpenAIEngine.h"
#include "mouse_selection/MouseSelection.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE
class OpenAIEngine;
class GoogleEngine;
class BasicEngine;
class MouseSelection;
class ChildWorker;

class  MainWindow : public QMainWindow {
    friend class ChildWorker;
Q_OBJECT
public:
	std::shared_ptr<BasicEngine> engine;

	std::shared_ptr<GoogleEngine> google_engine;

    std::shared_ptr<OpenAIEngine> openai_engine;

    MouseSelection *mouse_listener;

	void en2zhTranslate();

	void zh2enTranslate();

    QClipboard *clipboard;

    QThread *worker_thread;

    ChildWorker* child_worker;

    QTextCursor *cursorZH;

    QTextCursor *cursorEN;

public:
	explicit MainWindow(QWidget *parent = nullptr);

	~MainWindow() override;

	bool eventFilter(QObject *obj, QEvent *event) override;

signals:
    void zh2en_signal(QString text);

    void en2zh_signal(QString text);

public slots:
    void display_status_result(const QString& output, const QString& status, bool flag);

private slots:
	void on_exitBtn_clicked();

    void selectionCheckBox_changed();

    void onTopCheckBox_changed();

    void recv_from_mouse_listener();

    void on_copyZHBtn_clicked();

    void modeBox_changed(int index);

    void engineBox_changed(int index);

    void check_proxy();

    void set_proxy();


private:
	Ui::MainWindow *ui;

private:
    void initTest();

    void initVariable();

    void initSignalSlot();

    void initEvent();

    void initWindows();

    void setCursorFormat(QTextCursor* cursor);

};

// ChildWorker class declare
class ChildWorker : public QObject {
    Q_OBJECT
public:
    MainWindow* parent;

public:
    explicit ChildWorker(MainWindow* parent);

    ~ChildWorker() override;

signals:
    void work_done(QString output, QString status, bool flag);


public slots:
    void zh2en_slot(const QString& text);

    void en2zh_slot(const QString& text);
};


#endif //NOT_POWERFUL_TRANSLATOR_MAINWINDOW_H
