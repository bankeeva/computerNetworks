from datetime import datetime

from playwright.async_api import async_playwright
import pandas as pd


async def parse_url_to_df(url):
    rows = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        for page_num in range(1, 4):
            page_url = url + f"page{page_num}/"
            await page.goto(page_url, wait_until="domcontentloaded")
            
            articles = page.locator("article")

            for article_index in range(3):
                article = articles.nth(article_index)

                try:
                    title_link = article.locator("h2 a").first
                    title = ((await title_link.inner_text()) or "None").strip()

                    author_link = article.locator("a[data-test-id='user-info-username']").first
                    author = ((await author_link.inner_text()) or "None").strip()

                    time_link = article.locator("time").first
                    dt = ((await time_link.get_attribute("datetime")) or "None").strip()
                    normal_dt = "None"
                    if dt != "None":
                        dt = dt.replace("Z", "+00:00")
                        dt_obj = datetime.fromisoformat(dt)
                        normal_dt = dt_obj.strftime("%d.%m.%Y %H:%M")

                    views_link = article.locator(
                        "span.tm-icon-counter__value, span.tm-icon-counter_value").first
                    views = ((await views_link.inner_text()) or "None").strip()

                    if title == "None" or author == "None" or views == "None":
                        continue

                    rows.append({
                        "title": title,
                        "author": author,
                        "datetime": normal_dt,
                        "views": views
                    })

                except Exception:
                    continue

        await browser.close()

    return pd.DataFrame(rows)
