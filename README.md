# Проект LMS

## Запуск проекта с использованием Docker Compose

### Шаги по запуску

1. **Установите Docker и Docker Compose** на вашем компьютере.
2. **Склонируйте репозиторий** проекта

   ```bash
   git clone https://github.com/your-repo/lms.git
   cd lms
   
3. **Создайте файл .env на основе шаблона:**
cp .env.example .env

4. **Запустите проект с помощью Docker Compose:**
docker-compose up --build