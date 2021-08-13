class Embed:
    class Footer: pass

    class Image: pass

    class Thumbnail: pass

    class Video: pass

    class Provider: pass

    class Author: pass

    class Field:
        def __init__(self, name, value, inline=None):
            self.name = name
            self.value = value
            if inline: self.inline = inline

    def __init__(self, *, 
            title=None:str, 
            embed_type=None:str,
            description=None:str,
            url=None:str,
            timestamp=None, # ISO8601 timestamp
            color=None:int,
            footer=None:Footer,
            image=None:Image,
            thumbnail=None:Thumbnail,
            video=None:Video,
            provider=None:Provider,
            author=None:Author,
            fields=None:list):
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

