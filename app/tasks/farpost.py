from multiprocessing import freeze_support
from typing import Any, Callable
import asyncio

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pypasser.exceptions import IpBlock
import undetected_chromedriver as uc
from pypasser import reCaptchaV2
from bs4 import BeautifulSoup
from loguru import logger

from app.resources.database import async_session
from app.repositories import FarpostRepository
from app.schemes.farpost import PostPreview
from .base import celery


class FarPostParser:
    def __init__(self):
        self.driver = uc.Chrome(headless=True)
    
    def _is_captcha(self) -> bool:
        exists = "Вы не робот?" in self.driver.page_source
        return exists

    def _try_solve_captcha(self) -> bool:
        try:
            is_checked = reCaptchaV2(driver=self.driver, play=False)
        except (IpBlock, FileNotFoundError, NoSuchElementException):
            return False
        
        if is_checked is False:
            logger.debug("Captcha not solved")
            return False
        
        self.driver.find_element(By.CSS_SELECTOR, '#send-button').click()
        if 'Verification Success' in self.driver.page_source:
            logger.debug("Captcha solved")
            return True
        
        logger.debug("Captcha not solved")
        return False

    @staticmethod
    def _attr_exists(attr_name: str) -> Callable:
        def wrapper(tag_data: Any | None) -> bool:
            nonlocal attr_name
            return bool(tag_data)
        return wrapper
    
    def _open_page(self, url: str, skip_captcha: bool = False) -> str:
        self.driver.get(url)
        if self._is_captcha() and skip_captcha is False:
            logger.debug("Captcha detected")
            is_solved = self._try_solve_captcha()

            if is_solved is False:
                return self._open_page(url, True)

        return self.driver.page_source

    def _get_feed(self, query: str) -> str:
        logger.debug(f"Open feed page: {query}")
        page = self._open_page(f"https://www.farpost.ru/vladivostok/service/construction/guard/+/{query}/")
        return page

    def _get_post_view(self, post_id: int) -> str:
        logger.debug(f"Open post page ID:{post_id}")
        page = self._open_page(f"https://www.farpost.ru/{post_id}")
        return page

    def _process_feed(self, query: str, html_body: str) -> list[PostPreview]:
        soup = BeautifulSoup(html_body, 'lxml')
        elements = soup.find_all("tr", attrs={"data-doc-id": self._attr_exists("data-doc-id")}, limit=10)
        
        posts = []
        for index, element in enumerate(elements, start=1):
            data = {"position": index, "query": query}
            head_div = element.find("div", {"data-bulletin-id": self._attr_exists("data-bulletin-id")})
            data["id"] = head_div["data-bulletin-id"]
            title = head_div.find("a", {"data-role": "bulletin-link"})
            data["title"] = title.string
            view_counter = head_div.find("span", class_="views")
            data["views_count"] = int(view_counter.string)
            
            posts.append(
                PostPreview(**data)
            )
        return posts
    
    def _get_author_from_post_view(self, post_id: int, html_body: str) -> str | None:
        soup = BeautifulSoup(html_body, 'lxml')
        author_div = soup.find("div", class_="seller-summary-user")
        if author_div is None:
            # self.driver.save_screenshot(f"{post_id}.png")
            logger.debug(f"Post[{post_id}] view: div with class='seller-summary-user' not found")
            return None
        
        try:
            return author_div.span.a.string
        except type(None):
            return None

    def _fill_post(self, post: PostPreview) -> PostPreview:
        post_body = self._get_post_view(post.id)
        author = self._get_author_from_post_view(post.id, post_body)
        post.author = author
        return post

    def get_posts(self, query: str = "Системы+видеонаблюдения") -> list[PostPreview]:
        feed_body = self._get_feed(query)

        if self._is_captcha():
            logger.debug(f"Process feed[{query}] fail: robot detected")
            return []
        
        posts = self._process_feed(query, feed_body)
        logger.debug(f"Process feed[{query}]: result: {posts}")
        from pprint import pprint as print
        
        for post in posts:
            self._fill_post(post)

        return posts
    
    def close(self):
        self.driver.close()


async def _save_new_posts(repository: FarpostRepository, posts: list[PostPreview]):
    logger.debug("Try to create new posts")
    for post in posts:
        post_id = await repository.create(post)
        logger.debug(f"Post with id:{post_id} created")


async def _delete_old_posts(repository: FarpostRepository, query: str):
    logger.debug(f"Try to delete old posts: {query}")
    posts = await repository.list(query)
    for post in posts:
        result = await repository.delete(post)
        if result:
            logger.debug(f"Post with id:{post.id} deleted")
        else:
            logger.debug(f"Post with id:{post.id} not deleted")


async def _update_farpost_posts(posts: list[PostPreview]):    
    async with async_session() as session:
        repository = FarpostRepository(session)
        
        await _delete_old_posts(repository, posts[0].query)
        await _save_new_posts(repository, posts)
        


@celery.task
def update_farpost_data():
    parser = FarPostParser()
    posts = []
    try:
        posts.extend(
            parser.get_posts()
        )
    finally:
        parser.close()
    
    if bool(posts) is False:
        return
    
    asyncio.run(_update_farpost_posts(posts))

