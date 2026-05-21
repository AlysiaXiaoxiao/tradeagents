from pydantic import BaseModel
from typing import List, Dict
import yaml
import random
from pathlib import Path
import names

class Persona(BaseModel):
    name: str
    role: str
    persona: str
    objectives: List[str]
    trader_type: List[str]
    communication_style: str
    routines: List[str]
    skills: List[str]

def generate_persona() -> Persona:
    # Gender and Name
    gender_option = random.choice([
        ("男性", "male"),
        ("女性", "female"),
        ("非二元性别", None),
    ])
    gender, name_gender = gender_option
    name = names.get_full_name(gender=name_gender) if name_gender else names.get_full_name()

    # Pronouns with verb forms
    if gender == "男性":
        pronouns = {
            "subject": "he",
            "object": "him",
            "possessive": "his",
            "be": "is",
            "has": "has"
        }
    elif gender == "女性":
        pronouns = {
            "subject": "she",
            "object": "her",
            "possessive": "her",
            "be": "is",
            "has": "has"
        }
    else:  # Non-binary
        pronouns = {
            "subject": "they",
            "object": "them",
            "possessive": "their",
            "be": "are",
            "has": "have"
        }

    # Capitalize pronouns for sentence beginnings
    pronouns_cap = {
        k: v.capitalize() if k not in ["be", "has"] else v
        for k, v in pronouns.items()
    }

    # Role
    role = random.choice(["Buyer", "Seller"])

    # Occupation Mapping with Routines and Skills
    occupation_data = {
        '医生': {
            'education_levels': ["硕士", "博士"],
            'income_brackets': ["高"],
            'routines': ['查看患者病历', '进行手术', '参加医学会议', '接诊患者', '监督医疗团队'],
            'skills': ['医学诊断', '手术技能', '患者护理', '医学研究', '团队管理']
        },
        '工程师': {
            'education_levels': ["本科", "硕士", "博士"],
            'income_brackets': ["中", "高"],
            'routines': ['设计系统', '编写代码', '参加团队会议', '调试软件', '审查代码'],
            'skills': ['编程', '系统设计', '问题解决', '软件开发', '代码优化']
        },
        '教师': {
            'education_levels': ["本科", "硕士"],
            'income_brackets': ["低", "中"],
            'routines': ['准备教案', '授课', '批改作业', '会见家长', '参加工作坊'],
            'skills': ['教学', '课程开发', '课堂管理', '沟通', '评估']
        },
        '艺术家': {
            'education_levels': ["高中", "本科"],
            'income_brackets': ["低", "中"],
            'routines': ['创作艺术作品', '参加展览', '推广作品', '与其他艺术家合作', '研究新技法'],
            'skills': ['创造力', '艺术技能', '市场推广', '人脉拓展', '批判性思维']
        },
        '技工': {
            'education_levels': ["高中", "专科"],
            'income_brackets': ["低", "中"],
            'routines': ['检查车辆', '维修发动机', '订购零件', '维护设备', '提供客户服务'],
            'skills': ['机械知识', '问题解决', '技术技能', '客户服务', '注重细节']
        },
        '科学家': {
            'education_levels': ["硕士", "博士"],
            'income_brackets': ["中", "高"],
            'routines': ['进行实验', '分析数据', '发表论文', '参加会议', '与同行合作'],
            'skills': ['研究', '数据分析', '科学写作', '批判性思维', '协作']
        },
        '护士': {
            'education_levels': ["专科", "本科"],
            'income_brackets': ["低", "中"],
            'routines': ['监测患者健康', '给药', '更新记录', '协助医生', '教育患者'],
            'skills': ['患者护理', '医学知识', '同理心', '注重细节', '沟通']
        },
        '律师': {
            'education_levels': ["硕士", "博士"],
            'income_brackets': ["高"],
            'routines': ['会见客户', '准备法律文件', '出庭代理', '研究判例', '谈判和解'],
            'skills': ['法律知识', '谈判', '分析思维', '公开演讲', '写作']
        },
        '销售人员': {
            'education_levels': ["高中", "专科", "本科"],
            'income_brackets': ["低", "中"],
            'routines': ['联系潜在客户', '展示产品', '谈判交易', '跟进客户', '完成销售目标'],
            'skills': ['沟通', '说服', '谈判', '客户服务', '时间管理']
        },
        '创业者': {
            'education_levels': ["高中", "本科", "硕士"],
            'income_brackets': ["中", "高"],
            'routines': ['制定商业策略', '会见投资人', '管理团队', '监督运营', '分析市场趋势'],
            'skills': ['领导力', '战略规划', '风险管理', '人脉拓展', '金融素养']
        }
    }

    # Select occupation and corresponding data
    occupation = random.choice(list(occupation_data.keys()))
    occupation_info = occupation_data[occupation]
    education_level = random.choice(occupation_info['education_levels'])
    income_bracket = random.choice(occupation_info['income_brackets'])

    # Determine minimum age based on education level
    def get_min_age_for_education(education_level):
        education_age = {
            "高中": 18,
            "专科": 20,
            "本科": 22,
            "硕士": 24,
            "博士": 27
        }
        return education_age.get(education_level, 18)

    min_age = get_min_age_for_education(education_level)
    age = random.randint(min_age, 100)

    # Investment Experience and Risk Appetite
    investment_experience = random.choice(['新手', '中级', '专家'])
    risk_appetite = random.choice(['保守', '适中', '激进'])

    # Demographic Characteristics
    demographic_characteristics = {
        "age": age,
        "gender": gender,
        "education_level": education_level,
        "occupation": occupation,
        "income_bracket": income_bracket,
        "geographic_location": random.choice(["城市", "郊区", "乡村"])
    }

    # Economic Attributes
    economic_attributes = {
        "spending_habits": random.choice(["节俭", "适中", "奢侈"]),
        "saving_preferences": random.choice(["低", "中", "高"]),
        "risk_tolerance": round(random.uniform(0.0, 1.0), 2),
        "investment_experience": investment_experience
    }

    # Personality Traits
    personality_traits = {
        "decision_making_style": random.choice(["理性", "情绪化", "冲动", "协作型"]),
        "openness": round(random.uniform(0.0, 1.0), 2),
        "conscientiousness": round(random.uniform(0.0, 1.0), 2),
        "extraversion": round(random.uniform(0.0, 1.0), 2),
        "agreeableness": round(random.uniform(0.0, 1.0), 2),
        "neuroticism": round(random.uniform(0.0, 1.0), 2)
    }

    # Hobbies and Interests
    hobbies_list = ["阅读", "运动", "烹饪", "旅行", "音乐", "艺术", "园艺", "摄影", "科技"]
    hobbies_and_interests = random.sample(hobbies_list, k=3)
    hobbies_and_interests_str = ", ".join(hobbies_and_interests)

    # Dynamic Attributes
    recent_life_events_list = random.sample(
        ["获得晋升", "搬到新城市", "开始新爱好", "毕业", "退休"],
        k=2
    )
    dynamic_attributes = {
        "current_mood": random.choice(["开心", "难过", "平静", "兴奋"]),
        "recent_life_events": recent_life_events_list
    }
    recent_life_events_str = ", ".join(dynamic_attributes["recent_life_events"])

    # Financial Objectives
    short_term_goals_list = random.sample(
        ["建立应急基金", "偿还信用卡债务", "为度假储蓄"],
        k=2
    )
    long_term_goals_list = random.sample(
        ["为退休储蓄", "买房", "创业"],
        k=2
    )
    investment_preferences_list = random.sample(
        ["股票", "债券", "房地产", "加密货币", "大宗商品"],
        k=3
    )
    financial_objectives = {
        "short_term_goals": short_term_goals_list,
        "long_term_goals": long_term_goals_list,
        "risk_appetite": risk_appetite,
        "investment_preferences": investment_preferences_list
    }
    short_term_goals_str = ", ".join(financial_objectives["short_term_goals"])
    long_term_goals_str = ", ".join(financial_objectives["long_term_goals"])
    investment_preferences_str = ", ".join(financial_objectives["investment_preferences"])

    # Routines and Skills
    routines_list = occupation_info['routines']
    skills_list = occupation_info['skills']

    routines = random.sample(routines_list, k=3) if len(routines_list) >= 3 else routines_list
    skills = random.sample(skills_list, k=3) if len(skills_list) >= 3 else skills_list

    routines_str = ", ".join(routines)
    skills_str = ", ".join(skills)

    # Communication Style
    decision_making_to_communication = {
        "理性": ["直接", "正式"],
        "情绪化": ["有说服力", "友好", "非正式"],
        "冲动": ["非正式", "直接"],
        "协作型": ["友好", "有说服力"]
    }

    communication_styles = ["直接", "有说服力", "克制", "友好", "正式", "非正式"]
    decision_making_style = personality_traits["decision_making_style"]
    communication_style_options = decision_making_to_communication.get(decision_making_style, communication_styles)
    communication_style = random.choice(communication_style_options)

    # Read Persona Template as YAML and extract content under 'persona'
    with open('./trade_agents/agents/personas/persona_template.yaml', 'r') as file:
        template_yaml = yaml.safe_load(file)
    template_content = template_yaml.get('persona', '')

    # Format Persona Description
    persona_description = template_content.format(
        name=name,
        age=age,
        gender=gender,
        pronoun_subject=pronouns["subject"],
        pronoun_object=pronouns["object"],
        pronoun_possessive=pronouns["possessive"],
        pronoun_be=pronouns["be"],
        has=pronouns["has"],
        pronoun_subject_cap=pronouns_cap["subject"],
        pronoun_object_cap=pronouns_cap["object"],
        pronoun_possessive_cap=pronouns_cap["possessive"],
        education_level=education_level,
        occupation=occupation,
        income_bracket=income_bracket,
        geographic_location=demographic_characteristics["geographic_location"],
        spending_habits=economic_attributes["spending_habits"],
        saving_preferences=economic_attributes["saving_preferences"],
        risk_tolerance=economic_attributes["risk_tolerance"],
        investment_experience=investment_experience,
        decision_making_style=personality_traits["decision_making_style"],
        openness=personality_traits["openness"],
        conscientiousness=personality_traits["conscientiousness"],
        extraversion=personality_traits["extraversion"],
        agreeableness=personality_traits["agreeableness"],
        neuroticism=personality_traits["neuroticism"],
        hobbies_and_interests=hobbies_and_interests_str,
        current_mood=dynamic_attributes["current_mood"],
        recent_life_events=recent_life_events_str,
        short_term_goals=short_term_goals_str,
        long_term_goals=long_term_goals_str,
        risk_appetite=risk_appetite,
        investment_preferences=investment_preferences_str,
        communication_style=communication_style,
        routines=routines_str,
        skills=skills_str
    )

    # Objectives
    objectives = [
        f"以有利价格{'购买' if role == 'Buyer' else '出售'}商品",
        f"你的目标是{'最大化效用' if role == 'Buyer' else '最大化利润'}"
    ]

    # Trader Type
    trader_type = [investment_experience, risk_appetite, personality_traits["decision_making_style"]]

    return Persona(
        name=name,
        role=role,
        persona=persona_description,
        objectives=objectives,
        trader_type=trader_type,
        communication_style=communication_style,
        routines=routines,
        skills=skills
    )

def save_persona_to_file(persona: Persona, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    # Prepare the persona dictionary
    persona_dict = {
        'name': persona.name,
        'role': persona.role,
        'persona': persona.persona,
        'objectives': persona.objectives,
        'trader_type': persona.trader_type,
        'communication_style': persona.communication_style,
        'routines': persona.routines,
        'skills': persona.skills
    }

    # Custom YAML dumper to force literal block style for the persona field
    class LiteralDumper(yaml.SafeDumper):
        def represent_scalar(self, tag, value, style=None):
            if tag == 'tag:yaml.org,2002:str' and '\n' in value:
                style = '|'
            return super().represent_scalar(tag, value, style)

    with open(output_dir / f"{persona.name.replace(' ', '_')}.yaml", "w") as f:
        yaml.dump(
            persona_dict,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=1000,
            indent=2,
            Dumper=LiteralDumper
        )

def generate_and_save_personas(num_personas: int, output_dir: Path):
    for _ in range(num_personas):
        persona = generate_persona()
        save_persona_to_file(persona, output_dir)

if __name__ == "__main__":
    output_dir = Path("./trade_agents/agents/personas/generated_personas")
    generate_and_save_personas(10, output_dir)
    print(f"Generated 10 personas in {output_dir}")
