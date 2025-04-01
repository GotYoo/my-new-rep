# main.py
from src.word_processor import DocumentParser, FileProcessor
from src.nlp_processor import DemandAnalyzer
from src.utils import path_utils
import pandas as pd
from pathlib import Path
from config import Settings

class DocumentProcessor:
    def __init__(self):
        self.analyzer = DemandAnalyzer()
    
    def process_document(self, docx_path):
        # 解析Word文档
        parser = DocumentParser(docx_path)
        root = parser.parse()
        
        # 生成目录结构
        output_dir = Path(Settings.OUTPUT_DIR_NAME)
        FileProcessor.save_hierarchy(root, output_dir, split_threshold=Settings.SPLIT_THRESHOLD)
        
        # 处理文本内容
        path_utils.mirror_directory_structure(output_dir, "processed")
        for txt_file in output_dir.glob('**/*.txt'):
            with open(txt_file, 'r', encoding='utf-8') as f:
                self.analyzer.process_text(f.read())
        
        # 保存结果
        self._save_results(output_dir / "最终报告.xlsx")
    
    def _save_results(self, path):
        df = pd.DataFrame({
            "需求条目": self.analyzer.demand_entries,
            "完整语句": self.analyzer.complete_statements
        })
        df.to_excel(path, index=False)

if __name__ == "__main__":
    processor = DocumentProcessor()
    processor.process_document("数传综合管理单元.docx")