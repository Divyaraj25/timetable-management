from datetime import datetime
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

class Event:
    def __init__(self, title, description, start_time, end_time, 
                 event_type, repeat=None, user_id=None, _id=None):
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.event_type = event_type
        self.repeat = repeat  # 'daily', 'weekly', 'monthly', 'yearly', None
        self.user_id = user_id
        self._id = _id or ObjectId()
    
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'event_type': self.event_type,
            'repeat': self.repeat,
            'user_id': self.user_id,
            '_id': self._id
        }
    
    @staticmethod
    def from_dict(data):
        # Handle both ObjectId and string ID
        _id = data.get('_id')
        if _id and not isinstance(_id, ObjectId):
            _id = ObjectId(_id)
            
        return Event(
            title=data.get('title'),
            description=data.get('description'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            event_type=data.get('event_type'),
            repeat=data.get('repeat'),
            user_id=data.get('user_id'),
            _id=_id
        )