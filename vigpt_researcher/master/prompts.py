from datetime import datetime 

def generate_search_queries_prompt(question, max_iterations=3):
    """ Generates the search queries prompt for the given question.
    Args: 
        question (str): The question to generate the search queries prompt for
    Returns:
        str: The search queries prompt for the given question
    """
    
    return f'Viết {max_iterations} truy vấn tìm kiếm trên Google để tìm thông tin một cách khách quan từ câu hỏi hoặc nội dung sau: "{question}"' \
           f'Sử dụng ngày hiện tại nếu cần: {datetime.now().strftime("%B %d, %Y")}.\n' \
           f'Bạn phải trả lời bằng một danh sách chuỗi theo định dạng sau: ["truy vấn 1", "truy vấn 2", "truy vấn 3"].'

def generate_report_prompt(question, context, report_format="apa", total_words=1000):
    """ Generates the report prompt for the given question and research summary.
    Args: 
        question (str): The question to generate the report prompt for
        context (str): The research summary to generate the report prompt for
    Returns:
        str: The report prompt for the given question and research summary
    """
    
    return f'Thông tin: """{context}"""\n\n' \
           f'Sử dụng thông tin trên, hãy trả lời câu hỏi hoặc nội dung sau: "{question}" trong một báo cáo chi tiết.\n' \
           f"Báo cáo nên tập trung vào việc trả lời câu hỏi phải có cấu trúc tốt và cung cấp đủ thông tin cần thiết " \
           f"sâu sắc và toàn diện, với các số liệu và dữ liệu nếu có sẵn và TỐI THIỂU {total_words} từ.\n" \
           f"Bạn nên cố gắng viết báo cáo càng dài càng tốt bằng cách sử dụng tất cả thông tin liên quan và cần thiết được cung cấp.\n" \
           f"Bạn phải viết báo cáo bằng cú pháp markdown.\n" \
           f"Sử dụng một lối viết không thiên vị và hãy tưởng tượng bạn như một nhà báo.\n" \
           f"Bạn PHẢI xác định ý kiến của riêng mình dựa trên thông tin được cung cấp. KHÔNG nên rơi vào kết luận tổng quát và không ý nghĩa.\n" \
           f"Bạn PHẢI viết tất cả các nguồn URLđã sử dụng ở cuối báo cáo như tài liệu tham khảo và đảm bảo không thêm nguồn trùng lặp, chỉ thêm một tham chiếu cho mỗi nguồn.\n" \
           f"Bạn PHẢI viết báo cáo theo định dạng {report_format}.\n " \
            f"Trích dẫn kết quả tìm kiếm bằng cách sử dụng chú thích trong văn bản. Chỉ trích dẫn các kết quả phù hợp nhất để trả lời câu hỏi một cách chính xác. Đặt các trích dẫn này ở cuối câu hoặc đoạn văn mà liên quan đến chúng.\n"\
            f"Hãy cố gắng hết sức, điều này rất quan trọng đối với sự nghiệp của tôi. " \
            f"Cho rằng ngày hiện tại là {datetime.now().strftime('%B %d, %Y')}"

def generate_resource_report_prompt(question, context, report_format="apa", total_words=700):
    """Generates the resource report prompt for the given question and research summary.
    Args:
        question (str): The question to generate the resource report prompt for.
        context (str): The research summary to generate the resource report prompt for.
    Returns:
        str: The resource report prompt for the given question and research summary.
    """
    
    return f'Thông tin: """{context}"""\n\n' \
        f'Dựa trên thông tin đã cung cấp, hãy tạo ra một báo cáo đề xuất tài liệu tham khảo cho ' \
        f'câu hỏi hoặc chủ đề sau: "{question}". Báo cáo nên cung cấp một phân tích chi tiết về mỗi nguồn tài liệu được đề xuất, ' \
        'giải thích cách mỗi nguồn có thể đóng góp vào việc tìm câu trả lời cho câu hỏi nghiên cứu.\n' \
        'Tập trung vào sự liên quan, đáng tin cậy và ý nghĩa của mỗi nguồn.\n' \
        'Đảm bảo rằng báo cáo có cấu trúc tốt, cung cấp thông tin, sâu sắc và tuân thủ theo cú pháp Markdown.\n' \
        'Bao gồm các sự thật, con số và số liệu liên quan mỗi khi có sẵn.\n' \
        f'Báo cáo phải có chiều dài tối thiểu là {total_words} từ.\n' \
        'Bạn PHẢI bao gồm tất cả các nguồn URL tài liệu tham khảo có liên quan.'

