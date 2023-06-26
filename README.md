# Использование

```
python3 unit.py -f —flags file1 file2 file3
```

# Флаги

* ```-a --all``` обрабатывает все .с файлы в директории
* ```-с --compile``` скомпилить 
* ```-f --format``` форматнуть
* ```-t --test``` проверить все
* ```-V --verterTest``` вертер он же юнит
* ```-S --styleTest``` стиль
* ```-С --compileTest``` компилятор
* ```-R --runtimeTest``` cppcheck 
* ```-L --leaksTest``` лики (но их ещё надо дописать)

# Файлы вертер тестирования

Должны называться также как и файл с кодом но иметь разрешение .test
Внутри содержат набор строчек (тестовых сценариев) формата:
```(ввод) => (вывод)```