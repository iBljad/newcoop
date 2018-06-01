from datetime import datetime

from selenium import webdriver

from newcoop_app.models import Game, Platform, Link

url = "https://www.giantbomb.com/games/?letter=&sortBy=release&platform=&genre=&theme=&minRating=&rating=&region" \
      "=&fromYear=2/01/2010&toYear=05/20/2018&multiplayer%5B0%5D=17&multiplayer%5B1%5D=20&multiplayer%5B2%5D=22" \
      "&widescreen=1&page="

driver = webdriver.Chrome()

for i in range(1, 10):
    driver.get(url + str(i))
    game_list = driver.find_elements_by_css_selector('.editorial.grid>li')

    for game in game_list:
        title = game.find_element_by_tag_name("h3").text
        try:
            date = datetime.strptime(game.find_element_by_tag_name("span").text, '%B %d, %Y')
        except Exception:
            date = datetime.strptime('January 1, 2019', '%B %d, %Y')

        platforms = [p.get_attribute('textContent') for p in game.find_elements_by_tag_name("li") if
                     p.get_attribute("class") != "system more js-unhide-list"]

        ga = Game(game_name=title, pub_date=date)
        ga.save()

        for p in platforms:
            pl, flag = Platform.objects.get_or_create(platform_name=p)
            link = Link(game=ga, platform=pl)
            link.save()
