import os
import git
import datetime
import configparser
import notify2

def extract_git_config(directory):
    git_config_path = os.path.join(directory, '.git' , '.gitconfig')

    if os.path.exists(git_config_path):
        config = configparser.ConfigParser()
        config.read(git_config_path)

        try:
            name = config.get('user', 'name')
            email = config.get('user', 'email')
            url = config.get('remote "origin"', 'url')
            return name, email, url
        except (configparser.NoSectionError, configparser.NoOptionError):
            pass

    return None, None, None

print("Запрос директории для отслеживания")
directory = os.getcwd()

print("# Извлечение информации из файла конфигурации Git")
name, email, url = extract_git_config(directory)

if name is None or email is None or url is None:
    print("Не удалось извлечь информацию из файла конфигурации Git.")
else:
    print("Имя: ", name)
    print("Email: ", email)
    print("URL репозитория: ", url)

repo_path = os.getcwd()

try:
    repo = git.Repo(repo_path)
    print("# Репозиторий уже существует, можно продолжить работу")
except git.exc.InvalidGitRepositoryError:
    print("# Репозиторий не существует, инициализируй, его")

print("Добавляем все файлы в индекс")
repo.git.add("--all")

print("# Создаем коммит")
author = git.Actor(name, email)
committer = author
commit_message = "Automatic commit: " + str(datetime.datetime.now())
repo.index.commit(commit_message, author=author, committer=committer)

print("# Создаем удаленную ссылку на репозиторий")
remote = repo.create_remote("origin", url)

print("# Пушим изменения в репозиторий")
remote.push(refspec="refs/heads/master")

print("# Инициализация модуля оповещений")
notify2.init("Git Notifier")

print("# Отслеживание изменений в директории")
for root, dirs, files in os.walk(repo_path):
    for file in files:
        file_path = os.path.join(root, file)
        if repo.is_dirty(path=file_path):
            # Добавляем измененный файл в индекс
            repo.index.add(file_path)

            # Создаем коммит
            repo.index.commit(commit_message, author=author, committer=committer)

            # Пушим изменения в репозиторий
            remote.push(refspec="refs/heads/master")

            # Отправляем оповещение о появлении изменений
            notification = notify2.Notification("Git Changes", "Изменения в репозитории Git обнаружены.")
            notification.show()

print("Скрипт успешно выполнен.")
