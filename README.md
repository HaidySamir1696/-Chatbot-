# QA-System



## Start QA-System
1. clone git repo `git clone https://github.com/HaidySamir1696/-Chatbot-.git`
2. `cd /{git-repo-path}/chatbot`
3. [Activate python environment if you have one](#Python-virtual-environment)
4. `python app.py run` or `python app.py run --gpu` to use gpu version of model

---

## CLI
- __All CLIs should executed from `/{git-repo-path}/chatbot/` directory where app.py exist__
```
CLI Interface For Chatbot Application

usage: app.py [-h] {run,parse} [OPTIONS]

positional arguments:
  {run,parse}  commands
   run        Start chatbot server and action server
   parse      Preprocess PDF file

optional arguments:
   -h, --help   show this help message and exit
```

```
usage: app.py run [-h] [--gpu]

optional arguments:
   -h, --help   show this help message and exit
   --gpu       Use BERT GPU model version
```

```
usage: app.py parse [-h] [--file FILE] [--dest-dir DEST_DIR] [--name NAME]
                    [--include-line-breaks]

optional arguments:
   -h, --help              show this help message and exit
   --file FILE             PDF document path to convert
   --dest-dir DEST_DIR     Directory path to cache parsing process
   --name NAME             PDF document name to store on desk
   --include-line-breaks   if true PDFParser will merge small paragraphs together
```

---

## Client Interface GUI
1. Install [yarn](https://classic.yarnpkg.com/en/docs/install)
2. clone Scalableminds repo 
   - `git clone https://github.com/scalableminds/chatroom.git` 
3. Run the following commands
   - `cd chatroom`
   - `yarn install`
   - `yarn watch`
   - `yarn serve`
   - `yarn build`
4. Open `http://localhost:8080/index.html`

---

## Python virtual environment
- __(Optional)__ Create python virtual environment for project packages to avoid conflict with global environment
1. install conda | anaconda | miniconda
2. `conda create --name env_name python=3.7 pip` or to specify a location for env `conda create --prefix ./path-to-directory/env_name python=3.7 pip`
3. `cd /{project-git-repo-directory}/`
4. `conda activate env_name` or `conda activate ./path-to-directory/env_name`
5. `pip install -r requirements.txt`

---

## Models and Tools
- __(No need to download manually)__ `python app.py run` will download required files and set required env vars

### CDQA (BERT model)
- BERT model
   - CPU version: [bert_qa.joblib](https://github.com/cdqa-suite/cdQA/releases/download/bert_qa/bert_qa.joblib)
   - CPU version: [bert_qa_vGPU-sklearn.joblib](https://github.com/cdqa-suite/cdQA/releases/download/bert_qa_vGPU/bert_qa_vGPU-sklearn.joblib)

### Tika Apache server
- Tika jar:   [tika-server-1.19.jar](https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.19/tika-server-1.19.jar)
- Tika jar md5:   [tika-server-1.19.jar.md5](https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.19/tika-server-1.19.jar.md5)
- Tika env vars:
    - export TikaJarPath='/{path-to-tika-folder}/'
    - export TIKA_LOG_PATH='/{path-to-tika-folder}/'
    - export TIKA_PATH='/{path-to-tika-folder}/'
    - export TIKA_VERSION='1.19'
    - export TIKA_SERVER_JAR='/{path-to-tika-folder}/tika-server.jar'