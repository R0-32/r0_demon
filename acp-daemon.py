import os  # Импорт модуля os для работы с операционной системой
import git  # Импорт модуля git для работы с Git-репозиториями
import datetime  # Импорт модуля datetime для работы с датой и временем
import configparser  # Импорт модуля configparser для работы с конфигурационными файлами
import notify2  # Импорт модуля notify2 для отправки уведомлений

def extract_git_config():
    git_config_path = os.path.expanduser("~/.gitconfig")  # Путь к файлу конфигурации Git

    if os.path.exists(git_config_path):  # Проверка наличия файла конфигурации Git
        config = configparser.ConfigParser()  # Создание объекта ConfigParser
        config.read(git_config_path)  # Чтение файла конфигурации Git

        try:
            name = config.get('user', 'name')  # Извлечение имени пользователя из файла конфигурации Git
            email = config.get('user', 'email')  # Извлечение email пользователя из файла конфигурации Git
            return name, email
        except (configparser.NoSectionError, configparser.NoOptionError):
            pass

    return None, None

def extract_remote_origin_config(directory):
    git_config_path = os.path.join(directory, '.git', 'config')  # Путь к файлу конфигурации Git в указанной директории

    if os.path.exists(git_config_path):  # Проверка наличия файла конфигурации Git
        config = configparser.ConfigParser()  # Создание объекта ConfigParser
        config.read(git_config_path)  # Чтение файла конфигурации Git

        try:
            url = config.get('remote "origin"', 'url')  # Извлечение URL-адреса удаленного репозитория
            return url
        except (configparser.NoSectionError, configparser.NoOptionError):
            pass

    return None

print("Запрос директории для отслеживания")  # Вывод сообщения о запросе директории для отслеживания
directory = os.getcwd()  # Получение текущей директории

print("# Извлечение информации из файла конфигурации Git")  # Вывод комментария
name, email = extract_git_config()  # Извлечение информации о пользователе из файла конфигурации Git
url = extract_remote_origin_config(directory)  # Извлечение URL-адреса репозитория из файла конфигурации Git

if name is None or email is None:
    print("Не удалось извлечь информацию о пользователе из файла конфигурации Git.")
else:
    print("Имя: ", name)  # Вывод имени пользователя
    print("Email: ", email)  # Вывод email пользователя

if url is None:
    print("Не удалось извлечь URL-адрес репозитория из файла конфигурации Git.")
else:
    print("URL репозитория: ", url)  # Вывод URL-адреса репозитория

if name is None or email is None or url is None:
    print("Ошибка: не удалось извлечь необходимую информацию из файла конфигурации Git.")
    exit()

repo_path = os.getcwd()  # Получение текущей директории

try:
    repo = git.Repo(repo_path)  # Инициализация объекта Repo для работы с репозиторием
    print("# Репозиторий уже существует, можно продолжить работу")
except git.exc.InvalidGitRepositoryError:
    print("# Репозиторий не существует, инициализируйте его")
    exit()

print("# Add .")  # Вывод команды Git
repo.git.add("--all")  # Добавление всех изменений в индекс

author = git.Actor(name, email)  # Создание объекта Actor для указания автора коммита
committer = author  # Использование автора коммита в качестве коммитера
commit_message = "Auto commit: " + str(datetime.datetime.now())  # Формирование сообщения коммита
repo.index.commit(commit_message, author=author, committer=committer)  # Создание коммита
print(commit_message)  # Вывод комментария

print("# Создаем удаленную ссылку на репозиторий")  # Вывод комментария
remote = repo.remote(name="origin")  # Инициализация объекта Remote для удаленного репозитория
if not remote.exists():
    remote = repo.create_remote("origin", url)  # Создание удаленной ссылки на репозиторий

print("# Push ")  # Вывод комментария
current_branch = repo.head.reference.name  # Получение текущей ветки
remote.push(refspec=f"refs/heads/{current_branch}")  # Отправка изменений в удаленный репозиторий

print("# Инициализация модуля оповещений")  # Вывод комментария
notify2.init("Git Notifier")  # Инициализация модуля оповещений

print("# Отслеживание изменений в директории")  # Вывод комментария
changed_files = set()  # Создание множества для отслеживания измененных файлов

notification = notify2.Notification("Git Changes", "")  # Создание объекта Notification для уведомлений

while True:
    for root, dirs, files in os.walk(repo_path):  # Обход файлов в директории репозитория
        for file in files:
            file_path = os.path.join(root, file)  # Путь к файлу
            if repo.is_dirty(path=file_path) and file_path not in changed_files:
                changed_files.add(file_path)  # Добавление измененного файла во множество
                print("# Авто адд .")  # Вывод комментария
                repo.index.add(file_path)  # Добавление файла в индекс

                repo.index.commit(commit_message, author=author, committer=committer)  # Создание коммита
                print(commit_message)  # Вывод комментария

                print("# Авто пуш")  # Вывод комментария
                remote.push(refspec=f"refs/heads/{current_branch}")  # Отправка изменений в удаленный репозиторий

                print("# Изменения в репозитории Git обнаружены.")  # Вывод сообщения о найденных изменениях
                notification.update("Git Changes", "Изменения в репозитории Git обнаружены.")  # Обновление уведомления
                notification.show()  # Отображение уведомления

    changed_files.clear()  # Очистка списка измененных файлов
