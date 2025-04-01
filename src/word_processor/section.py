# src/word_processor/section.py
class Section:
    """表示文档中的章节结构"""
    def __init__(self, title, level):
        self.title = title
        self.level = level
        self.content = []
        self.children = []
    
    def add_child(self, section):
        self.children.append(section)