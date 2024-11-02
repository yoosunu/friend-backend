import requests
from bs4 import BeautifulSoup
from celery import shared_task


@shared_task
def get_infos(link):

    codes = []
    tags = []
    titles = []
    links = []
    writers = []
    etcs = []

    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")

    trs = soup.find_all(class_="tr-normal")  # get trs
    for tr in trs:
        # code
        brd_num = tr.find(class_="brd-num")
        code = brd_num.get_text().strip()
        codes.append(code)

        # tag
        tag_type = tr.find(class_="tag-type-01")
        tag = tag_type.get_text().strip()
        tags.append(tag)

        # title
        title_html = tr.find(class_="title")
        title = title_html.get_text().strip()
        titles.append(title)

        # link
        title_html = tr.find(class_="title")
        onclick_value = title_html.get("onclick")
        start_index = onclick_value.find("'") + 1
        end_index = onclick_value.find("'", start_index)
        extracted_value = onclick_value[start_index:end_index]
        address = f"https://www.jbnu.ac.kr/web/Board/{extracted_value}/detailView.do?pageIndex=1&menu=2377"
        links.append(address)

        # source
        brd_writer = tr.find(class_="brd-writer")
        writer = brd_writer.get_text().strip()
        writers.append(writer)

        # etc
        etc_list = tr.find(class_="etc-list")
        etc_list_li = etc_list.find("li")
        etc = etc_list_li.get_text().strip()
        etcs.append(etc)

    return codes, tags, titles, links, writers, etcs


@shared_task
def gather_infos():
    url1 = "http://www.jbnu.ac.kr/web/news/notice/sub01.do?pageIndex=1&menu=2377"
    url2 = "http://www.jbnu.ac.kr/web/news/notice/sub01.do?pageIndex=2&menu=2377"
    url3 = "http://www.jbnu.ac.kr/web/news/notice/sub01.do?pageIndex=3&menu=2377"

    codes1, tags1, titles1, links1, writers1, etcs1 = get_infos(url1)
    codes2, tags2, titles2, links2, writers2, etcs2 = get_infos(url2)
    codes3, tags3, titles3, links3, writers3, etcs3 = get_infos(url3)

    codes_total = codes1 + codes2 + codes3
    tags_total = tags1 + tags2 + tags3
    titles_total = titles1 + titles2 + titles3
    links_total = links1 + links2 + links3
    writers_total = writers1 + writers2 + writers3
    etcs_total = etcs1 + etcs2 + etcs3

    return (
        codes_total,
        tags_total,
        titles_total,
        links_total,
        writers_total,
        etcs_total,
    )


@shared_task
def create_notifications_task():
    from .models import Notification

    codes, tags, titles, links, writers, etcs = gather_infos()

    for i in range(len(codes)):
        notification, created = Notification.objects.get_or_create(
            code=codes[i],
            defaults={
                "tag": tags[i],
                "title": titles[i],
                "link": links[i],
                "writer": writers[i],
                "etc": etcs[i],
            },
        )
        if created:
            print(f"Notification {notification} created successfully!")
        else:
            print(f"Notification {notification} already exists.")
