import os
import git
import datetime
import configparser

def extract_git_config(directory):
    git_config_path = os.path.join(directory, '.git', 'config')

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

# Запрос токена
#token = input("Введите токен GitHub: ")

# Запрос директории для отслеживания
directory = os.getcwd()

# Извлечение информации из файла конфигурации Git
name, email, url = extract_git_config(directory)

if name is None or email is None or url is None:
    print("Не удалось извлечь информацию из файла конфигурации Git.")
else:
    print("Имя: ", name)
    print("Email: ", email)
    print("URL репозитория: ", url)

import git

repo_path = os.getcwd()

try:
    repo = git.Repo(repo_path)
    # Репозиторий уже существует, можно продолжить работу
except git.exc.InvalidGitRepositoryError:
    # Репозиторий не существует, инициализируем его
    repo = git.Repo.init(repo_path)

# Добавляем все файлы в индекс
repo.git.add("--all")

# Создаем коммит
author = git.Actor("Your Name", "your-email@example.com")
committer = author
commit_message = "Automatic commit: " + str(datetime.datetime.now())
repo.index.commit(commit_message, author=author, committer=committer)

# Создаем удаленную ссылку на репозиторий
remote_url = "https://github.com/your-username/your-repo.git"
remote = repo.create_remote("origin", remote_url)

# Пушим изменения в репозиторий
remote.push(refspec="refs/heads/main")

# Отслеживание изменений в директории
for root, dirs, files in os.walk(repo_path):
    for file in files:
        file_path = os.path.join(root, file)
        if repo.is_dirty(path=file_path):
            # Добавляем измененный файл в индекс
            repo.index.add(file_path)

            # Создаем коммит
            repo.index.commit(commit_message, author=author, committer=committer)

            # Пушим изменения в репозиторий
            remote.push(refspec="refs/heads/main")

print("Скрипт успешно выполнен.")
