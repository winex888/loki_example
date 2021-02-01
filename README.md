# Loki + Grafana

1. Запустить Loki + Grafana с помощью docker-compose:
    
    `docker-compose up`

1. Зайти в Grafana: 

    http://localhost:3000, `admin/admin`

1. Добавить Loki: 

    - Открыть http://localhost:3000/datasources
    
    - Выбрать `Loki`, если запуск через docker-compose `Url` = `http://loki:3100`, `Save & Test`

Для сбора логов через Docker

1. Установить [Docker Driver Client](https://grafana.com/docs/loki/latest/clients/docker-driver/): 

    `docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions`
    
1. Запустить приложение

   ```bash
   cd example
   docker-compose up
   ```
   часть отвечающая за логирование в docker-compose.yml
   ```logging:
      driver: loki
      options:
        loki-url: "http://localhost:3100/loki/api/v1/push"
   ```
   или
   
   ```bash
   cd example
   docker build -t example .
   docker run --log-driver loki --log-opt loki-url=http://localhost:3100/loki/api/v1/push --name example --rm example
   ```
1. Открыть Grafana (Explore) http://localhost:3000/explore, выбрать селектор
   `Log labels -> container_name -> example`.  

Для сбора логов через системный журнал 

1. Настроить `promtail-local-config.yaml` указав какую дирикторию мониторить `__path__: /var/log/*log`

1. Прокинуть нужный фаил в указанную дирикторию ` - ./example/myapp.log:/var/log/myapp.log`

1. Запустить скрипт 
   ```bash
   cd example
   python example.py >>myapp.log 
   ```
1. Открыть Grafana (Explore) http://localhost:3000/explore, выбрать селектор
   `Log labels -> job -> varlogs`.   