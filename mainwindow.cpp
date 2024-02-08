//
// Created by pzy123 on 1/6/2024.
//

// You may need to build the project (run Qt uic code generator) to get "ui_Mainwindow.h" resolved 你好

#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QString>
#include <QDebug>
#include <QIcon>

MainWindow::MainWindow(QWidget *parent) :
		QMainWindow(parent), ui(new Ui::MainWindow) {
	ui->setupUi(this);
    initVariable();
    initSignalSlot();
    initEvent();
    initWindows();
    initTest();
}

MainWindow::~MainWindow() {
    delete child_worker;
	delete ui;
    // load BasicEngine::data to engine_settings.json
    std::ofstream f("engine_settings.json");
    f << BasicEngine::data;
    worker_thread->terminate();
}

void MainWindow::on_exitBtn_clicked() {
    delete mouse_listener;
	this->close();
}

bool MainWindow::eventFilter(QObject *obj, QEvent *event) {
	// Check if the event is a key press event
	if (event->type() == QEvent::KeyPress) {
		auto *keyEvent = dynamic_cast<QKeyEvent *>(event);

		// Handling Shift+Enter for newline insertion
		if (keyEvent->key() == Qt::Key_Return && keyEvent->modifiers() == Qt::ShiftModifier) {
			if (obj == ui->inputZH || obj == ui->inputEN) {
				auto *textEdit = qobject_cast<QTextEdit *>(obj);
				if (textEdit) {
					textEdit->insertPlainText("\n");
				}
				return true;
			}
		}
			// Handling Enter for triggering translation
		else if (keyEvent->key() == Qt::Key_Return) {
			if (obj == ui->inputZH) {
				zh2enTranslate();
				this->clearFocus();
				return true;
			} else if (obj == ui->inputEN) {
				en2zhTranslate();
				this->clearFocus();
				return true;
			}
		}
	}
	// Pass the event on to the parent class
	return QMainWindow::eventFilter(obj, event);
}

void MainWindow::en2zhTranslate() {
    ui->statusEN->setText("等待...");
    ui->outputZH->clear();
    emit en2zh_signal(ui->inputEN->toPlainText());
}

void MainWindow::zh2enTranslate() {
    ui->statusZH->setText("等待...");
    ui->outputEN->clear();
    emit zh2en_signal(ui->inputZH->toPlainText());
}

void MainWindow::recv_from_mouse_listener() {
    auto text = QString(mouse_listener->current_selected_text.c_str());
    ui->inputEN->setPlainText(text);
    ui->statusEN->setText("等待...");
    emit en2zh_signal(text);
}

void MainWindow::selectionCheckBox_changed() {
    if (ui->selectionCheckBox->isChecked()){
        mouse_listener->setIfMouseSelect(true);
    }else {
        mouse_listener->setIfMouseSelect(false);
    }
}

void MainWindow::on_copyZHBtn_clicked() {
    clipboard->setText(ui->outputZH->toPlainText());
}

void MainWindow::onTopCheckBox_changed() {
    if (ui->onTopCheckBox->isChecked()){
        this->setWindowFlags(Qt::WindowStaysOnTopHint);
        this->show();
    } else {
        this->setWindowFlags(Qt::Widget);
        this->show();
    }
}

void MainWindow::display_status_result(const QString& output, const QString& status, bool flag) {
    if (flag){
        ui->statusEN->setText(status);
        setCursorFormat(cursorZH);
        cursorZH->insertText(output);
//        ui->outputZH->setPlainText(output);
    } else {
        ui->statusZH->setText(status);
        setCursorFormat(cursorEN);
        cursorEN->insertText(output);
//        ui->outputEN->setPlainText(output);
        if (ui->actionAuto_Copy_EN->isChecked()){
            clipboard->setText(output);
        }
    }
}

void MainWindow::initTest() {
    ui->inputZH->setPlainText("请在这里输入中文");
    ui->inputEN->setPlainText("请在这里输入英文");
    ui->outputEN->setText("这里会输出英文");
    ui->outputZH->setText("这里会输出中文");
}

void MainWindow::initVariable() {
    google_engine = std::make_shared<GoogleEngine>();
    openai_engine = std::make_shared<OpenAIEngine>();
    engine = std::static_pointer_cast<BasicEngine>(google_engine);
    cursorEN = new QTextCursor(ui->outputEN->textCursor());
    cursorZH = new QTextCursor(ui->outputZH->textCursor());
    mouse_listener = new MouseSelection();
    clipboard = QGuiApplication::clipboard();
    worker_thread = new QThread();
    child_worker = new ChildWorker(this);
    child_worker->moveToThread(worker_thread);
    worker_thread->start();
}

