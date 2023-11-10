import lxml
import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup as BS
from config.config import PAGINATION_URL_CHECK, PAGE_URL

COUNT = 1
async def pagination_check(url: str, proxy=None) -> int:
	async with ClientSession() as session:
		async with session.get(url=url, proxy=proxy) as response:
			status_code = response.status
			text = await response.text()
	soup = BS(text, "lxml")
	pagination = soup.find_all("a", class_="pagination__link link")[-1].text.strip()
	return pagination

async def parsing_link(page: int, proxy=None) -> None:
	global COUNT
	async with ClientSession() as session:
		async with session.get(PAGE_URL.format(page), proxy=proxy) as response:
			status_code = response.status
			text = await response.text()
	soup = BS(text, "lxml")
	link = soup.find_all("a", class_="items-element__title")
	for i in link:
		title = i.text.strip()
		lk = i.get("href")
		with open("link_list.txt", "a") as file:
			file.write("{}:{}\n".format(title, link)
		print(COUNT, title, lk)
		COUNT += 1
	print("PAGE: ", page)

async def main() -> None:
	task = []
	pagination = int(await pagination_check(PAGINATION_URL_CHECK)) -1
	for i in range(2, pagination):
		task.append(asyncio.create_task(parsing_link(i)))
	await asyncio.gather(*task)

asyncio.run(main())



