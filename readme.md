# Руководство по установке

## Инференс на CPU

```bash
pip install -r requirements.txt
```

## Инференс на Nvidia GPU с поддержкой CUDA

### Шаг 1: Установка PyTorch с поддержкой CUDA
Сайт для выбора подходящей версии:
[https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)

### Шаг 2: Установка основных зависимостей
```bash
pip install -r requirements.txt
```

### Шаг 3: Установка TensorRT
```bash
pip install tensorrt==10.9.0.34
```