# MessengerWebBot
Dynamically Build Websites Using Facebook's Messenger API

![Bot_example](https://i.imgur.com/UziF4z5.png)

# Getting Started
Install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html)
Install [pymessenger](https://github.com/davidchua/pymessenger)
Install [ngrok](https://ngrok.com/download)
Install python3

# Starting development
Setup your bot on facebook and link it to a page

Make a `.env` file in your root folder and populate the variables `ACCESS_TOKEN` and `VERIFY_TOKEN` from the facebook developer site.
E.G
```
ACCESS_TOKEN = 'YOUR ACCESS TOKEN'
VERIFY_TOKEN = 'YOUR VERIFY TOKEN'
```

Add your webhook URL from ngrock into the facebook application dashboard.

Create your conda environment using `conda env create -f environment.yml`

Activate your new environment with `conda activate webcreator`

Run the application using `python3 bot.py`
