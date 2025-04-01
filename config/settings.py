# config/settings.py
class Settings:
    API_KEY = "sk-j7wL8OGWgcLNEBtu457eC2C19e56403e8fE1B311B206Cf11"
    API_BASE = "https://maas-api.cn-huabei-1.xf-yun.com/v1"
    NARRATIVE_FRAMEWORKS = {
        "科学目标": {"叙述框架": ["执行系统", "执行系统能力"]},
        "能力目标": {"叙述框架": ["执行系统", "执行系统能力"]},
        "技术目标": {"叙述框架": ["执行系统", "执行系统能力"]},
        "工程目标": {"叙述框架": ["执行系统", "触发时间", "执行系统能力"]},
        "能力需求": {"叙述框架": ["执行系统", "任务阶段", "触发时间", "前置条件", "介词", "执行系统能力", "执行系统能力度量", "约束"]},
        "系统需求": {"叙述框架": ["执行系统", "前置条件", "介词", "执行系统能力"]},
        "进度要求": {"叙述框架": ["执行系统", "任务阶段"]},
        "功能要求": {"叙述框架": ["执行系统", "任务阶段", "触发时间", "前置条件", "介词", "使能系统", "使能项", "执行系统能力", "执行系统能力度量", "约束"]},
        "性能要求": {"叙述框架": ["执行系统", "任务阶段", "触发时间", "前置条件", "介词", "执行系统能力", "执行系统能力度量", "约束"]},
        "接口要求": {"叙述框架": ["执行系统", "前置条件", "介词", "执行系统能力度量", "约束"]},
        "可靠性要求": {"叙述框架": ["触发时间", "执行系统能力度量", "约束"]},
        "环境要求": {"叙述框架": ["执行系统", "前置条件", "介词", "执行系统能力度量", "约束"]}
    }
    SPLIT_THRESHOLD = 500
    OUTPUT_DIR_NAME = "数传综合管理单元测试"