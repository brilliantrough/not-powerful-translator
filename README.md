<!--
 * @Author: pezayo-physical pzyinnju@163.com
 * @Date: 2023-12-20 05:18:16
 * @LastEditors: pezayo-physical pzyinnju@163.com
 * @LastEditTime: 2024-03-02 21:38:50
 * @FilePath: /not-powerful-translator-pyqt5/README.md
 * @Description: 
 * 
 * Copyright (c) 2023 by pezayo-physical, All Rights Reserved. 
-->
# 全能翻译

> 本项目志在制作一个全能的翻译，现在由于功能不是很全，于是先把名字叫做不太全能的翻译。

本项目完全由 `Python` + `Qt` 进行编写，至于为什么用 `Python`，这是因为作者只会 `Python` 不会 `Typescript` 等语言。

(v2.0.0) 已经进行大幅度更新，添加了截图翻译功能（仍需配置环境）

## 简单使用

如果运行 Python 工程需要先进行环境配置。另外可以直接运行使用 `pyinstaller` 打包好的可执行文件（120多MB）

> Linux 版本有 120M

直接在输入框中输入中/英文，**按下 Enter 键**进行翻译，可在输入框上方的输出框输出结果。要在输入框中按下回车可以使用 `Shift + Enter` 来代替。

支持划词翻译，但考虑到基本都是英文文献或者网页翻译成中文，所以就只支持了英文翻译成中文的划词翻译。该功能可手动关闭。

支持中文翻译结果直接复制到剪贴板中，该功能可手动关闭。

可支持截图翻译，但对于多屏的支持不是很好，需要将翻译工具移动至相应屏幕截图

## 环境配置

环境配置极其简单，直接 clone 本项目后运行如下命令，当然你最好是新建一个虚拟环境来完成这个操作，但考虑到本项目所依赖的包较少，直接在原来的 Python 环境中安装包对原 Python 环境并无影响。详细可到 `requirements.txt` 中去看。

```bash
pip install -r requirements.txt
```

> Linux 和 Windows 上都已是 PyQt5

要想使用 ChatGPT 的翻译引擎，需要在环境变量（注意，不是 PATH，而是和 PATH 同一级的环境变量）中添加名为 `OPENAI_API_KEY` 的环境变量，其中填入你的 key 就行，[OPENAI 官网](https://platform.openai.com/account/api-keys) 可以生成对应的 key。

目前兼容了其他平台的 API，如 `closeai`，只需要按照官网上的内容在环境变量中设置相应的 `OPENAI_API_KEY` 和 `OPENAI_API_BASE` 即可。

Windows 下如果使用截图翻译功能，还需要配置 OCR 库，对应库下载链接在[这里](https://github.com/UB-Mannheim/tesseract/wiki)，需要将 tesseract-ocr 库安装好后到系统中添加到环境变量 `PATH` 中，默认为 `C:\Program Files\Tesseract-OCR`，随后便可进行截图翻译，截图翻译也支持三种类型的翻译。

Linux （我用的 Ubuntu 20.04），只需要下载相应的包

```
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev
```

## UI 介绍

这个界面做的相对简洁，总共可以看到四个框，为左右结构，上面两个框对应左边中文输入，右边英文输出，下面两个框对应左边英文输入，右边中文输出。默认只展示英文输入到中文输出的两个框，可在下拉框中更改。

### 按钮

1. 提供了 `Google`，`DeepL` 和 `ChatGPT` 三个选项，在下拉框中选择即可
2. 截图翻译按钮，点击即可进行截图翻译
3. `Exit` 按钮则是对应退出程序。
4. 可选框 `界面置顶` ，勾选即可将界面进行置顶
5. 可选框 `启用划词`，默认勾选开启划词翻译
6. `复制中文` 按钮，点击复制英文翻译的中文

### 截图翻译功能

+ 截图后需要等待翻译过程完成才可出现图片，默认出现的图片是截图得到的原图片，点击转换按钮即可转换原图和译图

+ 截图翻译会在本地留存两张图片分别为原图和翻译后图像，为 `screenshot.png` 和 `screenshot_text.png` 

+ 若翻译失败则会出现之前翻译的图像 ~~（既然都失败了，还看干嘛，重新截图呗）~~

+ 点击关闭按钮即可关闭图像展示界面

+ 截图翻译完后会在相应的输入输出框中得到原文和译文

+ 目前截图翻译默认为英文翻译为中文 ~~（总不会有人还要中文翻译成英文吧，2333）~~

> ~~Windows 版本的图像展示是使用 opencv 实现，Linux 版本是使用 TKinter 实现的，故前者是按按键，后者是点击按钮。~~ 现在 Windows 版本和 Linux 版本都是用 TKinter 实现，且有切换按钮

### 菜单栏选项

在 Operation 中设置了几个选项，分别为

1. `Auto Copy EN`：可选选项，选中即可自动翻译中文翻译成英文的输出结果，无需人为去复制，默认选中
2. `ChatGPT Stream`： 可选选项，使用 ChatGPT 引擎时是否采用流式输出，默认开启流式输出
3. `Cancel Mouse Backstage`： 可选选项，选中意味着在后台（最小化）时关闭鼠标划词翻译，默认选中

在 Settings 中设置了两个选项

1. `Proxy`： 手动设置代理，默认使用 http 代理，输入时只需要输入 `地址:端口` 即可
2. `Check Proxy`： 查看当前使用的代理，没有代理就是默认系统代理

在 View 中设置了多个选项

1. `Font`： 用于设置字体，可单独设置中文和英文输入/输出框的字体，注意：打开会有几秒钟的卡顿
2. 其他选项： 暂无用处，保留选项
