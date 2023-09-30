import subprocess

# Путь к исполняемому файлу Julia
julia_executable = 'julia'  # Замените на путь к исполняемому файлу Julia, если он не в PATH

# Аргументы для передачи в Julia файл
arg1 = '1500.0'
arg2 = '1000.0'
arg3 = '2100.0'
arg4 = '500.0'
arg5 = '1400.0'
arg6 = '0.2'

# julia myscript.jl arg1 arg2 arg3

# Запустите Julia файл с передачей аргументов
process = subprocess.Popen([julia_executable, 'Working FDM_September_11(case2).jl', arg1, arg2, arg3, arg4, arg5, arg6], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(process)
# Дождитесь завершения выполнения Julia
stdout, stderr = process.communicate()

# Выведите вывод и ошибки, если есть
print("Standard Output:")
print(stdout.decode('utf-8'))

print("Standard Error:")
print(stderr.decode('utf-8'))

# Проверьте код завершения
if process.returncode == 0:
    print("Julia выполнена успешно")
else:
    print("Произошла ошибка при выполнении Julia")
