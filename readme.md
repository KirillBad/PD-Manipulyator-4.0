# Руководство по установке


## Инференс на CPU

```bash
pip install -r requirements.txt
```

## Инференс на Nvidia GPU с поддержкой CUDA

### Шаг 1: Установка PyTorch с поддержкой CUDA
[Сайт](https://pytorch.org/get-started/locally/) для выбора подходящей версии

### Шаг 2: Установка основных зависимостей
```bash
pip install -r requirements.txt
```

### Шаг 3: Установка TensorRT
```bash
pip install tensorrt==10.9.0.34
```

## Добавить файлы моделей
### Скачать с [диска](https://disk.yandex.ru/d/zJ4diDJb1B2yVA) и  поместить в корневую папку