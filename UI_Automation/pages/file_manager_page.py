import base64
import copy
from io import BytesIO
from time import sleep
from typing import List, Tuple

from appium import webdriver
from PIL import Image
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.BasePage import BasePage


class FileManagerPage(object):
    '''资源管理器页面。

    包含资源管理器可用的页面操作与操作结果断言。
    TODO: 将操作方式重构为使用遥控器操作的方式（目前为鼠标操作方式）
    TODO: 将配置信息写到配置文件中
    '''

    # 基本配置
    BASE_CAPABILITIES = {
        'platformName': 'Android',
        'deviceName': 'Android Emulator',
        'platformVersion': '9',
    }

    # 应用特有配置
    APP_CAPABILITIES = {
        'appPackage': 'com.xgimi.filemanager',
        'appActivity': '.NewFileManagerActivity'
    }

    EXECUTOR = "http://localhost:4723/wd/hub"

    # 元素定位器

    # 单元格显示的区域
    GRID_CONTAINER = (By.ID, 'com.xgimi.filemanager:id/gmuigrid_grid')
    # tab栏
    TAB_BAR = (By.ID, 'com.xgimi.filemanager:id/viewpagertab')
    # 提示语
    NOTICE = (By.ID, 'com.xgimi.filemanager:id/file_header_notice')
    # 侧边栏
    SIDE_BAR = (
        By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout')
    # 弹出菜单
    POP_UP_MENU = (By.ID, 'com.xgimi.filemanager:id/dialog')

    # 本地视频、音乐、图片、文档播放器的activity
    ACTIVITY_VIDEO_PLAYER = '.activity.VideoPlayerActivity'
    ACTIVITY_MUSIC_PLAYER = '.localplayer.LocalMusicActivity'
    ACTIVITY_PICTURE_VIEWER = '.activity.ImagePlayActivity'
    ACTIVITY_DOCUMENT_VIEWER = '.HTMLViewerActivity'

    # 本地视频、音乐、图片、文档播放器的应用包名
    PACKAGE_VIDEO_PLAYER = 'com.xgimi.gimiplayer'
    PACKAGE_MUSIC_PLAYER = 'com.xgimi.doubanfm'
    PACKAGE_PICTURE_VIEWER = 'com.xgimi.gimiplayer'
    PACKAGE_DOCUMENT_VIEWER = 'com.android.htmlviewer'

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
        self.current_tab = '全部'

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

    def switch_tab(self, tab_name: str):
        '''切换tab。

        切换到名为 tab_name 的tab上，可传入的值：全部、视频、音乐、图片、文档。
        TODO(zerak.zhang): 重构为遥控器操作的方式，优化视频tab的特殊处理

        Args:
            tab_name: tab名称
        '''
        element_tab_bar = self.find_element(self.TAB_BAR)
        element_selected_tab = element_tab_bar.find_element_by_xpath(
            f'//android.widget.TextView[@text="{tab_name}"]')
        element_selected_tab.click()

        self.current_tab = tab_name

    def click_grid(self, grid_path: str):
        '''点击单元格，遥控器操作方式。

        点击名为grid_path的单元格。

        Args:
            grid_path: 单元格名称/路径

        Returns:
            点击确定的次数，方便回退到最初的目录

        Raises:
            NoSuchElementException: 找不到单元格时抛出

        Usage:
            page.click_grid('bar.png')
            page.click_grid('内置存储/Pictures/Screenshots/foo.png')
        '''
        grid_name_list = grid_path.split('/')
        for grid_name in grid_name_list:
            self.__move_to_grid(grid_name)
            self.press_keycode(23)  # center键
            self.depth += 1

    def back_to_initial_director(self):
        '''回到调用资源管理器初始页面。

        通常在调用click_grid后使用。

        Usage:
            page.click_grid('内置存储/Pictures/Screenshots/foo.png')
            page.back_to_initial_director()  # 可回到资源管理器初始页面
        '''
        self.press_keycode(4, self.depth)
        self.depth = 0

    def click_grid_d(self, grid_name: str):
        '''点击单元格，鼠标操作方式（弃用）。

        点击名为grid_name的单元格，如：点击"内置存储"、点击"syslog"等。

        Args:
            grid_name: 单元格名称
        '''
        element_grid_container = self.find_element(
            self.GRID_CONTAINER)
        element_selected_grid = element_grid_container.find_element_by_xpath(
            f'//android.widget.TextView[@text="{grid_name}"]/../..')
        element_selected_grid.click()

    def long_press_grid(self, grid_name: str):
        '''长按单元格。

        长按名为grid_name的单元格，如：长按"logcat.log"、长按"Alarms"等。

        Args:
            grid_name: 单元格名称
        '''
        def long_press_center():
            '''触发遥控器长按确定键的事件。

            但需要事先把焦点移动到需要长按的元素上。
            TODO(zerak.zhang): 优化长按事件触发逻辑，当前逻辑需要先获取遥控器的输入device，目前未实现
            '''
            self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                       '/dev/input/event6', '4', '4', '458792']})
            self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                       '/dev/input/event6', '1', '28', '1']})
            self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                       '/dev/input/event6', '0', '0', '0']})
            sleep(1)
            self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                       '/dev/input/event6', '4', '4', '458792']})
            self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                       '/dev/input/event6', '1', '28', '0']})
            self.driver.execute_script('mobile:shell', {'command': 'sendevent', 'args': [
                                       '/dev/input/event6', '0', '0', '0']})

        self.__move_to_grid(grid_name)
        long_press_center()

    def call_side_bar_and_click_option(self, option_name: str):
        '''呼出侧边栏并点击某一选项。

        呼出资源管理器的侧边栏并点击名为 option_name 的选项。

        Args:
            option_name: 选项名称

        Raises:
            NoSuchElementException: 找不到对应名称的option时抛出
        '''
        self.driver.press_keycode(82)  # TODO(zerak.zhang): 优化呼出侧边栏
        element_side_bar = self.find_element(
            self.SIDE_BAR)
        element_selected_option = element_side_bar.find_element_by_xpath(
            f'//android.widget.TextView[@resource-id="com.xgimi.filemanager:id/stv" and @text="{option_name}"]/..')
        element_selected_option.click()

    def click_pop_up_menu_option(self, option_name: str):
        '''点击 长按菜单 中的选项

        点击长按菜单中名为 option_name 的选项，如点击“复制文件”“重命名”。

        Args:
            option_name: 选项名称
        '''
        element_pop_up_menu = self.find_element(self.POP_UP_MENU)
        element_selected_option = element_pop_up_menu.find_element_by_xpath(
            f'//android.widget.Button[@text="{option_name}" and @resource-id="com.xgimi.filemanager:id/item_xgimidialog_btn"]')
        element_selected_option.click()

    def press_keycode(self, keycode: int, repeat: int = 1):
        '''发送按键键值

        发送某个按键键值，可重复发送

        Args:
            keycode: 键值
            repeat: 重复次数
        '''
        for _ in range(repeat):
            self.driver.press_keycode(keycode)
            sleep(0.5)

    def double_click(self, keycode: int = 4):
        '''双击某键。

        双击，通常用来退出，默认键值为退出。
        '''
        command = {'command': 'input', 'args': ['keyevent', f'{keycode}']}
        self.driver.execute_script('mobile:shell', command)
        self.driver.execute_script('mobile:shell', command)
        # self.driver.press_keycode(keycode)
        # self.driver.press_keycode(keycode)
        # actions = TouchAction(self.driver)

    def is_grid_sorted_by_name(self) -> bool:
        '''判断当前可见的单元格是否按照名称排序。

        可见单元格是否按照名称升序排序。

        Returns:
            按照名称升序排序返回True，否则返回False。
        '''
        element_grid_container = self.find_element(self.GRID_CONTAINER)
        elements_grid = element_grid_container.find_elements_by_xpath(
            'androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout')
        if len(elements_grid) < 2:
            return True
        else:
            last_grid_name = ''
            for grid in elements_grid:
                grid_name = grid.find_element_by_xpath(
                    'android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView').text
                if last_grid_name <= grid_name:
                    last_grid_name = grid_name
                else:
                    return False
            return True

    def is_grid_sorted_by_time(self) -> bool:
        '''判断当前可见的单元格是否按照时间排序。

        可见单元格是否按照时间升序排序。按时间排序需要切换到列表模式，才能从UI上获取到时间。

        Returns:
            按照时间升序排序返回True，否则返回False。
        '''
        try:
            self.call_side_bar_and_click_option('列表模式')
        except NoSuchElementException:
            pass

        element_grid_container = self.find_element(self.GRID_CONTAINER)
        elements_grid = element_grid_container.find_elements_by_xpath(
            'androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout')

        flag = True

        if len(elements_grid) < 2:
            flag = True
        else:
            last_grid_time = '修改时间 ：9999-12-31'
            for grid in elements_grid:
                # 这里对目录模式做了兼容（音乐tab默认目录模式）
                elements_text = grid.find_elements_by_xpath(
                    'android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.TextView')
                if len(elements_text) < 3:
                    continue
                else:
                    grid_time = elements_text[2].text
                if last_grid_time >= grid_time:
                    last_grid_time = grid_time
                else:
                    flag = False
                    break

        # 还原为图标模式
        self.call_side_bar_and_click_option('图标模式')

        return flag

    def is_list_mode_effective(self) -> bool:
        '''判断列表模式是否生效
        '''
        element_grid_container = self.find_element(self.GRID_CONTAINER)
        elements_grid = element_grid_container.find_elements_by_xpath(
            'androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout')
        if len(elements_grid) > 0:
            element_grid = elements_grid[0]
            width = element_grid.size.get('width', 0)
            height = element_grid.size.get('height', 100000)
            return width / height > 5
        else:
            # 判断无内容时背景中是否有提示语
            if element_grid_container.find_element_by_id('com.xgimi.filemanager:id/dialog_title'):
                return True
            else:
                return False

    def is_element_similar_to_img(self, element: WebElement, image_path: str, similarity: float = 0.8) -> bool:
        '''判断元素（节点）截图是否与特定图片相似。

        TODO
        判断元素截图与给定图片是否达到指定的相似度。

        Args:
            element: 页面元素（节点）
            image_path: 用于比较的图片路径
            similarity: 相似度，0为完全不相似，1为完全相同

        Returns:
            元素截图与给定图片是否达到给定相似度

        Usage:
            page.is_element_similar_to_img(element_grid, '/path/to/grid.png')
        '''
        return True

    def is_grid_exist(self, grid_name: str) -> bool:
        '''判断单元格是否存在（会移动焦点）

        Args:
            grid_name: 单元格名称
        '''
        try:
            self.__move_to_grid(grid_name)
            return True
        except NoSuchElementException:
            return False

    def __get_current_activity(self) -> str:
        '''获取当前的activity。

        TODO: 好像可以删除
        通常用于断言。

        Returns:
            当前的activity
        '''
        return ''

    def __move_to_grid(self, grid_name: str):
        '''将焦点移动到某单元格。

        TODO: 优化实现，目前焦点移动较慢
        TODO: 仍存在缺陷，焦点不能往上。
        定位名为grid_name的单元格，并将焦点移动到其上面，目前仅支持图标模式下的移动。
        定位逻辑：判断焦点所在行是否包含名为 grid_name 的单元格，不包含则移至下一行。

        Args:
            grid_name: 单元格名称

        Raises:
            NoSuchElementException: 找不到对应单元格时抛出
        '''

        def get_grid_name(grids: List[WebElement]) -> List[str]:
            '''获取单元格列表的text

            Args:
                grids: 节点列表

            Returns:
                节点名称列表
            '''
            def get_text(grid):
                return grid.find_element_by_xpath(
                    'android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView').text
            return list(map(get_text, grids))

        def get_focus_and_focused_row() -> Tuple[int, List[WebElement]]:
            '''获取焦点所在行（6个单元格）

            Returns:
                焦点位置 和 焦点所在行
                焦点位置为-1，表示焦点不在单元格上
            '''
            ROW_SIZE = 6

            element_grid_container = self.find_element(
            self.GRID_CONTAINER)
            elements_grid = element_grid_container.find_elements_by_xpath(
                'androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout')
            row_num = int((len(elements_grid) + ROW_SIZE - 1) / ROW_SIZE)  # 行数
            for i in range(row_num):
                for j in range(ROW_SIZE):
                    try:
                        if elements_grid[i * 6 + j].get_attribute('focused') == 'true':
                            upper_limit = min(len(elements_grid), i*6 + 6)
                            return (j, elements_grid[i*6: upper_limit])
                    except IndexError:
                        # 懒人处理法：对不满6个的行做特殊处理
                        break

            return (-1, [])

        def is_element_exist(text: str) -> bool:
            '''判断页面是否有 带有文本text的元素。

            专门为“视频”tab的观看记录做的特殊处理。

            Args:
                需要判断的text
            '''
            try:
                element_grid_container = self.find_element(
                    self.GRID_CONTAINER)
                element_grid_container.find_element_by_xpath(
                    f'//android.widget.TextView[@text="{text}"]')
                return True
            except NoSuchElementException:
                return False

        # 查找当前行是否存在名为grid_name的单元格。first_grid_name用于判断是否到底部。
        first_grid_name = ''
        while True:

            # TODO: 优化。专门为视频tab的观看记录做的特殊处理
            if self.current_tab == '视频' and is_element_exist('观看记录'):
                self.press_keycode(20)
                continue

            focus, elements_focused_row = get_focus_and_focused_row()

            # 判断焦点所在行有无目标单元格
            # 有则右移到此单元格，无则移动到下一行
            # 到底部时仍未找到则抛出错误
            if focus >= 0:
                focused_row_grid_name = get_grid_name(elements_focused_row)
                if first_grid_name == focused_row_grid_name[0]:
                    raise NoSuchElementException(f'没有找到名为 {grid_name} 的单元格')
                first_grid_name = focused_row_grid_name[0]

                try:
                    index = focused_row_grid_name.index(grid_name)
                except ValueError:
                    index = None

                if index is not None:
                    if index - focus >= 0:
                        # 右移
                        self.press_keycode(22, index - focus)
                    else:
                        # 左移
                        self.press_keycode(21, focus - index)
                    break

            self.press_keycode(20)

    def __cut_out_screen(self, rect: dict = {}) -> Image.Image:
        '''从屏幕中截取一小块图片。

        TODO
        从图片坐标为(x, y)的位置，截取大小为(width, height)这么大一块的图片。

        Args:
            rect: 截取的位置和大小，如 {'x': 10, 'y': 100, 'width': 400, 'height': 300}
            若rect为空，则截取整个画面（即截屏）

        Returns:
            截取出来的图片
        '''
        img_base64_str = self.driver.get_screenshot_as_base64()
        img_binary_str = base64.b64decode(img_base64_str)
        img = Image.open(BytesIO(img_binary_str))
        if rect:
            pass
        else:
            img.show()
        
        return img


if __name__ == '__main__':
    pass
