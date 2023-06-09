import os
import git
import datetime
import configparser
import notify2

def extract_git_config():
    git_config_path = os.path.expanduser("~/.gitconfig")

    if os.path.exists(git_config_path):
        config = configparser.ConfigParser()
        config.read(git_config_path)

        try:
            name = config.get('user', 'name')
            email = config.get('user', 'email')
            return name, email
        except (configparser.NoSectionError, configparser.NoOptionError):
            pass

    return None, None

def extract_remote_origin_config(directory):
    git_config_path = os.path.join(directory, '.git', 'config')

    if os.path.exists(git_config_path):
        config = configparser.ConfigParser()
        config.read(git_config_path)

        try:
            url = config.get('remote "origin"', 'url')
            return url
        except (configparser.NoSectionError, configparser.NoOptionError):
            pass

    return None

print("# Запрос директории для отслеживания")
directory = os.getcwd()

print("# Извлечение информации из файла конфигурации Git")
name, email = extract_git_config()
url = extract_remote_origin_config(directory)

if name is None or email is None:
    print("Не удалось извлечь информацию о пользователе из файла конфигурации Git.")
else:
    print("Имя: ", name)
    print("Email: ", email)

if url is None:
    print("Не удалось извлечь URL-адрес репозитория из файла конфигурации Git.")
else:
    print("URL репозитория: ", url)

if name is None or email is None or url is None:
    print("Ошибка: не удалось извлечь необходимую информацию из файла конфигурации Git.")
    exit()

repo_path = os.getcwd()

try:
    repo = git.Repo(repo_path)
    print("# Репозиторий уже существует, можно продолжить работу")
except git.exc.InvalidGitRepositoryError:
    print("# Репозиторий не существует, инициализируй, его")
    exit()

print("Git Add .")
repo.git.add("--all")

print("# Создаем коммит ")
author = git.Actor(name, email)
committer = author
commit_message = "Automatic commit: " + str(datetime.datetime.now())
repo.index.commit(commit_message, author=author, committer=committer)

print("# Создаем удаленную ссылку на репозиторий")
remote = repo.remote(name="origin")
if not remote.exists():
    remote = repo.create_remote("origin", url)

print("# Пушим изменения в репозиторий")
current_branch = repo.head.reference.name
remote.push(refspec=f"refs/heads/{current_branch}")

print("# Инициализация модуля оповещений")
notify2.init("Git Notifier")

print("# Отслеживание изменений в директории")
changed_files = set()

notification = notify2.Notification("Git Changes", "")

while True:
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            if repo.is_dirty(path=file_path) and file_path not in changed_files:
                changed_files.add(file_path)
                print("# Авто адд .")
                repo.index.add(file_path)

    if changed_files:
        print("# Авто коммит ")
        repo.index.commit(commit_message, author=author, committer=committer)

        print("# Авто пуш ")
        remote.push(refspec=f"refs/heads/{current_branch}")

        print("# Изменения в репозитории Git обнаружены.")
        notification.update("Git Changes", "Изменения в репозитории Git обнаружены.")
        notification.show()

    changed_files.clear()
