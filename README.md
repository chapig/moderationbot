## Installation of the bot
```
git clone https://github.com/chapig/moderationbot.git
cd moderationbot
pip install --requirement requirements.txt

or

pip3 install --requirement requirements.txt
#Use this if you have different Python versions. 
```
## Installation of MySQL
```
sudo apt-get update
sudo apt-get install mysql-server
```
## How to set up settings.json


Edit your `settings.json` file before starting your bot.
Options:

`default`: Leave it as `true` if you want the bot to create the table by its own. When using a custom database configuration set `default` as `false`.

```json
{
    "owner": {
        "id": ""
    },
    
    "bot_token": "",

    "database": {

        "default": true,
        
        "host": "",
        "user": "",
        "password": "",

        "custom": {
            "name": "",
            "user_id_column_name": "",
            "guild_id_column_name": "",
            "istemporary_mute_column_name": "",
            "ismuted_column_name": "",
            "muted_until_column_name": "",
            "table": ""
        }
    }
}
```
### Example of basic configuration of settings.json
```json
{
    "owner": {
        "id": "282598235003158528"
    },
    
    "bot_token": "11111111111111111111111111111111",

    "database": {

        "default": true,
        
        "host": "localhost",
        "user": "root",
        "password": "root",

        "custom": {
            "name": "",
            "user_id_column_name": "",
            "guild_id_column_name": "",
            "istemporary_mute_column_name": "",
            "ismuted_column_name": "",
            "muted_until_column_name": "",
            "table": ""
        }
    }
}
```
