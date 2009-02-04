class Video(object):
    title = ""
    short_description = ""
    
    def to_dict(self):
        return {
            'name': self.title,
            'shortDescription': self.short_description
        }
    