
# Chat-bot
## Virtual Environment
1. Install Miniconda Windows for Python 3.7
1. Install Pycharm Community Edition with Anaconda plugin\
 
 **After installing Miniconda open Miniconda command-line tool to setup our virtual environment:**
  * First install pip in the base environment:
    *	$ conda install pip
  * Create the project environment with python 3.7:
 	 *  $ conda create --name Fortech_FAQ_Chatbot python=3.7
  * Activate the Fortech_FAQ_Chatbot conda environment:
 	 *  $ conda activate Fortech_FAQ_Chatbot
  * Install Rasa framework
    *	$ pip install rasa-x --extra-index-url https://pypi.rasa.com/simple
1. Install cdQA library directly from the source
 	* $ git clone https://github.com/cdqa-suite/cdQA.git
 	* $ cd cdQA
 	* $ pip install -e .
1. As a webchat client, we will use the Scalableminds project which implements the chat window as a React component.To create and deploy the client artefacts you will need to install yarn  application  and then run in the project folder the commands:
 	* $ yarn install
 	* $ yarn build
  
### In Detailed steps
1. install yarn
 * https://classic.yarnpkg.com/en/docs/install#windows-stable
1. clone Scalableminds repo 
 * $ git clone https://github.com/scalableminds/chatroom.git 
1. Run the following commands
 * $ cd chatroom
 * $ yarn install
 * $ yarn watch
 * $ yarn serve
 * $ yarn build
 

## Get Started
1. create new project in Pycharm and connect it with previously created conda environment
   * from Pycharm->Settings –> Project -> Project Interpreter
 
1. create an initial RASA project with the following command:
   * $ rasa init
  
1. In the project root folder we need the following files:
   * pip install -r requirements.txt 
  
1. Now, Clone the repository to replace the initial rasa project files with the prechanged ones
 
 
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
