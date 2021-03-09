from time import sleep

import pytest

# TODO: 调试的时候临时加了这个
try:
    from appium_po.pages.com_xgimi_filemanager.file_manager_page import FileManagerPage
    from utils import android_common as android
    from utils.adb_tool import AndroidDebugBridge
except ModuleNotFoundError:
    import sys
    import os
    sys.path.append(os.getcwd())
    os.chdir(os.path.abspath(os.path.join('../../testcase', 'testcase')))
    from appium_po.pages.com_xgimi_filemanager.file_manager_page import FileManagerPage
    from utils import android_common as android
    from utils.adb_tool import AndroidDebugBridge


class TestFilemanager:

    @pytest.fixture
    def page(self, request):
        '''测试应用的page

        通过page调用应用的常用操作进行测试

        Args:
            request: 通过request可访问测试上下文和其他fixture
        '''
        page = FileManagerPage(request)

        return page

    def test_side_bar(self, page: FileManagerPage):
        '''检查资源管理器侧边栏功能

        关联用例：
            禅道6587 验收-资源管理器-资源管理器侧边栏
        '''
        # 全部tab
        page.switch_tab('全部')
        page.call_side_bar_and_click_option('列表模式')
        assert page.is_list_mode_effective()
        page.call_side_bar_and_click_option('图标模式')

        page.call_side_bar_and_click_option('搜索DLNA服务')
        assert page.is_toast_exist('已启动搜索')

        # 视频tab
        page.switch_tab('视频')
        assert page.is_grid_sorted_by_name()

        page.call_side_bar_and_click_option('按时间排序')
        assert page.is_grid_sorted_by_time()
        page.call_side_bar_and_click_option('按名称排序')

        page.call_side_bar_and_click_option('列表模式')
        assert page.is_list_mode_effective()
        page.call_side_bar_and_click_option('图标模式')

        # TODO: 视频tab目录模式和播放模式

        page.call_side_bar_and_click_option('搜索视频文件')
        # TODO: 断言当前的activity
        page.driver.back()

        # TODO: 全选、多选

        # 音乐tab
        page.switch_tab('音乐')
        assert page.is_grid_sorted_by_name()

        page.call_side_bar_and_click_option('按时间排序')
        assert page.is_grid_sorted_by_time()
        page.call_side_bar_and_click_option('按名称排序')

        page.call_side_bar_and_click_option('列表模式')
        assert page.is_list_mode_effective()
        page.call_side_bar_and_click_option('图标模式')

        page.call_side_bar_and_click_option('搜索音频文件')
        # TODO: 断言当前的activity
        page.driver.back()

        # TODO: 全选、多选

        # 图片tab
        page.switch_tab('图片')
        assert page.is_grid_sorted_by_name()

        page.call_side_bar_and_click_option('按时间排序')
        assert page.is_grid_sorted_by_time()
        page.call_side_bar_and_click_option('按名称排序')

        page.call_side_bar_and_click_option('搜索图片文件')
        # TODO: 断言当前的activity
        page.driver.back()

        # TODO: 全选、多选

        # 文档tab
        page.switch_tab('文档')
        assert page.is_grid_sorted_by_name()

        page.call_side_bar_and_click_option('按时间排序')
        assert page.is_grid_sorted_by_time()
        page.call_side_bar_and_click_option('按名称排序')

        page.call_side_bar_and_click_option('搜索文档文件')
        # TODO: 断言当前的activity
        page.driver.back()

        # TODO: 全选、多选

        # TODO: 文件复制、剪切、粘贴

    def test_fundamantal_function(self, page: FileManagerPage):
        '''测试基本功能

        关联用例:
            禅道6586 验收-资源管理器-资源管理器功能检查
        '''
        # 播放内置存储系统的视频
        page.switch_tab('全部')
        page.click_grid('内置存储/wandoujia/video_2D.mp4')
        sleep(3)
        assert page.PACKAGE_VIDEO_PLAYER == page.driver.current_package
        assert page.ACTIVITY_VIDEO_PLAYER == page.driver.current_activity
        page.double_click()
        page.back_to_initial_director()

        # 播放外置U盘视频
        # TODO: 单元格路径为临时路径
        page.click_grid('张正/test_media/3D_FPS/3D-15FPS.mp4')
        sleep(3)
        assert page.PACKAGE_VIDEO_PLAYER == page.driver.current_package
        assert page.ACTIVITY_VIDEO_PLAYER == page.driver.current_activity
        page.double_click()
        page.back_to_initial_director()

        # TODO: 播放DLNA文件夹视频

        # TODO: 添加设备
        page.click_grid('添加设备')
        page.back_to_initial_director()

        # 视频tab内播放视频
        page.switch_tab('视频')
        page.click_grid('video_2D.mp4')
        sleep(3)
        assert page.PACKAGE_VIDEO_PLAYER == page.driver.current_package
        assert page.ACTIVITY_VIDEO_PLAYER == page.driver.current_activity
        page.double_click()
        page.press_keycode(4)

        # 音乐tab
        page.switch_tab('音乐')
        # TODO: 单元格路径为临时路径
        page.click_grid('Music(共7首)/xgimi01.mp3')
        sleep(3)
        assert page.PACKAGE_MUSIC_PLAYER == page.driver.current_package
        assert page.ACTIVITY_MUSIC_PLAYER == page.driver.current_activity
        page.double_click()  # 不能退出音乐播放器
        page.back_to_initial_director()

        # 图片tab
        page.switch_tab('图片')
        # TODO: 单元格路径为临时路径
        page.click_grid('1920x1080.jpg')
        sleep(3)
        assert page.PACKAGE_PICTURE_VIEWER == page.driver.current_package
        assert page.ACTIVITY_PICTURE_VIEWER == page.driver.current_activity
        page.back_to_initial_director()

        # 文档tab
        page.switch_tab('文档')
        page.click_grid('try.txt')
        page.double_click(23)
        sleep(3)
        assert page.PACKAGE_DOCUMENT_VIEWER == page.driver.current_package
        assert page.ACTIVITY_DOCUMENT_VIEWER == page.driver.current_activity
        page.press_keycode(4)


if __name__ == '__main__':

    pytest.main()
