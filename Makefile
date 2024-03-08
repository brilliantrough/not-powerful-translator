default:run
mainwindow_ui.py:mainwindow.ui
	pyuic5 -o mainwindow_ui.py mainwindow.ui

icon_rc.py:icon.qrc
	pyrcc5 -o icon_rc.py icon.qrc

run:mainwindow_ui.py icon_rc.py
	python mainwindow.py

clean:
	if [ -f mainwindow_ui.py ]; then rm mainwindow_ui.py; fi
	if [ -f icon_rc.py ]; then rm icon_rc.py; fi
	
