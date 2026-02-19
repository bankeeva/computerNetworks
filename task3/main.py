from datetime import datetime

from playwright.sync_api import sync_playwright
import pandas as pd


def authorize(page):
    login = input("Логин\n")
    password = input("Пароль\n")

    page.goto("https://habr.com/ru/login/", wait_until="domcontentloaded")

    page.fill('input[type="email"]', login)
    page.fill('input[type="password"]', password)
    page.click('button[type="submit"]')


rows = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
 
    ans = input("Вы хотите авторизоваться? (лучше не надо) да/нет\n").lower()
    if ans == "да":
        authorize(page)

    for page_num in range(1, 3):
        url = f"https://habr.com/ru/feed/page{page_num}/"
        page.goto(url, wait_until="domcontentloaded")
        
        articles = page.locator("article")

        for i in range(3):
            article = articles.nth(i)

            title_link = article.locator("h2 a").first
            title = (title_link.inner_text() or "None").strip()

            author_link = article.locator("a[data-test-id='user-info-username']").first
            author = (author_link.inner_text() or "None").strip()

            time_link = article.locator("time").first
            dt = (time_link.get_attribute("datetime") or "None").strip()
            if dt != "None":
                dt = dt.replace("Z", "+00:00")
                dt_obj = datetime.fromisoformat(dt)
                normal_dt = dt_obj.strftime("%d.%m.%Y %H:%M")

            views_link = article.locator("span.tm-icon-counter__value, span.tm-icon-counter_value").first
            views = (views_link.inner_text() or "None").strip()

            rows.append({
                "title": title,
                "author": author,
                "datetime": normal_dt,
                "views": views
            })

    browser.close()

df = pd.DataFrame(rows)
df.to_csv("result.csv", index=False, encoding="utf-8-sig")
