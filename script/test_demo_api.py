# -*- coding: utf-8 -*-
# @Time    : 2020-05-23
# @Author  : 爱吃苹果的鱼

from framework.base import selenium_init
from framework.base import selenium_action
import allure
import pytest
import time
from bs4 import BeautifulSoup


@allure.feature('feature_api_demo')
class TestApiDemo:

    @pytest.fixture(scope='function')
    def setup(self):
        self.webInit = selenium_init.SeleniumInit()
        self.driver = self.webInit.setup('headless')
        self.webAct = selenium_action.SeleniumActionAPI(self.driver)

    @pytest.mark.api
    @allure.story('test_story_of_api_demo')
    def test_api_demo(self, setup):
        self.webAct.to_url("https://cn.bing.com/")  # 打开必应网页（无头模式）
        self.webAct.ele_send_keys(self.webAct.ele_get_by_id('sb_form_q'), 'selenium')  # 搜索框输入'selenium'
        self.webAct.ele_click_by_id('search_icon')  # 搜索
        time.sleep(3)
        bs = BeautifulSoup(self.driver.page_source, 'html.parser')
        result = False
        for item in bs.select("*[id='b_results']"):
            if 'selenium' in str(item.get_text()).lower():
                result = True
            else:
                print(str(item.get_text()).lower() + '：不包含selenium')
                result = False
        assert result

    def teardown(self):
        self.driver.quit()