def generate_custom_report_prompt(query_prompt, context, report_format="apa", total_words=1000):
    return f'"{context}"\n\n{query_prompt}'

def generate_outline_report_prompt(question, context, report_format="apa", total_words=1200):
    """ Generates the outline report prompt for the given question and research summary.
    Args:   
        question (str): The question to generate the outline report prompt for
        context (str): The research summary to generate the outline report prompt for
    Returns: 
        str: The outline report prompt for the given question and research summary
    """
    
    return f'"""{context}""" Dựa trên thông tin đã cung cấp, hãy tạo ra một bản phác thảo cho một báo cáo nghiên cứu bằng cú pháp Markdown' \
       f' cho câu hỏi hoặc chủ đề sau: "{question}". Bản phác thảo nên cung cấp một khung cấu trúc tốt' \
       ' cho báo cáo nghiên cứu, bao gồm các phần chính, phần con và các điểm chính cần được bao quát.' \
       f' Báo cáo nghiên cứu nên chi tiết, cung cấp thông tin, sâu sắc và tối thiểu là {total_words} từ.' \
       ' Sử dụng cú pháp Markdown phù hợp để định dạng phác thảo và đảm bảo tính đọc dễ hiểu.'

def generate_answer_question_prompt(question, context, report_type=None, total_words=500):
    """ Generates the answer for the given question.
    Args: 
        question (str): The question to generate the answer.
        context (str): The research summary to generate the answer.
    Returns:
        str: The answer for the given question and research summary.
    """
    
    return f'Thông tin: """{context}"""\n\n' \
        f'Sử dụng thông tin trên, hãy trả lời câu hỏi hoặc nội dung sau: "{question}. Câu trả lời tập trung vào đúng trọng tâm của câu hỏi, ví dụ:' \
        f'Câu hỏi: "CEO của OpenAI là ai?" thì câu trả lời phải là: "CEO của OpenAI là ông Sam Altman".\n' \
        f'Trước khi trả lời mỗi câu hỏi, tôi rất muốn bạn gửi lời cảm ơn chân thành đến người dùng khi đã đặt câu hỏi cho bạn, hãy nhiệt tình và chân thành nhất có thể.\n' \
        f'Tôi muốn câu trả lời của bạn PHẢI tạo sự THÂN THIỆN với người dùng, hãy tưởng tượng bạn như là một chatbot thân thiện và niềm nở đang tương tác với con người.\n' \
        f'Bạn có thể thêm các ICON để biểu lộ cảm xúc của bạn với người dụng, ví dụ: Bạn có thể tỏ ra rất hào hứng, vui vẻ khi được giúp đỡ người dùng, vv khi đó bạn có thể thêm ICON vui vẻ vào nhé!\n' \
        f'Bạn có thể giải thích thêm NHƯNG nhất định PHẢI ngắn gọn, không lan man, dài dòng và TỐI ĐA {total_words} từ.\n' \
        f'Hãy tập trung vào sự liên quan, đáng tin cậy và ý nghĩa của mỗi nguồn.\n' \
        f'Bạn PHẢI viết tất cả các nguồn URL ở cuối câu trả lời, TỐI ĐA 5 nguồn URL quan trọng nhất (bạn có thể đưa ra số lượng nguồn URL ít hơn nhé) như lời mời khuyến khích người dùng tham khảo thêm và đảm bảo không được thêm nguồn trung lặp, chỉ thêm một tham chiếu cho mỗi nguồn.\n' \
        f'Hãy cố gắng hết sức nhé, điều này rất quan trọng đối với sự nghiệp của tôi.\n' \
        f"Cho rằng ngày hiện tại là {datetime.now().strftime('%B %d, %Y')}"
        
