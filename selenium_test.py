from selenium import webdriver
from selenium.webdriver.common.by import By
from helpers import random_letters
# from webdriver_manager.firefox import GeckoDriverManager

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# from webdriver_manager
import requests
import pytest
import os


@pytest.fixture(scope='class')
def channel_setup(request):
  service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

  chrome_options = Options()
  options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1080",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
  ]
  for option in options:
    chrome_options.add_argument(option)

  request.cls.driver = webdriver.Chrome(service=service, options=chrome_options)
  request.cls.base_url = os.environ.get('URL') + "/channels/"
  request.cls.params = {
    "title": random_letters(50),
    "description": random_letters(200),
    "url": "https://www.google.com/",
    "image_url": "https://www.google.com/images/branding/googlelogo/1x/googlelogo_light_color_272x92dp.png",
    "language": random_letters(200),
    "subjects": random_letters(200)
  }

  yield request.cls.driver
  request.cls.driver.close()
  request.cls.driver.quit()


# class TestUsers():
#   pass

# @pytest.mark.usefixtures("setup")
# class TestVideos():
#   pass


@pytest.mark.usefixtures("channel_setup")
class TestChannels():

  def test_channel_creation(self):
    # Create a new random channel
    self.driver.get(self.base_url)
    response = requests.post(self.base_url, data=self.params)

    assert response.status_code == 200, f"Error handeling the post request (status code: {response.status_code}, {response.text})"

  def test_created_channel(self):
    # Check if the created channel appears in the list
    self.driver.get(self.base_url)
    created_element = self.driver.find_element(By.XPATH, "/html/body/ul[2]/li[last()]")

    assert created_element.text == self.params["title"]

  def test_check_channel_infos(self):
    # Go the the channel page and check the infos
    self.driver.get(self.base_url + self.params['title'])

    response = requests.get(self.base_url + self.params['title'])
    assert response.status_code == 200, f"Error handeling the post request (status code: {response.status_code}, {response.text})"

    channel = list(response.json().values())[0]

    assert channel['description'] == self.params['description']
    assert channel['image_url'] == self.params['image_url']
    assert channel['language'] == self.params['language']
    assert channel['subjects'] == self.params['subjects']
    assert channel['title'] == self.params['title'] # a modif
    assert channel['url'] == self.params['url']


# class TestMainPage():
  
#   def test_title(self):
#     self.driver.get(self.base_url)
#     assert self.driver.title == "Home"

  # Test the login bar