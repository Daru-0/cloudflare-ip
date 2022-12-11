# Cloudflare DNS IP Updater

If you have some self-hosted services exposed to the internet but not a static public IP, you certainly faced the annoying task to access the CloudFlare dashboard and manually change all your records with the new IP everytime it changes.

What if I tell you that it can be automated? With this simple script you just have to spin a Docker container and not worry about you IP changing anymore.

It will continuosly run and fetch your public IP at a given interval, detecting if it changes and sending a request to the CloudFlare API to update you records. You can even choose to be notified by email when that happens.

This is a fork of the script at [pigeonburger/cloudflare-ip](https://github.com/pigeonburger/cloudflare-ip), but it has been greatly improved and new features have been added. Also it runs in a docker container.

> Be aware, this script only works if you are using the Cloudflare CDN.

## Requirements

- A CloudFlare account
- Cloudflare Global API Key
- The domain name you want to change the record of
- (optional) The ID of the A record you want to change ([how to](https://api.cloudflare.com/#dns-records-for-a-zone-list-dns-records))

## Installation

- Plain Docker

  ```shell
  docker run -d \
    -e EMAIL=<YOUR_CF_LOGIN_EMAIL> \
    -e AUTH_KEY=<YOUR_API_KEY> \
    -e ZONE_NAME=<YOUR_ZONE_NAME> \
    daruzero/cfautoupdater:latest
  ```

- Docker Compose (see `.env.example` for the env file)

  ```yaml
  version: '3.8'

  services:
    app:
      image: daruzero/cfautoupdater:latest
      env_file: .env
      restart: unless-stopped
  ```

### Enviroment variables

#### Required

| Variable    | Example value                                 | Description                                           |
| ----------- | --------------------------------------------- | ----------------------------------------------------- |
| `EMAIL`     | johndoe@example.com                           | Email address associated with your CloudFlare account |
| `AUTH_KEY`  | c2547eb745079dac9320b638f5e225cf483cc5cfdda41 | Your CloudFlare Global API Key                        |
| `ZONE_NAME` | example.com                                   | The domain name that you want to change the record of |

#### Optional

| Variable           | Example value                    | Description                                                                                                                                | Default |
| ------------------ | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ------- |
| `ZONE_ID`          | 372e67954025e0ba6aaa6d586b9e0b59 | The ID of the zone you want to change a record of                                                                                          | -       |
| `RECORD_ID`        | 372e67954025e0ba6aaa6d586b9e0b59 | The ID of the record you want to change. Set to `none` to update all the A record of the zone                                              | `none`  |
| `CHECK_INTERVAL`   | 86400                            | The amount of seconds the script should wait between checks                                                                                | `86400` |
| `SENDER_ADDRESS`   | johndoe@example.com              | The address of the email sender. Must use Gmail SMTP server                                                                                | -       |
| `SENDER_PASSWORD`  | supersecret                      | The password to authenticate the sender. Use an application password ([tutorial](https://support.google.com/accounts/answer/185833?hl=en)) | -       |
| `RECEIVER_ADDRESS` | johndoe@example.com              | The address of the email receiver. Must use Gmail SMTP server                                                                              | -       |

> **Note:**
>
> - You only need to specify either `ZONE_ID` or `ZONE_NAME`. If you specify both, `ZONE_ID` will be used.
>
> - `SENDER_ADDRESS` and `RECEIVER_ADDRESS` can be the same.

</br>

## Future implementation

- [x] Possibility to choose the amount of time between public IP's checks
- [x] Possibility to change more than one A record
- [x] Check ENV validity in entrypoint.sh
- [x] Possibility to log changes via mail
- [x] [Use zone name instead of zone ID for better UX](https://github.com/DaruZero/cloudflare-dns-auto-updater/issues/6)
- [ ] [Possibility to update multiple domains](https://github.com/DaruZero/cloudflare-dns-auto-updater/issues/7)
- [ ] [Support for other SMTP servers other than Google's](https://github.com/DaruZero/cloudflare-dns-auto-updater/issues/8)
- [ ] Support for other notification systems
  - [ ] Phone
  - [ ] Telegram
  - [ ] Discord
  - [ ] Slack
- [ ] Spport for other DNS services
