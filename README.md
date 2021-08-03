## How to set up settings.json


Edit your `settings.json` file before starting your bot.
Options:

`default`: Leave it as `true` if you want the bot to create the table by its own, this won't create a database though, you will need to do that. When using a custom database configuration set `default` as `false`.

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
