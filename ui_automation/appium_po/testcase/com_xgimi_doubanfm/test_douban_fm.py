from time import sleep

import pytest

# TODO: 调试的时候临时加了这个
try:
    from appium_po.pages.com_xgimi_doubanfm.douban_fm_page import DoubanFmPage
except ModuleNotFoundError as e:
    import sys
    import os
    # sys.path.append('D:\\ProgramFiles\\allure-2.13.8\\bin')
    for _ in range(10):
        if os.getcwd().endswith('ui_automation'):
            sys.path.append(os.getcwd())
            break
        os.chdir('..')
    from appium_po.pages.com_xgimi_doubanfm.douban_fm_page import DoubanFmPage


class TestDoubanFm(object):

    @pytest.fixture
    def page(self, request):
        page = DoubanFmPage(request)

        return page

    def test_local_palyer_basic_interaction(self, page: DoubanFmPage):
        '''验证本地音乐播放器的基本交互

        基本交互包括：暂停、上一首、下一首、快进、快退
        '''

        # 暂停
        page.play_or_pause()
        current_time = page.get_current_time()
        sleep(3)
        assert current_time == page.get_current_time()
        page.play_or_pause()

        # 上一首
        first_music_name = page.get_music_name()
        page.last_song()
        assert first_music_name != page.get_music_name()

        # 下一首
        page.next_song()
        assert first_music_name == page.get_music_name()

        # 快进
        time_before, time_after = page.fast_forward()
        assert time_before + 10 < time_after

        # 快退
        time_before, time_after = page.fast_backward()
        assert time_before > time_after


if __name__ == '__main__':
    # 调试
    import pytest

    # 调试单个方法，不行的话试试下面的命令，或切换到UI_Automation目录下
    testcase_path = 'appium_po\\testcase\\com_xgimi_doubanfm\\test_douban_fm.py'
    class_name = 'TestDoubanFm'
    method_name = 'test_local_palyer_basic_interaction'
    pytest.main([f'{testcase_path}::{class_name}::{method_name}',])

    # 相同功能的命令行命令
    # pytest appium_po\\testcase\\com_xgimi_doubanfm\\test_douban_fm.py::TestDoubanFm::test_local_palyer_basic_interaction
