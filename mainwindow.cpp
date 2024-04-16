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
    initSettings();
    initWindows();
    initTest();
}

MainWindow::~MainWindow() {
    delete mouse_listener;
    delete child_worker;
	delete ui;
    worker_thread->terminate();
}

void MainWindow::closeEvent(QCloseEvent *event) {
    SET_SIZE(this->width(), this->height());
    SET_PROXY_FLAG(BasicEngine::proxy_flag);
    SET_PROXY_ADDRESS(BasicEngine::proxy_address);
    SET_PROXY_PORT(BasicEngine::proxy_port);
    // Call your custom function
    WRITE_SETTINGS();

    // Optionally, prompt the user before closing
    auto reply = QMessageBox::question(this, tr("Confirm Close"),
                                       tr("Are you sure you want to quit?"),
                                       QMessageBox::Yes | QMessageBox::No);

    if (reply == QMessageBox::Yes) {
        event->accept(); // Accept the close event
    } else {
        event->ignore(); // Ignore the close event
    }
}

void MainWindow::on_exitBtn_clicked() {
	this->close();
}

void MainWindow::on_screenShotBtn_clicked(){
    // developing
    QMessageBox::information(this, "ScreenShot", "Developing");
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
    ui->outputZH->clear();
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
    ui->outputZH->selectAll();
    ui->outputZH->copy();
    ui->outputZH->moveCursor(QTextCursor::End);
//    clipboard->setText(ui->outputZH->toPlainText());
}

