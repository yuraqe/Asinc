import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
from aiohttp_socks import ChainProxyConnector
from aiohttp_retry import RetryClient, ExponentialRetry
from fake_useragent import UserAgent


class AsyncParser:
    def __init__(self, domain):
        self.domain = domain
        self.category_list = []
        self.pagen_list = []
        self._total_discount = 0


    @staticmethod
    def get_soup(url):
        resp = requests.get(url=url)
        return BeautifulSoup(resp.text, 'lxml')


    def get_urls_categories(self, soup):
        all_links = soup.find('div', class_='nav_menu').find_all('a')
        for cat in all_links:
            self.category_list.append(f"{self.domain}{cat['href']}")


    def get_urls_pages(self):
        for cat in self.category_list:
            resp = requests.get(url=cat)
            soup = BeautifulSoup(resp.text, 'lxml')
            for page in soup.find('div', class_='pagen').find_all('a'):
                self.pagen_list.append(f"{self.domain}{page['href']}")


    async def _detail_button(self, session, link):
        retry_options = ExponentialRetry(attempts=5)
        retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session,
                                   start_timeout=0.5)
        async with retry_client.get(link) as response:
            if response.ok:
                resp = await response.text()
                soup = BeautifulSoup(resp, 'lxml')
                item_cards = [f"{self.domain}{el['href']}" for el in soup.select('div.sale_button a')]
                tasks = [self._get_data(session, detail_url) for detail_url in item_cards]
                await asyncio.gather(*tasks)


    async def _get_data(self, session, detail_url):
        async with session.get(detail_url) as response:
            resp = await response.text()
            soup = BeautifulSoup(resp, 'lxml')
            in_stock = int(soup.find(id='in_stock').text.split(': ')[1])
            old_price = int(soup.find(id='old_price').text.split()[0])
            curr_price = int(soup.find(id='price').text.split()[0])
            self._total_discount += (old_price - curr_price) * in_stock


    async def main(self):
        ua = UserAgent()
        fake_ua = {'user-agent': ua.random}
        async with aiohttp.ClientSession(headers=fake_ua) as session:
            await asyncio.gather(*[asyncio.create_task(self._detail_button(session, link)) for link in self.pagen_list])


    def __call__(self, url, *args, **kwargs):
        soup = self.get_soup(url)
        self.get_urls_categories(soup)
        self.get_urls_pages()
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.main())


if __name__ == '__main__':
    parse_site = AsyncParser(domain='https://parsinger.ru/html/')
    parse_site('https://parsinger.ru/html/index1_page_1.html')

print(parse_site._total_discount)

