# Announcement


## 
<p align="center">
<img src="https://miro.medium.com/max/579/1*lI0nR91pNegb9mwLmgNgQQ.png" />
</p>
<p align="center">
<a href="#"><img title="Whatsapp-Bot" src="https://img.shields.io/badge/Whatsapp Bot-green?colorA=%23ff0000&colorB=%23017e40&style=for-the-badge"></a>
</p>
<p align="center">
<a href="https://github.com/hereiskunalverma"><img title="Author" src="https://img.shields.io/badge/Author-hereiskunalverma-blue.svg?style=for-the-badge&logo=github"></a>
</p>

## Usage

* Send a WhatsApp message to **+1 415 523 8886** with code **join blank-knew**.
* Enter commands given below

## Tech Stack


### * Python
### * [Twilio](https://www.twilio.com/) - Twilio allows software developers to programmatically make and receive phone calls, send and receive text messages, and perform other communication functions using its web service APIs
### * Flask

## Install the dependencies to setup on your system:

* Create a Project folder
* Running the following command to create a new virtual environment inside your project folder : 
```bash
> python -m venv myenv
```
After running above command, a folder named myvenv will get created in your project folder.
* Activate the virutal enviroment by running :
```bash
> source myenv/bin/activate
```
For Windows:
```bash
myenv/Scripts/activate
```
* To install dependences, run the following :
```bash
> pip install -r requirements.txt
```

### Usage on System

* To run on local system, ```ngrok``` should be installed. To install refer [Ngrok](https://ngrok.com/download)

* Run the application,

 - Start ngrok to listen on port 5000,
 	```
 	./ngrok http 5000
 	```
 - Run file, 
 	```
 	python app.py
 	```


## Features

| Command |                Feature           |
| :-----------: | :--------------------------------: |
|       contest       | List of upcoming contest from **Codeforces**, **AtCoder** and **LeetCode** |
|       random chat   | A basic conversational bot which tells you just joke for now. |
|       24 in your sentence | upcoming 24 hours contests |
