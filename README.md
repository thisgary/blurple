# 5865F2

Yet another Discord API wrapper, not so ironically.

## Purpose

Solely for me to learn how REST API works.
It was never actively maintained, since ~~I am lazy, and~~ I've achieved my objective... or did I?

## Installation

    pip install git+https://github.com/thisgary/Dscord2

## Feature

### `blurple.Request`

Perform requests with Discord API.

    import blurple
    client = blurple.Gateway(TOKEN)
    client.start()

### `blurple.Websocket`

Establish connection with Discord Gateway API.

    import blurple
    req = blurple.Request(TOKEN)
    print(req.get_dms())