void MainWindow::onTopCheckBox_changed() {
    SET_ON_TOP_FLAG(ui->onTopCheckBox->isChecked());
    if (_ON_TOP_FLAG){
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
    baidu_engine = std::make_shared<BaiduEngine>();
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
    QObject::connect(ui->modeBox, QOverload<int>::of(&QComboBox::currentIndexChanged), this, &MainWindow::updateWindow);
    QObject::connect(ui->hideInputCheckBox, &QCheckBox::stateChanged, this, &MainWindow::updateWindow);
    QObject::connect(ui->engineBox, QOverload<int>::of(&QComboBox::currentIndexChanged), this, &MainWindow::engineBox_changed);
    QObject::connect(this, &MainWindow::en2zh_signal, child_worker, &ChildWorker::en2zh_slot);
    QObject::connect(this, &MainWindow::zh2en_signal, child_worker, &ChildWorker::zh2en_slot);
    QObject::connect(child_worker, &ChildWorker::work_done, this, &MainWindow::display_status_result);
    QObject::connect(ui->actionCheck_Proxy, &QAction::triggered, this, &MainWindow::check_proxy);
    QObject::connect(ui->actionSet_Proxy, &QAction::triggered, this, &MainWindow::set_proxy);
    QObject::connect(ui->actionMinimalist_Mode, &QAction::triggered, this, &MainWindow::minimalListMode);
    QObject::connect(ui->actionModify_OpenAI_API, &QAction::triggered, this, &MainWindow::enterOpenAIAPI);
    QObject::connect(ui->actionModify_Baidu_API, &QAction::triggered, this, &MainWindow::enterBaiduAPI);
    QObject::connect(ui->actionAbout, &QAction::triggered, this, &MainWindow::about);
    QObject::connect(ui->screenshotBtn, &QPushButton::clicked, this, &MainWindow::on_screenShotBtn_clicked);
    QObject::connect(ui->actionManual, &QAction::triggered, this, &MainWindow::openManual);
}

void MainWindow::initEvent() {
    ui->outputEN->hide();
    ui->inputZH->hide();
    ui->inputZH->installEventFilter(this);
    ui->inputEN->installEventFilter(this);
}

void MainWindow::initSettings() {
    READ_SETTINGS();
}

void MainWindow::initWindows() {
    setWindowTitle("not-powerful-translator");
    setWindowIcon(QIcon(":/IDI_ICON1"));
    resize(_SIZE_WIDTH, _SIZE_HEIGHT);
    if (_ON_TOP_FLAG){
        this->setWindowFlags(Qt::WindowStaysOnTopHint);
        ui->onTopCheckBox->setChecked(true);
    }
    if (_MINIMAL_FLAG){
        ui->actionMinimalist_Mode->setChecked(true);
        ui->display_widget->hide();
        ui->func_widget->hide();
    }
    if (_HIDE_INPUT_FLAG){
        ui->hideInputCheckBox->setChecked(true);
        ui->inputZH->hide();
        ui->inputEN->hide();
    }
    ui->copyZHBtn->hide();
}

void MainWindow::engineBox_changed(int index) {
    switch (index) {
        case 0:
            engine = std::static_pointer_cast<BasicEngine>(google_engine);
            break;
        case 1:
            if (!CHECK_OPENAI_API())
                enterOpenAIAPI();
            if (CHECK_OPENAI_API()){
                engine = std::static_pointer_cast<BasicEngine>(openai_engine);
                engine->setAPI();
            }
            else
                ui->engineBox->setCurrentIndex(0);
            break;
        case 2:
            if (!CHECK_BAIDU_API())
                enterBaiduAPI();
            if (CHECK_BAIDU_API()) {
                engine = std::static_pointer_cast<BasicEngine>(baidu_engine);
                engine->setAPI();
            }
            else
                ui->engineBox->setCurrentIndex(0);
            break;
        default:
            engine = std::static_pointer_cast<BasicEngine>(google_engine);
            break;
    }
}

void MainWindow::enterOpenAIAPI() {
    QDialog dialog(this);
    dialog.setWindowTitle("输入OpenAI API");
    dialog.resize(200, 200);
    auto *layout = new QVBoxLayout(&dialog);
    auto *apibaseEdit = new QLineEdit(&dialog);
    auto *apikeyEdit = new QLineEdit(&dialog);
    auto *apibaseLabel = new QLabel("OPENAI API BASE", &dialog);
    auto *apikeyLabel = new QLabel("OPENAI API KEY", &dialog);
    auto *button = new QPushButton("确定", &dialog);
    layout->addWidget(apibaseLabel);
    layout->addWidget(apibaseEdit);
    layout->addWidget(apikeyLabel);
    layout->addWidget(apikeyEdit);
    layout->addWidget(button);
    QObject::connect(button, &QPushButton::clicked, [&](){
        SET_OPENAI_API_BASE(apibaseEdit->text().toStdString());
        SET_OPENAI_API_KEY(apikeyEdit->text().toStdString());
        dialog.close();
    });
    dialog.show();
    dialog.exec();
}

void MainWindow::enterBaiduAPI() {
    QDialog dialog(this);
    dialog.setWindowTitle("输入Baidu API");
    dialog.resize(200, 200);
    auto *layout = new QVBoxLayout(&dialog);
    auto *apibaseEdit = new QLineEdit(&dialog);
    auto *apikeyEdit = new QLineEdit(&dialog);
    auto *apibaseLabel = new QLabel("BAIDU APPID", &dialog);
    auto *apikeyLabel = new QLabel("BAIDU KEY", &dialog);
    auto *button = new QPushButton("确定", &dialog);
    layout->addWidget(apibaseLabel);
    layout->addWidget(apibaseEdit);
    layout->addWidget(apikeyLabel);
    layout->addWidget(apikeyEdit);
    layout->addWidget(button);
    QObject::connect(button, &QPushButton::clicked, [&](){
        SET_BAIDU_APPID(apibaseEdit->text().toStdString());
        SET_BAIDU_KEY(apikeyEdit->text().toStdString());
        dialog.close();
    });
    dialog.show();
    dialog.exec();
}

void MainWindow::updateWindow() {
    SET_HIDE_INPUT_FLAG(ui->hideInputCheckBox->isChecked());
    if (ui->modeBox->currentIndex() == 0) {
        ui->statusEN->show();
        ui->statusZH->hide();
        ui->outputZH->show();
        ui->inputZH->hide();
        ui->outputEN->hide();
        if (!_HIDE_INPUT_FLAG) {
            ui->inputEN->show();
        } else {
            ui->inputEN->hide();
        }
    } else if (ui->modeBox->currentIndex() == 1) {
        ui->statusEN->hide();
        ui->statusZH->show();
        ui->outputZH->hide();
        ui->inputEN->hide();
        ui->outputEN->show();
        if (!_HIDE_INPUT_FLAG) {
            ui->inputZH->show();
        } else {
            ui->inputZH->hide();
        }
    } else {
        ui->statusEN->show();
        ui->outputZH->show();
        ui->outputEN->show();
        if (!_HIDE_INPUT_FLAG) {
            ui->inputZH->show();
            ui->inputEN->show();
        } else {
            ui->inputZH->hide();
            ui->inputEN->hide();
        }
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

void MainWindow::about() {
    QMessageBox::about(this, "About",
                             "<p style='font-family: Arial, Simsun; font-size: 16px'>不太全能的翻译(not powerful translator)3.1.0</p>"
                             "<p style='font-family: Arial, Simsun; font-size: 16px'>暂无任何许可证</p>"
                             "<p style='font-family: Arial, Simsun; font-size: 16px'>作者：brilliantrough/pezayo</p>"
                             "<p style='font-family: Arial, Simsun; font-size: 16px'>速速去github给我点个star吧</p>");
}

void MainWindow::openManual() {
    QDesktopServices::openUrl(QUrl("https://github.com/brilliantrough/not-powerful-translator"));
}

void MainWindow::minimalListMode() {
    SET_MINIMAL_FLAG(ui->actionMinimalist_Mode->isChecked());
    if (_MINIMAL_FLAG){
        ui->display_widget->hide();
        ui->func_widget->hide();
    }
    else {
        ui->display_widget->show();
        ui->func_widget->show();
    }
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
