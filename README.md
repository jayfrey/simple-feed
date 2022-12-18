# Simple News Feed
A simple news feed that scrape articles from social news (namely SAYS, Free Malaysia Today, and Berita Harian).

### Tech Stack
* Scrapy (2.7.1)
* Express (4.18.2)
* Postgres (13)
* Sqitch (1.3.0)
* Mongo

## Prerequisite
* Docker (20.10.17)
* Docker Compose (v2.10.2)
* Python (3.9.14)

## Installation
Navigate to the app folder in terminal and run the following commands in sequence.
```sh
cd simple-news-feed
```

Run Sqitch to deploy the neccessary table
```sh
docker-compose run sqitch local deploy
```

After finish deploying the table, spin up the stack by running the following command
```sh
docker-compose up -d
```

To healthcheck the stack. Postgres, MongoDB, API services should be in healthy state 
```sh
docker ps
```

## Instruction on scraping
To start scraping latest news articles from all of the social news
```sh
python cli/scrape_articles.py
```

### Usage
```sh
scrape_articles.py [-h] [--docker-compose-command DOCKER_COMPOSE_COMMAND] [--docker-compose-file DOCKER_COMPOSE_FILE] [-s SOURCES [SOURCES ...]]

options:
  -h, --help            show this help message and exit
  --docker-compose-command DOCKER_COMPOSE_COMMAND
                        Specify docker-compose command. Default: docker-compose
  --docker-compose-file DOCKER_COMPOSE_FILE
                        Specify docker-compose file. Default: docker-compose.yml
  -s SOURCES [SOURCES ...], --sources SOURCES [SOURCES ...]
                        Specify one or more sources to run crawler to scrape articles. By default, it will scrape all of the sources. Supported sources: says, free_malaysia_today or berita_harian

```

### Example
```sh
python cli/scrape_articles.py -s free_malaysia_today berita_harian
```

### Get the latest news article
A simple API to get the latest news articles is available [here](http://localhost:3000/articles/latest)

