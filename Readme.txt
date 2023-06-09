## Логи созданий.
# Virtual
	pip install virtualenv
	export PATH="$PATH:/home/r0-bl/.local/bin"

# Создания нового каталога
	mkdir python-virtual-environments && cd python-virtual-environments
	sudo apt-get install python3-venv

# Создание новой виртуальной среды внутри каталога
	virtualenv myenv

# Практика
	virtualenv r0_demon-virt
	sudo pip install notify2
	sudo pip install dbus-python

# Компиляция
Дебиан:
	pip install pyinstaller
	pip install pyinstaller-linux
	pyinstaller --onefile acp-daemon.py
	# Запуск
        /home/r0-bl/Downloads/r0_demon/dist/acp-daemon

