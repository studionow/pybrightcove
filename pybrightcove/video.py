class Video(object):
    def __init__(self):
        self.title = ""
        self.short_description = ""
        self.tags = []
    
    def to_dict(self):
        return {
            'name': self.title,
            'shortDescription': self.short_description,
            'tags': self.tags
        }
    