void MainWindow::initSignalSlot() {
    QObject::connect(mouse_listener, &MouseSelection::passSelectedText, this, &MainWindow::recv_from_mouse_listener);
    QObject::connect(ui->selectionCheckBox, &QCheckBox::stateChanged, this, &MainWindow::selectionCheckBox_changed);
    QObject::connect(ui->onTopCheckBox, &QCheckBox::stateChanged, this, &MainWindow::onTopCheckBox_changed);
    QObject::connect(ui->modeBox, QOverload<int>::of(&QComboBox::currentIndexChanged), this, &MainWindow::modeBox_changed);
    QObject::connect(ui->engineBox, QOverload<int>::of(&QComboBox::currentIndexChanged), this, &MainWindow::engineBox_changed);
    QObject::connect(this, &MainWindow::en2zh_signal, child_worker, &ChildWorker::en2zh_slot);
    QObject::connect(this, &MainWindow::zh2en_signal, child_worker, &ChildWorker::zh2en_slot);
    QObject::connect(child_worker, &ChildWorker::work_done, this, &MainWindow::display_status_result);
    QObject::connect(ui->actionCheck_Proxy, &QAction::triggered, this, &MainWindow::check_proxy);
    QObject::connect(ui->actionProxy, &QAction::triggered, this, &MainWindow::set_proxy);
}

void MainWindow::initEvent() {
    ui->outputEN->hide();
    ui->inputZH->hide();
    ui->inputZH->installEventFilter(this);
    ui->inputEN->installEventFilter(this);
}

void MainWindow::initWindows() {
    setWindowTitle("不太全能的翻译");
    setWindowIcon(QIcon(":/IDI_ICON1"));
    resize(900, 400);
}

void MainWindow::modeBox_changed(int index) {
    switch (index) {
        case 0:
            ui->inputEN->show();
            ui->outputZH->show();
            ui->inputZH->hide();
            ui->outputEN->hide();
            break;
        case 1:
            ui->inputEN->hide();
            ui->outputZH->hide();
            ui->inputZH->show();
            ui->outputEN->show();
            break;
        default:
            ui->inputEN->show();
            ui->outputZH->show();
            ui->inputZH->show();
            ui->outputEN->show();
            break;
    }
}

void MainWindow::engineBox_changed(int index) {
    switch (index) {
        case 0:
            engine = std::static_pointer_cast<BasicEngine>(google_engine);
            break;
        case 1:
            engine = std::static_pointer_cast<BasicEngine>(openai_engine);
            break;
        default:
            engine = std::static_pointer_cast<BasicEngine>(google_engine);
            break;
    }
}

void MainWindow::setCursorFormat(QTextCursor *cursor) {
    cursor->movePosition(QTextCursor::Start);
    auto block_format = QTextBlockFormat();
    block_format.setLineHeight(150, QTextBlockFormat::ProportionalHeight);
    cursor->setBlockFormat(block_format);
}

void MainWindow::check_proxy() {
    std::string proxy = BasicEngine::getProxy();
    // using QMessageBox to show the proxy
    QMessageBox::information(this, "Proxy", QString(proxy.c_str()));
}

void MainWindow::set_proxy() {
    // using QDialog to set the proxy
    QDialog dialog(this);
    dialog.setWindowTitle("设置代理");
    dialog.resize(200, 200);
    auto *layout = new QVBoxLayout(&dialog);
    auto *proxyEdit = new QLineEdit(&dialog);
    auto *portEdit = new QLineEdit(&dialog);
    auto *proxyLabel = new QLabel("代理地址", &dialog);
    auto *portLabel = new QLabel("端口", &dialog);
    auto *button = new QPushButton("确定", &dialog);
    layout->addWidget(proxyLabel);
    layout->addWidget(proxyEdit);
    layout->addWidget(portLabel);
    layout->addWidget(portEdit);
    layout->addWidget(button);
    QObject::connect(button, &QPushButton::clicked, [&](){
        std::string proxy = proxyEdit->text().toStdString();
        int port = portEdit->text().toInt();
        BasicEngine::setProxy(proxy, port, false);
        dialog.close();
    });
    dialog.show();
    dialog.exec();
}

ChildWorker::ChildWorker(MainWindow *parent) {
    this->parent = parent;
}

ChildWorker::~ChildWorker() {
    parent = NULL;
}

void ChildWorker::zh2en_slot(const QString& text) {
    auto result = parent->engine->zh2en(text.toStdString());
    auto output = QString(std::get<0>(result).c_str());
    emit work_done(output, QString(std::get<1>(result).c_str()), false);
}

void ChildWorker::en2zh_slot(const QString& text) {
    auto result = parent->engine->en2zh(text.toStdString());
    auto output = QString(std::get<0>(result).c_str());
    emit work_done(output, QString(std::get<1>(result).c_str()), true);
}
