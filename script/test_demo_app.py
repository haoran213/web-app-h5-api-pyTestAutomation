# -*- coding: utf-8 -*-
# @Time    : 2020-05-23
# @Author  : 爱吃苹果的鱼

import pytest
import allure
from framework.base import appium_init
from framework.app.appcommon import AppCommon
from framework.base.selenium_action import SeleniumActionAPI
from framework.utils.string_utils import StringUtils
import time


@allure.feature('feature_app_demo')
class TestAppDemo:

    @pytest.fixture(scope='function')
    def setup(self):
        #
        # 使用模拟器docker android:https://github.com/budtmo/docker-android
        # docker run --privileged -d -p 6080:6080 -p 4723:4723 -p 5554:5554 -p 5555:5555
        #   -v sample_apk:/root/tmp
        #   -e DEVICE="Samsung Galaxy S6" -e APPIUM=true -e CONNECT_TO_GRID=true
        #   -e APPIUM_HOST="127.0.0.1" -e APPIUM_PORT=4723 -e SELENIUM_HOST="172.17.0.1"
        #   -e SELENIUM_PORT=4444 -e MOBILE_WEB_TEST=true -e RELAXED_SECURITY=true
        #   --name android-container01 budtmo/docker-android-x86-8.1
        self.appInit = appium_init.AppiumInit('8', 'android', '127.0.0.1:5555', 'com.android.contacts',
                                        'com.android.contacts.activities.PeopleActivity', '4723')
        self.driver = self.appInit.setup()
        self.app = AppCommon(self.driver)
        self.appium = SeleniumActionAPI(self.driver)
        self.util = StringUtils()

    @pytest.mark.app
    @allure.story('test_story_of_app_demo')
    def test_app_demo(self, setup):
        self.app.tap_click(int(959*self.app.device_x_get()/1080), int(1670*self.app.device_y_get()/1794))
        # time.sleep(5)
        # self.appium.ele_click_by_id('com.android.contacts:id/left_button')
        time.sleep(2)
        edit_boxes = self.appium.ele_list_get_by_class_name("android.widget.EditText")
        random_name = self.util.name_get()
        self.appium.ele_send_keys(edit_boxes[0], random_name)
        self.appium.ele_send_keys(edit_boxes[2], self.util.phone_get())
        self.appium.ele_click_by_id('com.android.contacts:id/editor_menu_save_button')
        result = self.app.toast_chk('//*[@text=\'{}\']'.format(random_name))
        assert result

    def teardown(self):
        self.driver.quit()

