import base64
import copy
from time import sleep
from typing import List, Tuple
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By



class DoubanFmPage(object):
    '''本地音乐播放器页面。

    包含本地音乐播放器可用的页面操作与操作结果断言。
    '''
    # 基本配置
    BASE_CAPABILITIES = {
        'platformName': 'Android',
        'deviceName': 'Android Emulator',
        'platformVersion': '9',
    }

    # 应用特有配置
    APP_CAPABILITIES = {
        'appPackage': 'com.xgimi.doubanfm',
        'appActivity': '.localplayer.LocalMusicActivity'
    }

    EXECUTOR = "http://localhost:4723/wd/hub"

    # 包名与Activity
    PACKAGE = 'com.xgimi.doubanfm'
    ACTIVITY_XGIMI_MUSIC = 'com.xgimi.doubanfm.activity.MusicActivity'
    ACTIVITY_XGIMI_MUSIC_ALBUM = 'com.xgimi.album.MainActivity'
    ACTIVITY_XGIMI_MUSIC_SEARCH = 'com.xgimi.modulesearch.SearchActivity'
    ACTIVITY_XGIMI_MUSIC_SINGER_INFO = 'com.xgimi.modulesearch.SingerInfoActivity'
    ACTIVITY_LOCAL_PLAYER = '.localplayer.LocalMusicActivity'

    # 元素定位器（本地播放器activity）

    # 背景
    BACKGROUND_LOCAL = (By.ID, 'com.xgimi.doubanfm:id/music_bg_iv')
    # 播放器主体
    MAIN_LAYOUT_LOCAL = (By.ID, 'com.xgimi.doubanfm:id/music_relativelayout')
    # 当前时间、总时间、进度条
    CURRENT_TIME_LOCAL = (By.ID, 'com.xgimi.doubanfm:id/curr_time')
    TOTAL_TIME_LOCAL = (By.ID, 'com.xgimi.doubanfm:id/all_time')
    PROGRESS_BAR_LOCAL = (By.ID, 'com.xgimi.doubanfm:id/play_pb')
    # 音乐名称、歌手、歌词、音乐封面
    MUSIC_NAME_LOCAL = (By.ID, 'com.xgimi.doubanfm:id/song_name_tv')
    ARTIST_LOCAL = (By.ID, 'com.xgimi.doubanfm:id/artist_tv')
    LYRIC_LOCAL = (By.ID, 'com.xgimi.doubanfm:id/lrcView')
    MUSIC_COVER_LOCAL = (By.ID, 'com.xgimi.doubanfm:id/cover_iv')
    # 上一首按钮、暂停/播放按钮、下一首按钮
    LAST_SONG_BUTTON_LOCAL = (By.ID, 'com.xgimi.doubanfm:id/shangyiqu_btn')
    PLAY_BUTTON_LOCAL = (By.ID, 'com.xgimi.doubanfm:id/bofang_btn')
    NEXT_SONG_BUTTON_LOCAL = (By.ID, 'com.xgimi.doubanfm:id/xiayiqu_btn')

    # 元素定位器（极米音乐activity）

    # 音乐名称、歌手、歌词（主题专辑封面）
    MUSIC_NAME_ALBUM_COVER = (By.ID, 'com.xgimi.doubanfm:id/song_name_tv')
    ARTIST_ALBUM_COVER = (By.ID, 'com.xgimi.doubanfm:id/artist_tv')
    LYRIC_ALBUM_COVER = (By.ID, 'com.xgimi.doubanfm:id/lrcView')
    # 音乐名称、歌词（主题动感频谱）
    MUSIC_NAME_DYNAMIC_SPECTTUM = (By.ID, 'com.xgimi.doubanfm:id/title')
    LYRIC_TOP_DYNAMIC_SPECTTUM = (By.ID, 'com.xgimi.doubanfm:id/krc_top')
    LYRIC_BOTTOM_DYNAMIC_SPECTTUM = (By.ID, 'com.xgimi.doubanfm:id/krc_bottom')
    # 歌词、画板（主题艺术歌词）
    LYRIC_ARTISTIC_LYRIC = (By.ID, 'com.xgimi.doubanfm:id/text_surface')
    CANVAS_ARTISTIC_LYRIC = (By.ID, 'com.xgimi.doubanfm:id/canvas')

    # 上一首按钮、暂停/播放按钮、下一首按钮
    LAST_SONG_BUTTON = (By.ID, 'com.xgimi.doubanfm:id/switch_left')
    PLAY_BUTTON = (By.ID, 'com.xgimi.doubanfm:id/play_status')  # 只是中间的播放状态图标
    NEXT_SONG_BUTTON = (By.ID, 'com.xgimi.doubanfm:id/switch_right')
    # 主题选择列表
    THEME_LIST = (By.ID, 'com.xgimi.doubanfm:id/horizonGrid')    

    def __init__(self, request):
        '''
        Args:
            reqeust: pytest的内建fixture
        '''
        caps = copy.copy(self.BASE_CAPABILITIES)
        caps.update(self.APP_CAPABILITIES)

        driver = webdriver.Remote(
            command_executor=self.EXECUTOR, desired_capabilities=caps)
        driver.implicitly_wait(10)

        def fin():
            driver.quit()
        request.addfinalizer(fin)

        self.driver = driver
        self.request = request
        self.depth = 0

    def find_element(self, loc):
        # TODO: 切换到框架之后需要删除此方法
        return self.driver.find_element(*loc)

    def is_toast_exist(self, text):
        # TODO: 切换框架后删除
        try:
            toast_loc = (By.XPATH, f'.//*[contains(@text,"{text}")]')
            self.find_element(toast_loc)
            return True
        except NoSuchElementException:
            return False

    def press_keycode(self, keycode: int, repeat: int = 1):
        '''TODO: 删掉
        '''
        self.driver.press_keycode(keycode)
        sleep(0.5)

    def next_song(self):
        '''下一首
        '''
        self.press_keycode(22)

    def play_or_pause(self):
        '''播放/暂停
        '''
        self.press_keycode(23)

    def last_song(self):
        '''上一首
        '''
        self.press_keycode(21)

    def fast_forward(self) -> Tuple[int, int]:
        '''快进

        Returns:
            快进前的时间，快进后的时间
        '''
        time_before_moving_forward = self.current_time

        self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                   '/dev/input/event6', '4', '4', '458831']})
        self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                   '/dev/input/event6', '1', '106', '1']})
        self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                   '/dev/input/event6', '0', '0', '0']})
        # 至少延迟1s，长按1s后才触发快进
        sleep(2)
        self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                   '/dev/input/event6', '4', '4', '458831']})
        self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                   '/dev/input/event6', '1', '106', '0']})
        self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                   '/dev/input/event6', '0', '0', '0']})

        time_after_moving_forward = self.current_time

        return (time_before_moving_forward, time_after_moving_forward)

    def fast_backward(self) -> Tuple[int, int]:
        '''快退

        Returns:
            快退前的时间，快退后的时间
        '''
        time_before_moving_backward = self.current_time

        self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                   '/dev/input/event6', '4', '4', '458832']})
        self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                   '/dev/input/event6', '1', '105', '1']})
        self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                   '/dev/input/event6', '0', '0', '0']})
        # 至少延迟1s，长按1s后才触发快退
        sleep(2)
        self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                   '/dev/input/event6', '4', '4', '458832']})
        self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                   '/dev/input/event6', '1', '105', '0']})
        self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                   '/dev/input/event6', '0', '0', '0']})

        time_after_moving_backward = self.current_time

        return (time_before_moving_backward, time_after_moving_backward)

    # TODO(zerak.zhang): 获取歌曲信息、时间太久了，会导致用例失败
    @property
    def music_name(self) -> str:
        return self.find_element(self.MUSIC_NAME_LOCAL).text

    @property
    def total_time(self) -> int:
        '''歌曲的总时长，以秒为单位返回
        '''
        total_time_str = self.find_element(self.TOTAL_TIME_LOCAL).text
        total_time_min_and_sec = total_time_str.split(':')
        total_time = int(
            total_time_min_and_sec[0])*60 + int(total_time_min_and_sec[1])

        return total_time

    @property
    def current_time(self) -> int:
        '''歌曲的当前播放时长，以秒为单位返回
        '''
        current_time_str = self.find_element(self.CURRENT_TIME_LOCAL).text
        current_time_min_and_sec = current_time_str.split(':')
        current_time = int(
            current_time_min_and_sec[0])*60 + int(current_time_min_and_sec[1])

        return current_time

    @property
    def current_progress(self) -> str:
        '''当前进度，播放即将完成时进度为1000
        '''
        return self.find_element(self.PROGRESS_BAR_LOCAL).text


if __name__ == '__main__':
    pass