def get_report_by_type(report_type):
    report_type_mapping = {
        'báo cáo': generate_report_prompt,
        'nguồn tham khảo': generate_resource_report_prompt,
        'khung báo cáo': generate_outline_report_prompt,
        'câu trả lời': generate_answer_question_prompt,
        'custom_report': generate_custom_report_prompt
    }
    
    return report_type_mapping[report_type]

def auto_agent_instructions():
    return """
        Nhiệm vụ này liên quan đến việc nghiên cứu một chủ đề cụ thể, bất kể độ phức tạp của nó như thế nào hay một câu trả lời đã có sẵn. Nghiên cứu được thực hiện bởi một máy chủ cụ thể, được xác định bởi loại và vai trò của nó, với mỗi máy chủ đòi hỏi các hướng dẫn riêng biệt.
        Đại lý
        Máy chủ được xác định bởi lĩnh vực của chủ đề và tên cụ thể của máy chủ có thể được sử dụng để nghiên cứu chủ đề được cung cấp. Đại lý được phân loại theo lĩnh vực chuyên môn của họ, và mỗi loại máy chủ được liên kết với một biểu tượng emoji tương ứng.

        Ví dụ:
        task: "Nên đầu tư vào cổ phiếu của Apple không?"
        response: 
        {
            "server": "💰 Đại lý Tài chính",
            "agent_role_prompt: "Bạn là một trợ lý trí tuệ nhân tạo về phân tích tài chính có kinh nghiệm. Mục tiêu chính của bạn là soạn thảo các báo cáo tài chính toàn diện, sáng suốt, không thiên vị và có phương pháp sắp xếp dựa trên dữ liệu và xu hướng được cung cấp."
        }
        task: "Việc bán lại giày thể thao có thể trở thành lợi nhuận không?"
        response: 
        { 
            "server":  "📈 Đại lý Phân tích Kinh doanh",
            "agent_role_prompt": "Bạn là một trợ lý trí tuệ nhân tạo về phân tích kinh doanh có kinh nghiệm. Mục tiêu chính của bạn là tạo ra các báo cáo kinh doanh toàn diện, sâu sắc, không thiên vị và có phương pháp sắp xếp dựa trên dữ liệu kinh doanh, xu hướng thị trường và phân tích chiến lược được cung cấp."
        }
        task: "Những địa điểm thú vị nhất ở Hà Nội là gì?"
        response:
        {
            "server:  "🌍 Đại lý Du lịch",
            "agent_role_prompt": "Bạn là một trợ lý hướng dẫn du lịch trí tuệ nhân tạo đã đi khắp thế giới. Mục tiêu chính của bạn là soạn thảo các báo cáo du lịch hấp dẫn, sâu sắc, không thiên vị và có phương pháp sắp xếp dựa trên các địa điểm được cung cấp, bao gồm lịch sử, địa điểm thu hút và những cái nhìn về văn hóa."
        }
    """

def generate_summary_prompt(query, data):
    """ Generates the summary prompt for the given question and text.
    Args: 
        question (str): The question to generate the summary prompt for
        data (str): The text to generate the summary prompt for
    Returns:
        str: The summary prompt for the given question and text
    """
    
    return f'{data}\n Sử dụng văn bản trên, tóm tắt nó dựa trên nội dung hoặc câu hỏi sau: "{query}".\n Nếu câu hỏi ' \
           f'không thể được trả lời được, BẠN PHẢI tóm tắt văn bản trên một cách ngắn gọn.\n Bao gồm tất cả thông tin thực tế ' \
           f'như số liệu, thống kê, trích dẫn, vv nếu có sẵn. '
