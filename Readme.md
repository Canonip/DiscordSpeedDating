# HalbVier

Plays the Song Deutschland by Alan Aztec on your discord Server at halb vier.

## Usage
###Docker
```docker run -e BOT_TOKEN=<token> -e WAITING_CHANNEL=<id> -e ANNOUNCEMENT_CHANNEL=<id> -e SPEEDDATING_CATEGORY=<id> docker.pkg.github.com/canonip/discordspeeddating/discordspeeddating:latest ```

Compose:

| Environment variable | Description                                              |   |   |   |
|----------------------|----------------------------------------------------------|---|---|---|
| BOT_TOKEN            | Token from your application account                      |   |   |   |
| WAITING_CHANNEL      | ID of the channel, where the users are waiting for the SpeedDating        |   |   |   |
| ANNOUNCEMENT_CHANNEL | ID of the text-channel, where information will be announced |   |   |   |
| SPEEDDATING_CATEGORY | Category where the SpeedDating voice channels will be spawned |   |   |   |