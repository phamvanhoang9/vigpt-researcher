# import sys
# sys.path.append('..')

import time 
from vigpt_researcher.config import Config 
# from ..config import Config
from vigpt_researcher.master.functions import *
# from ..master.functions import *
from vigpt_researcher.context.compression import ContextCompressor
from vigpt_researcher.memory import Memory 


class VIGPTResearcher:
    """
    VIGPT Researcher
    """
    def __init__(self, query, report_type="research_report", source_urls=None, config_path=None, websocket=None):
        """
        Initialize the VIGPT Researcher class.
        Args:
            query:
            report_type:
            config_path:
            websocket:
        """
        self.query = query
        self.agent = None
        self.role = None
        self.report_type = report_type
        self.websocket = websocket
        self.cfg = Config(config_path)
        self.retriever = get_retriever(self.cfg.retriever)
        self.context = []
        self.source_urls = source_urls
        self.memory = Memory()
        self.visited_urls = set()

    async def run(self):
        """
        Runs the VIGPT Researcher
        Returns:
            Report
        """
        print(f"🔎 Đang tìm kiếm thông tin cho '{self.query}'...")
        # Generate Agent
        self.agent, self.role = await choose_agent(self.query, self.cfg)
        await stream_output("logs", self.agent, self.websocket)

        # If specified, the researcher will use the given urls as the context for the research.
        if self.source_urls:
            self.context = await self.get_context_by_urls(self.source_urls)
        else:
            self.context = await self.get_context_by_search(self.query)

        # Write Research Report
        if self.report_type == "custom_report":
            self.role = self.cfg.agent_role if self.cfg.agent_role else self.role
        await stream_output("logs", f"✍️ Đang viết {self.report_type} cho nhiệm vụ tìm kiếm thông tin: {self.query}...", self.websocket)
        report = await generate_report(query=self.query, context=self.context,
                                       agent_role_prompt=self.role, report_type=self.report_type,
                                       websocket=self.websocket, cfg=self.cfg)
        time.sleep(2) # Sleep for 2 seconds in order to prevent the report from being cut off
        return report

    async def get_context_by_urls(self, urls):
        """
            Scrapes and compresses the context from the given urls
        """
        new_search_urls = await self.get_new_urls(urls)
        await stream_output("logs",
                            f"🧠 Tôi sẽ tiến hành tìm kiếm thông tin dựa vào các url sau: {new_search_urls}...",
                            self.websocket)
        scraped_sites = scrape_urls(new_search_urls, self.cfg)
        return await self.get_similar_content_by_query(self.query, scraped_sites)

    async def get_context_by_search(self, query):
        """
           Generates the context for the research task by searching the query and scraping the results
        Returns:
            context: List of context
        """
        context = []
        # Generate Sub-Queries including original query
        sub_queries = await get_sub_queries(query, self.role, self.cfg) + [query]
        await stream_output("logs",
                            f"🧠 Tôi sẽ tiến hành tìm kiếm thông tin dựa vào các nội dung sau: {sub_queries}...",
                            self.websocket)

        # Run Sub-Queries
        for sub_query in sub_queries:
            await stream_output("logs", f"\n🔎 Đang tìm kiếm thông tin cho '{sub_query}'...", self.websocket)
            scraped_sites = await self.scrape_sites_by_query(sub_query)
            content = await self.get_similar_content_by_query(sub_query, scraped_sites)
            await stream_output("logs", f"📃 {content}", self.websocket)
            context.append(content)

        return context

    async def get_new_urls(self, url_set_input):
        """ Gets the new urls from the given url set.
        Args: url_set_input (set[str]): The url set to get the new urls from
        Returns: list[str]: The new urls from the given url set
        """

        new_urls = []
        for url in url_set_input:
            if url not in self.visited_urls:
                await stream_output("logs", f"✅ Đang thêm nguồn url để thực hiện tìm kiếm thông tin: {url}\n", self.websocket)

                self.visited_urls.add(url)
                new_urls.append(url)

        return new_urls

    async def scrape_sites_by_query(self, sub_query):
        """
        Runs a sub-query
        Args:
            sub_query:

        Returns:
            Summary
        """
        # Get Urls
        retriever = self.retriever(sub_query)
        search_results = retriever.search(max_results=self.cfg.max_search_results_per_query)
        new_search_urls = await self.get_new_urls([url.get("href") for url in search_results])

        # Scrape Urls
        await stream_output("logs", f"📝 Đang quét các url sau: {new_search_urls}...\n", self.websocket)
        await stream_output("logs", f"🤔 Đang tìm kiếm thông tin liên quan...\n", self.websocket)
        scraped_content_results = scrape_urls(new_search_urls, self.cfg)
        return scraped_content_results

    async def get_similar_content_by_query(self, query, pages):
        await stream_output("logs", f"📃 Đang lấy thông tin liên quan đến nội dung sau: {query}...", self.websocket)
        # Summarize Raw Data
        context_compressor = ContextCompressor(documents=pages, embeddings=self.memory.get_embeddings())
        # Run Tasks
        return context_compressor.get_context(query, max_results=8)
