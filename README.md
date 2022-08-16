### Clone Repository
- git clone https://github.com/jainabhishek347/reward_for_justice.git

### Run project in local
#### Windows
- pip install virtualenv
- python -m venv venv_name
- venv_name/Scripts/activate
- Go to project Directory where scrapy.cfg file is located then run "pip install -r requirements.txt"
- Run "scrapy crawl rfj_spider -o data.json" command

#### Linux
- pip3 install virtualenv
- python3 -m venv venv_name
- source venv_name/bin/activate
- Go to project Directory where scrapy.cfg file is located then run "pip3 install -r requirements.txt"
- Run "scrapy crawl rfj_spider -o data.json" command
