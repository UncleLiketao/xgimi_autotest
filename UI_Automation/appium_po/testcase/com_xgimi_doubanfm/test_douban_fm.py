from time import sleep

import pytest

# TODO: 调试的时候临时加了这个
try:
    from appium_po.pages.com_xgimi_doubanfm.douban_fm_page import DoubanFmPage
except ModuleNotFoundError as e:
    import sys
    import os
    sys.path.append(os.getcwd())
    os.chdir(os.path.abspath(os.path.join('../../testcase', 'testcase')))
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
        current_time = page.current_time
        sleep(3)
        assert current_time == page.current_time
        page.play_or_pause()

        # 上一首
        first_music_name = page.music_name
        page.last_song()
        assert first_music_name != page.music_name

        # 下一首
        page.next_song()
        assert first_music_name == page.music_name

        # 快进
        time_before, time_after = page.fast_forward()
        assert time_before < time_after

        # 快退
        time_before, time_after = page.fast_backward()
        assert time_before > time_after


if __name__ == '__main__':

    pytest.main()
