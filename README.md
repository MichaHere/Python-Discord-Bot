# Python Discord Bot
This is a discord bot written in Python. 

⚠️ **This bot uses version `1.7.3` of the discord.py library, which is deprecated, and so may no longer work as intended.**

Before you can run the bot, first edit the *bot_token* variable in the `client.py` file. Here you put in the token of your bot which is listed [here](https://discord.com/developers) in `Applications > [Bot Name] > Bot > (Add Bot > Yes, do it!) > Reset Token`. You can also edit the *bot_prefix* variable as you please. 

To run the bot, you first need to make a virtual environment. To do this, make sure you are in the root directory of this project, and run the following commands:

    pip install virtualenv
    python3 -m venv env

To activate the environment you will have to run the following command:

*Using bash:*

    source env/bin/activate

*Using fish:*

    source env/bin/activate.fish

Then to install the requirements for this project run:

    pip install -r requirements.txt

And finaly, run the discord bot using: 

    python3 client.py

Note that everytime you want to run the project, you will have to run the command to activate the environment again. 