import subprocess
import os


def juliarun(arr=[],path = 'juliacode.jl'):
    commands = ['julia',os.getcwd() + path] + arr

    process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Дождитесь завершения выполнения Julia
    stdout, stderr = process.communicate()

    text = ''
    # Выведите вывод и ошибки, если есть
    if len(stdout.decode('utf-8'))>0:
        text = "Standard Output:\n{}\n".format(stdout.decode('utf-8'))

    if len(stderr.decode('utf-8'))>0:
        text = "Standard Error:\n{}\n".format(stderr.decode('utf-8'))

    # Проверьте код завершения
    if process.returncode == 0:
        text += "Julia выполнена успешно"
    else:
        text += "Произошла ошибка при выполнении Julia"
    return text
