import sys
sys.path.append('..')

from vigpt_researcher import VIGPTResearcher
import asyncio 
import re
from termcolor import colored
import time


async def get_report(query: str, report_type: str, source_urls: set|None) -> str:
    researcher = VIGPTResearcher(query, report_type, source_urls)
    report = await researcher.run()
    
    return report

def save_report(report, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(report.strip()) # remove leading and trailing whitespaces

if __name__ == "__main__":
    
    query = [ "Thời tiết ở Hà Nội trong 3 ngày tới như thế nào?",
             "Sự phát triển của chíp bán dẫn ở Việt Nam như thế nào?"
            ]
    
    query_eval = "Tổng quan về ngành Điện tử - Viễn thông của Đại học Bách Khoa Hà Nội"
    source_urls = set()
    source_urls = source_urls.add("https://ts.hust.edu.vn/training-cate/nganh-dao-tao-dai-hoc/dien-tu-va-vien-thong")
    
    report_type = ["báo cáo", "nguồn tham khảo", "khung báo cáo", "câu trả lời ngắn gọn"]
    
    start_time = time.time()
    report = asyncio.run(get_report(query[0], report_type[3], source_urls=None))
    end_time = time.time()
    print(colored(f"\nTổng thời gian xử lý: {(end_time - start_time):.3f} giây.\n\n", "cyan"))
    
    # report_without_references = report.split("## Tài liệu tham khảo")[0]
    # save_report(report_without_references, "evaluation/hypos/hypo5.txt")
    # print("-"*80)
    # print(colored("Báo cáo đã được lưu vào thư mục evaluation/hypos/hypo5.txt", "blue"))
    # print("-"*80)  
    # urls = re.findall(r'(https?://\S+)', report)
    # with open("evaluation/refs.txt", "w") as file:
    #     for url in urls:
    #         file.write(url + '\n')    
    # print(colored("Danh sách các tài liệu tham khảo đã được lưu vào thư mục evaluation/refs.txt", "green"))    
    # print("-"*80)
    # print("\n")
    
    print(report)
