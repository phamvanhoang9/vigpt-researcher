import sys
sys.path.append('..')

from vigpt_researcher import VIGPTResearcher
import asyncio 
import re
from termcolor import colored
import time


async def get_report(query: str, report_type: str) -> str:
    researcher = VIGPTResearcher(query, report_type)
    report = await researcher.run()
    
    return report

def save_report(report, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(report.strip()) # remove leading and trailing whitespaces

if __name__ == "__main__":
    
    query = ["Cơ hội việc làm cho sinh viên ngành Điện tử - Viễn thông của Đại học Bách khoa Hà Nội sau khi tốt nghiệp",
             "Cách ôn luyện cho kỳ thi tư duy ở Đại học Bách Khoa Hà Nội",
             "Trình bày cơ chế hoạt động của mô hình GPT-4",
             "CEO Sam Altman đã có những cống hiến gì cho OpenAI?",
             "Tôi có nên đầu tư bất động sản ở Việt Nam khi đang là sinh viên không?",
             "Bảng xếp hạng 10 tỷ phú giàu nhất thế giới ở thời điểm hiện tại",
             "Cuộc đời của Steve Jobs như thế nào?",
             "Thời tiết ở Hà Nội trong vài ngày tới",
             "Bạn có thể cho tôi một đoạn thơ ngắn để tỏ tình crush được không?",
             "Cách viết một bài báo khoa học chuẩn IEEE",
             "Việc dành học bổng ở Đại học Bách Khoa Hà Nội có khó không?",
            ]
    
    report_type = ["báo cáo", "nguồn tham khảo", "khung báo cáo", "câu trả lời"]
    
    start_time = time.time()
    report = asyncio.run(get_report(query[8], report_type[3]))
    end_time = time.time()
    print(colored(f"\nTổng thời gian xử lý: {(end_time - start_time):.3f} giây.\n\n", "cyan"))
    
    # report_without_references = report.split("## Tài Liệu Tham Khảo")[0]
    # save_report(report_without_references, "evaluation/hypos.txt")
    # print("-"*80)
    # print(colored("Báo cáo đã được lưu vào thư mục evaluation/hypos.txt", "blue"))
    # print("-"*80)  
    # urls = re.findall(r'(https?://\S+)', report)
    # with open("evaluation/refs.txt", "w") as file:
    #     for url in urls:
    #         file.write(url + '\n')    
    # print(colored("Danh sách các tài liệu tham khảo đã được lưu vào thư mục evaluation/refs.txt", "green"))    
    # print("-"*80)
    # print("\n")
    
    print(report)
