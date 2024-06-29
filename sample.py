
from vigpt_researcher import VIGPTResearcher
import asyncio 

# Define global constants at the top
QUERY = "Tình hình phát triển ngành công nghiệp bán dẫn ở Việt Nam trong 5 năm tới như thế nào?"
REPORT_TYPE = "báo cáo"

async def fetch_report(query, report_type):
    """ 
    Fetch a research report based on the provided query and report type.
    """
    researcher = VIGPTResearcher(query=query, report_type=report_type, config_path=None)
    report = await researcher.run()
    return report

async def generate_research_report():
    """ 
    This is a sample script that executes an async main function to run a research report
    """
    report = await fetch_report(QUERY, REPORT_TYPE)
    print(report)
    
if __name__ == "__main__":
    asyncio.run(generate_research_report())


# from vigpt_researcher import VIGPTResearcher
# import asyncio 

# async def get_report(query: str, report_type: str, sources: set|None) -> str:
#     researcher = VIGPTResearcher(query=query, report_type=report_type, source_urls=sources)
#     report = await researcher.run()
#     return report

# if __name__ == "__main__":
#     query = "Những tiến bộ mới nhất trong AI là gì?"
#     report_type = "báo cáo"
#     sources = ["https://en.wikipedia.org/wiki/Artificial_intelligence", "https://www.ibm.com/watson/ai"]
    
#     report = asyncio.run(get_report(query, report_type, sources))
#     print(report)
    
    