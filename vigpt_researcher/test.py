import sys
sys.path.append('..')

from vigpt_researcher import VIGPTResearcher
import asyncio 


async def get_report(query: str, report_type: str) -> str:
    researcher = VIGPTResearcher(query, report_type)
    report = await researcher.run()
    
    return report

if __name__ == "__main__":
    query = "Bạn có thể cho tôi biết thông tin về ngành Điện tử - Viễn thông của Đại học Bách khoa Hà Nội được không?"
    report_type = "research_report"
    
    report = asyncio.run(get_report(query, report_type))
    print(report)
    