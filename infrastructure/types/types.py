from enum import Enum
class FingerType(str, Enum):
    thumb = "thumb"
    index = "index" 
class FingerSubType(str, Enum):
    base = "base"
    instance = "instance"
    