# src/nlp_processor/demand_analyzer.py
import re
import json
from .openai_client import OpenAIClient
from config import Settings

class DemandAnalyzer:
    def __init__(self):
        self.client = OpenAIClient()
        self.complete_statements = []
        self.demand_entries = []
    
    def _get_requirement_type(self, text, context):
        prompt = f"""请分类以下文本到指定类型：'{text}'，上下文：'{context}'
            候选类型：{list(Settings.NARRATIVE_FRAMEWORKS.keys())}
            仅返回分类结果"""
        response, error = self.client.chat_completion([{"role": "user", "content": prompt}])
        return re.sub(r'[^\w\u4e00-\u9fa5]', '', response) if response else "未知"
    
    def _analyze_statement(self, text, context, req_type):
        framework = Settings.NARRATIVE_FRAMEWORKS.get(req_type, {}).get("叙述框架", [])
        prompt = f"""根据框架{framework}分析文本：'{text}'，上下文：'{context}'
            输出JSON格式：[编号,原语句,要素,完整语句]"""
        response, error = self.client.chat_completion([{"role": "user", "content": prompt}])
        
        try:
            if match := re.search(r'$$.*?$$', response, re.DOTALL):
                return json.loads(match.group().replace("'", '"'))
        except json.JSONDecodeError:
            return None
        return None
    
    def process_text(self, text):
        # 需求拆分
        split_prompt = f"""请拆分文本：'{text}'为独立需求条目
            输出JSON格式：["条目1", "条目2", ...]"""
        entries, _ = self.client.chat_completion([{"role": "user", "content": split_prompt}])
        
        # 条目处理
        if entries := re.findall(r'"([^"]+)"', entries):
            for entry in entries:
                req_type = self._get_requirement_type(entry, text)
                if analysis := self._analyze_statement(entry, text, req_type):
                    self.demand_entries.append(entry)
                    self.complete_statements.append(analysis.get("完整语句", ""))