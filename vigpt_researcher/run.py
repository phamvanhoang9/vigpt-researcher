import sys
sys.path.append('..')

from vigpt_researcher import VIGPTResearcher
import asyncio 
import re
from termcolor import colored


async def get_report(query: str, report_type: str) -> str:
    researcher = VIGPTResearcher(query, report_type)
    report = await researcher.run()
    
    return report

def save_report(report, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(report.strip()) # remove leading and trailing whitespaces

if __name__ == "__main__":
    query = "Cơ hội nghề nghiệp cho sinh viên ngành Điện tử - Viễn thông của Đại học Bách khoa Hà Nội sau khi tốt nghiệp"
    report_type = "research_report"
    
    report = asyncio.run(get_report(query, report_type))
    report_without_references = report.split("## Tài Liệu Tham Khảo")[0]
    
    save_report(report_without_references, "evaluation/hypos.txt")
    print("-"*80)
    print(colored("Báo cáo đã được lưu vào thư mục evaluation/hypos.txt", "blue"))
    print("-"*80)
        
    urls = re.findall(r'(https?://\S+)', report)
    with open("evaluation/refs.txt", "w") as file:
        for url in urls:
            file.write(url + '\n')    
    print(colored("Danh sách các tài liệu tham khảo đã được lưu vào thư mục evaluation/refs.txt", "green"))    
    print("-"*80)
    print("\n")
    
    print(report)
