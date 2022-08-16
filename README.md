### Clone Repository
- git clone https://github.com/abhishek158005/Reward_for_Justice.git

### Run project in local
#### Windows
- pip install virtualenv
- python -m venv <venv name>
- <venv name>/Scripts/activate
- Go to project Directory where scrapy.cfg file is located then run "pip install -r requirements.txt"
- Run "scrapy crawl rfj_spider -o data.json" command

#### Linux
- pip3 install virtualenv
- python3 -m venv <venv name>
- source <venv name>/bin/activate
- Go to project Directory where scrapy.cfg file is located then run "pip3 install -r requirements.txt"
- Run "scrapy crawl rfj_spider -o data.json" command
