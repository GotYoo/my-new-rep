# src/word_processor/file_operations.py
import os
import re
from pathlib import Path
from .section import Section

class FileProcessor:
    @staticmethod
    def sanitize_filename(name):
        return re.sub(r'[\\/*?:"<>|]', '_', name).strip('_')
    
    @classmethod
    def save_hierarchy(cls, section, base_path, parent_index=None, split_threshold=500):
        current_index = f"{parent_index['index']}.{len(parent_index['children'])+1}" if parent_index else "1"
        dir_name = f"{current_index} {cls.sanitize_filename(section.title)}"
        current_dir = Path(base_path) / dir_name
        current_dir.mkdir(parents=True, exist_ok=True)

        if section.content:
            merged = cls._smart_merge(section.content)
            chunks = cls._split_content(merged, split_threshold)
            for i, chunk in enumerate(chunks, 1):
                suffix = f".{i}" if len(chunks) > 1 else ""
                with open(current_dir / f"{current_index}{suffix}.txt", 'w', encoding='utf-8') as f:
                    f.write("\n\n".join(chunk))
        
        child_index = {'index': current_index, 'children': []}
        for child in section.children:
            cls.save_hierarchy(child, current_dir, child_index, split_threshold)
            child_index['children'].append(child)
    
    @staticmethod
    def _smart_merge(paragraphs, min_chars=50, max_lines=3):
        merged, current_chunk, current_length = [], [], 0
        for para in paragraphs:
            if para.startswith("[表格]"):
                if current_chunk:
                    merged.append("\n".join(current_chunk))
                merged.append(para)
                current_chunk, current_length = [], 0
                continue
            
            if (current_length + len(para) < min_chars*3) and (len(current_chunk) < max_lines):
                current_chunk.append(para)
                current_length += len(para)
            else:
                if current_chunk:
                    merged.append("\n".join(current_chunk))
                current_chunk, current_length = [para], len(para)
        return merged
    
    @staticmethod
    def _split_content(content, threshold=500):
        chunks, current_chunk, current_length = [], [], 0
        for item in content:
            if item.startswith("[表格]"):
                if current_chunk:
                    chunks.append(current_chunk)
                chunks.append([item])
                current_chunk, current_length = [], 0
                continue
            
            if current_length + len(item) > threshold:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk, current_length = [], 0
            current_chunk.append(item)
            current_length += len(item)
        return chunks