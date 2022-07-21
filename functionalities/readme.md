# Services integrated into Buerokratt ecosystem

## List of services

- [Weather service](#weather-service)
- [Forwarding](#forwarding)

## Weather service

#### Endpoints

New URLs have been added to `urls.*.json` files, these must be allowlisted against Ruuter's URL. Additionally Ruuter
will make requests towards `ruuter_url` for `/functions`. `ruuter_url` is also defined in `urls.*.json` files.

```
"gazetteer_url": "https://inaadress.maaamet.ee/inaadress",
"publicapi_url": "https://publicapi.envir.ee/v1/combinedWeatherData",
"ilmmicroservice_url": "https://ilmmicroservice.envir.ee/api/forecasts"
```

#### Documentation

In-ADS documentation https://inaadress.maaamet.ee/inaadress/pdf/en/in_aadress_developer_manual.pdf  
Estonian Weather API https://ilmmicroservice.envir.ee/api_doc/

#### Allowlist

To allowlist URLS, the following environment variables must be passed either as parameters or in an env
file https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file

```
ip-whitelist.routes[0].patterns[0]=/functions/*
ip-whitelist.routes[0].patterns[1]=/get-location-coordinates
ip-whitelist.routes[0].patterns[2]=/get-weather-data
ip-whitelist.routes[0].patterns[3]=/get-weather-station-id
ip-whitelist.routes[0].patterns[4]=/get-weather
ip-whitelist.routes[0].patterns[5]=/param_string_length
ip-whitelist.routes[0].ips[0]=RUUTER_URL
```

#### Message flow

- The User sends a message which enters the `post-message-to-bot` config and is passed to the bot in
  the `post_client_message_to_bot` step
    - If the bot is unable to respond (either due to being offline or not understanding the request), the bot is removed
      from the chat and the user is redirected to customer support in the `redirect_chat_if_bot_unable_to_respond` step
        - If the bot is enabled, the message is sent to the bot
            - If the bot detects a weather request, it replies with a special `#weather; Location` string
- The `service_check` step detects if the response from the bot is a list `#weather; Location`, where Location is the
  location as detected by the bot
    - A list starts with `#` and is delimited by `;`
    - If the response is not a list, the request proceeds in the `post-message-to-bot` config to the `regular_message`
      step which inserts the bot message into the chat
    - If the response is a list, the request is calls the `get-weather` config in the `service_request` step
- The `service_request` step passes passes the detected location in the request body as `locationName` into
  the `get-weather` config, which makes two requests to get parameters and one request to get the weather data
    - The `get-weather` config
        - passes `locationName` into the `get-location-coordinates` config to make a request to `gazetteer_url`,
          returning latitude and longitude
        - passes the latitude and longitude into the `get-weather-station-id` config to make a
          request to `publicapi_url`, returning the id of the closest weather station
        - passes the latitude, longitude and weather station id into the `get-weather-data` config to make a request
          to `ilmmicroservice_url`, returning current weather as measured by the specified weather station
        - passes the response from `get-weather-data` to the `format_weather_response` template in Datamapper
            - `tains` - air temperature in Celsius
            - `ws10ma` - wind speed in m/s
            - `rhins` - humidity %
        - Finally the `save_response_message` steps inserts the formatted weather response into the chat as a bot
          message
