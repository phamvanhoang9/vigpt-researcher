import sys
sys.path.append('..')

from vigpt_researcher import VIGPTResearcher
import asyncio 
import re


async def get_report(query: str, report_type: str) -> str:
    researcher = VIGPTResearcher(query, report_type)
    report = await researcher.run()
    
    return report

if __name__ == "__main__":
    query = "Thông tin về ngành Điện tử - Viễn thông hệ Đại trà của Đại học Bách khoa Hà Nội được không?"
    report_type = "research_report"
    
    report = asyncio.run(get_report(query, report_type))
    
    with open("evaluation/hypos.txt", "w", encoding="utf-8") as file:
        file.write(report) 
    print("Hypothesis saved to evaluation/hypos.txt")
        
    urls = re.findall(r'(https?://\S+)', report)
    with open("evaluation/refs.txt", "w") as file:
        for url in urls:
            file.write(url + '\n')        
    print("References saved to evaluation/refs.txt")
    print("\n\n\n")
    
    print(report)
