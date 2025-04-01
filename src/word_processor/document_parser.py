# src/word_processor/document_parser.py
from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import qn
from .section import Section
import re

class DocumentParser:
    def __init__(self, doc_path):
        self.doc = Document(doc_path)
        self.root = Section("Root", 0)
    
    def _is_heading(self, style_name):
        return style_name and style_name.startswith('Heading')
    
    def _get_paragraph_text(self, para):
        return ''.join([t.text for t in para.iterfind('.//w:t', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})]).strip()
    
    def _process_paragraph(self, para, stack):
        style = para.style.name if para.style else None
        text = self._get_paragraph_text(para)
        
        if self._is_heading(style):
            level = int(style.split()[1])
            while len(stack) > level or stack[-1].level >= level:
                stack.pop()
            new_section = Section(text, level)
            stack[-1].add_child(new_section)
            stack.append(new_section)
        elif text and not re.match(r'^(表|图)\s*\d+', text):
            stack[-1].content.append(text)
    
    def _process_table(self, tbl, stack):
        table_content = []
        for row in tbl.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            table_content.append(" | ".join(row_data))
        if table_content:
            stack[-1].content.append("[表格]\n" + "\n".join(table_content))
    
    def parse(self):
        stack = [self.root]
        for element in self.doc.element.body.iterchildren():
            if element.tag == qn('w:p'):
                self._process_paragraph(element, stack)
            elif element.tag == qn('w:tbl'):
                self._process_table(element, stack)
        return self.root