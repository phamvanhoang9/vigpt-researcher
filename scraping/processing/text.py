"""Text processing functions"""
import urllib # for encoding file path
from typing import Dict, Generator, Optional

from selenium.webdriver.remote.webdriver import WebDriver

# import sys 
# sys.path.append('..')

from vigpt_researcher.config import Config
from vigpt_researcher.utils.llm import create_chat_completion
import os
from md2pdf.core import md2pdf # convert markdown to pdf


def split_text(text: str, max_length: int = 8192) -> Generator[str, None, None]:
    """Split text into chunks of a maximum length

    Args:
        text (str): The text to split
        max_length (int, optional): The maximum length of each chunk. Defaults to 8192.

    Yields:
        str: The next chunk of text

    Raises:
        ValueError: If the text is longer than the maximum length
    """
    paragraphs = text.split("\n") # split text into paragraphs
    current_length = 0 # current length of the chunk
    current_chunk = [] # current chunk of text

    for paragraph in paragraphs: # iterate through paragraphs
        if current_length + len(paragraph) + 1 <= max_length: # if the current length + length of the paragraph + 1 is less than the max length
            current_chunk.append(paragraph) # append the paragraph to the current chunk
            current_length += len(paragraph) + 1 # update the current length
        else:
            yield "\n".join(current_chunk) # yield the current chunk as a string in order to join the paragraphs
            current_chunk = [paragraph] # set the current chunk to the paragraph
            current_length = len(paragraph) + 1 # set the current length to the length of the paragraph + 1

    if current_chunk: # if there is any remaining text in the current chunk after the loop
        yield "\n".join(current_chunk)


def summarize_text(
    fast_llm_model: str, summary_token_limit: int, llm_provider: str, url: str, text: str, question: str, driver: Optional[WebDriver] = None
) -> str:
    """Summarize text using the OpenAI API

    Args:
        fast_llm_model (str): The fast LLM model e.g gpt3.5-turbo-16k
        summary_token_limit (int): The summary token limit
        llm_provider (str): The llm provider
        url (str): The url of the text
        text (str): The text to summarize
        question (str): The question to ask the model
        driver (WebDriver): The webdriver to use to scroll the page

    Returns:
        str: The summary of the text
    """
    if not text:
        return "Error: No text to summarize"

    summaries = []
    chunks = list(split_text(text))
    scroll_ratio = 1 / len(chunks) # why 1/len(chunks) ??  # scroll ratio is the ratio of the page to scroll to for each chunk of text to summarize 

    print(f"Summarizing url: {url} with total chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        if driver:
            scroll_to_percentage(driver, scroll_ratio * i)

        #memory_to_add = f"Source: {url}\n" f"Raw content part#{i + 1}: {chunk}"

        #MEMORY.add_documents([Document(page_content=memory_to_add)])

        messages = [create_message(chunk, question)]

        summary = create_chat_completion(
            model=fast_llm_model,
            messages=messages,
            max_tokens=summary_token_limit,
            llm_provider=llm_provider
        )
        summaries.append(summary)
        #memory_to_add = f"Source: {url}\n" f"Content summary part#{i + 1}: {summary}"

        #MEMORY.add_documents([Document(page_content=memory_to_add)])

    combined_summary = "\n".join(summaries)
    messages = [create_message(combined_summary, question)]

    final_summary = create_chat_completion(
        model=fast_llm_model,
        messages=messages,
        max_tokens=summary_token_limit,
        llm_provider=llm_provider,
    )
    print("Final summary length: ", len(combined_summary))
    print(final_summary)

    return final_summary


def scroll_to_percentage(driver: WebDriver, ratio: float) -> None:
    """Scroll to a percentage of the page

    Args:
        driver (WebDriver): The webdriver to use
        ratio (float): The percentage to scroll to

    Raises:
        ValueError: If the ratio is not between 0 and 1
    """
    if ratio < 0 or ratio > 1:
        raise ValueError("Percentage should be between 0 and 1")
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {ratio});")


def create_message(chunk: str, question: str) -> Dict[str, str]:
    """Create a message for the chat completion

    Args:
        chunk (str): The chunk of text to summarize
        question (str): The question to answer

    Returns:
        Dict[str, str]: The message to send to the chat completion
    """
    return {
        "role": "user",
        "content": f'"""{chunk}"""\n'
        f'Sử dụng văn bản trên, tóm tắt nó dựa trên công việc hoặc truy vấn sau: "{question}".\n'
        f'Nếu truy vấn không thể được trả lời bằng văn bản, BẠN PHẢI tóm tắt văn bản ngắn gọn.\n'
        f'Bao gồm tất cả thông tin thực tế như số liệu, thống kê, trích dẫn, v.v. nếu có.',
    }

def write_to_file(filename: str, text: str) -> None:
    """Write text to a file

    Args:
        text (str): The text to write
        filename (str): The filename to write to
    """
    with open(filename, "w") as file:
        file.write(text)

async def write_md_to_pdf(task: str, path: str, text: str) -> None:
    file_path = f"{path}/{task}"
    write_to_file(f"{file_path}.md", text)
    md_to_pdf(f"{file_path}.md", f"{file_path}.pdf")
    print(f"{task} written to {file_path}.pdf")

    encoded_file_path = urllib.parse.quote(f"{file_path}.pdf")

    return encoded_file_path

def read_txt_files(directory):
    all_text = ''

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r') as file:
                all_text += file.read() + '\n'

    return all_text


def md_to_pdf(input_file, output_file):
    md2pdf(output_file,
           md_content=None,
           md_file_path=input_file,
           css_file_path=None,
           base_url=None)
