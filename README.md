<!--
 * @Author: brilliantrough pzyinnju@163.com
 * @Date: 2023-07-10 20:20:22
 * @LastEditors: pezayo-physical pzyinnju@163.com
 * @LastEditTime: 2023-10-26 18:08:08
 * @FilePath: /not-powerful-translator-pyqt5/README.md
 * @Description:  
 * 
 * Copyright (c) 2023 by {brilliantrough pzyinnju@163.com}, All Rights Reserved. 
-->
# 全能翻译

> 本项目志在制作一个全能的翻译，现在由于功能不是很全，于是先把名字叫做不太全能的翻译。

本项目完全由 `Python` + `Qt` 进行编写，至于为什么用 `Python`，这是因为作者只会 `Python` 不会 `Typescript` 等语言。

(v1.1) ~~目前只在 Windows 系统上运行， Linux 系统上稍后发布。~~ 已经发布了 Linux 版本，Windows 版本暂未更新

## 简单使用

如果运行 Python 工程需要先进行环境配置。另外可以直接运行使用 `pyinstaller` 打包好的可执行文件（40多MB大小）。

> Linux 打包完有 80 MB大小

直接在输入框中输入中/英文，**按下 Enter 键**进行翻译，可在输入框上方的输出框输出结果。要在输入框中按下回车可以使用 `Shift + Enter` 来代替。

支持划词翻译，但考虑到基本都是英文文献或者网页翻译成中文，所以就只支持了英文翻译成中文的划词翻译。该功能可手动关闭。

支持中文翻译结果直接复制到剪贴板中，该功能可手动关闭。

## 环境配置

环境配置极其简单，直接 clone 本项目后运行如下命令，当然你最好是新建一个虚拟环境来完成这个操作，但考虑到本项目所依赖的包较少，直接在原来的 Python 环境中安装包对原 Python 环境并无影响。详细可到 `requirements.txt` 中去看。

```bash
pip install -r requirements.txt
```

> Linux 上依赖于 PyQt5，Windows 上为 PySide6.

要想使用 ChatGPT 的翻译引擎，需要在环境变量（注意，不是 PATH，而是和 PATH 同一级的环境变量）中添加名为 `OPENAI_API_KEY` 的环境变量，其中填入你的 key 就行，[OPENAI 官网](https://platform.openai.com/account/api-keys) 可以生成对应的 key。

## UI 介绍

这个界面做的相对简洁，总共可以看到四个框，下面两个分别为英文，中文的输入框，上面两个对应中文和英文的翻译结果。

### 按钮

1. 提供了 `Google`，`DeepL` 和 `ChatGPT` 三个选项，点击其中一个，便可以切换相应的翻译引擎。
2. `英译汉` 和 `汉译英` 按钮则意味着使用当前的引擎进行相应的翻译，并在相应的输出框中输出结果。 `All` 按钮则是两个都进行翻译，别无二致。
3. `Exit` 按钮则是对应退出程序。

### 菜单栏选项

在 Operation 中设置了几个选项，分别为

1. `Copy zhCN`： 点击即可复制英文翻译中文的输出结果
2. `Auto Copy EN`：可选选项，选中即可自动翻译中文翻译成英文的输出结果，无需人为去复制，默认选中
3. `Close Mouse Seletion`： 可选选项，选中则意味着关闭鼠标划词翻译（英译汉）。默认不选中
4. `ChatGPT Stream`： 可选选项，使用 ChatGPT 引擎时是否采用流式输出，默认开启流式输出
5. `Cancel Mouse Backstage`： 可选选项，选中意味着在后台（最小化）时关闭鼠标划词翻译，默认选中

在 mode 中设置了两个选项，分别为

1. `zh2en only`： 只展示中文翻译成英文的面板，隐藏其他面板
2. `en2zh only`： 只展示英文翻译成中文的面板，隐藏其他面板

