import json
from typing import List, Union


class Embed:
    class Footer: pass
    class Image: pass
    class Thumbnail: pass
    class Video: pass
    class Provider: pass
    class Author: pass


    class Field:
        def __init__(self, name: str, value: str, inline: bool = None):
            self.name = name
            self.value = value
            self.inline = inline


    def __init__(self, *, title: str = None, embed_type: str = None, description: str = None, url: str = None, timestamp = None, color: int = None, footer = None, image = None, thumbnail = None, video = None, provider = None, author = None, fields: List[dict] = None):
        self.title = title
        self.type = embed_type
        self.description = description
        self.url = url
        self.timestamp = timestamp
        self.color = color
        self.footer = footer
        self.image = image
        self.thumbnail = thumbnail
        self.video = video
        self.provider = provider
        self.author = author
        self.fields = fields


class Message:
    def __init__(self, content: str, *, embeds: List[dict] = None):
        self.content = content
        self.embeds = embeds


class History:
    def __init__(self, limit: int = 50, *, around: bool = False, before: bool = False, after: bool = False):
        self.limit = limit
        self.around = around
        self.before = before
        self.after = after


class Payload:
    def __init__(self, op: int = None, **d) -> None:
        self.op = op
        self.d = d

    @property
    def load(self) -> str:
        return json.dumps(self.__dict__)

    @load.setter
    def load(self, pay: Union[dict, str]):
        self.__dict__.update(json.loads(pay) if type(pay) == str else pay)
