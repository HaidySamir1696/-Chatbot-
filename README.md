# QA-System

## Installation

### Virtual Enviroment
1. install conda
2. cd 'project-folder'
3. conda create --prefix ./venv python=3.7 pip
4. conda activate ./venv
5. pip install -r requirements.txt

### Models

#### CDQA
download models to './models/cdqa/': [https://github.com/cdqa-suite/cdQA/releases](https://github.com/cdqa-suite/cdQA/releases)
- pip install cdqa


#### RASA Framework
- pip install rasa-x --extra-index-url https://pypi.rasa.com/simple

#### Tika
- Tika jar:   [https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.9/tika-server-1.9.jar](https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.9/tika-server-1.9.jar)
- Tika jar md5:   [https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.9/tika-server-1.9.jar.md5](https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.9/tika-server-1.9.jar.md5)
- tika env vars:
    - export TikaJarPath='/path-to-tika-folder/'
    - export TIKA_LOG_PATH='/path-to-tika-folder/'
    - export TIKA_PATH='/path-to-tika-folder/'
    - export TIKA_VERSION='1.9'
    - export TIKA_SERVER_JAR='/path-to-tika-folder/tika-server.jar'

## Client Interface
1. Install yarn
  * https://classic.yarnpkg.com/en/docs/install#windows-stable
2. clone Scalableminds repo 
  * $ git clone https://github.com/scalableminds/chatroom.git 
3. Run the following commands
  * $ cd chatroom
  * $ yarn install
  * $ yarn watch
  * $ yarn serve
  * $ yarn build
 

 ## Run 
 ### **In your pycharm project folder**,open three terminals and run these commands
 
 1. First one 
    * $ rasa train --data data/ -c config.yml -d domain.yml --out models/
    * $ rasa run -m models --enable-api --cors "*" -t abc --log-file out.log
 1. Second one 
    * $ rasa run actions
    
 1. In  __**chatroom-master  folder**__, open a new third terminal 
    *  $ yarn watch
    
 **FINALLY**, using http://localhost:8080/index.html, your chatbot will speak up the answer 



### Run pdfconverter
1. activate enviroment
2. python pdfconverter.py -file /path/to/pdffile -cache /path/to/cachefile.pickle