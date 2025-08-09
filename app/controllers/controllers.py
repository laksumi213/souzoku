from datetime import date
from app.views.views import MyLayout
from app.views.settings_view import SettingsBody
from app.models.models import *
from pyautogui import typewrite
import app.utils as utils
import asyncio
from flet import (
    Page,
    AlertDialog,
)


class BaseController:
    def __init__(self, page: Page):
        super().__init__()
        self.page = page


class MainController(BaseController):
    def __init__(self, page: Page):
        super().__init__(page)
        page.on_keyboard_event = self.on_key_down

        # MyLayout(page, self)
        page.add(MyLayout(page, self))

        page.session.set('/settings', SettingsBody())
        page.on_route_change = lambda e: route_change(self.page, e)
        page.go('/home')

    def on_key_down(self, e):
        # print()
        # print('on_key_down:', e)
        # print(self.page.route)
        if e.key == ':' and e.ctrl:
            utils.ime_off()
            typewrite(date.today().strftime('%Y/%m/%d'))

        if self.page.route == '/home':
            if (e.key == 'c' or e.key == 'C') and e.alt:
                self.clear_click(self)

        if e.key == 'Arrow Up' and e.alt:
            self.page.window.full_screen = not self.page.window.full_screen

        self.page.update()

    def clear_click(self, _):
        print()
        print('clear_click')

        for count in range(len(self.page.session.get('/home').search_fields.controls)):
            for control in self.page.session.get('/home').search_fields.controls[count].controls:
                control.value = ''
                if control.label == '被相続人：姓かな':
                    control.focus()

        self.page.session.get('/home').ch_contractor.value = True
        self.page.session.get('/home').ch_me_rep_person.value = True
        results = self.get_result_view_all(page=self.page)
        self.page.session.get('/home').customer_data_table(results)
        self.page.update()

    def return_clicked(self, _):
        print('')
        print('return_clicked:')

        # 戻るrouteを取得して削除
        self.page.session.get('past_route').pop()
        key = self.page.session.get('past_route').pop()
        print('past_route:', self.page.session.get('past_route'))

        # サイドバーのインデックスを設定
        print('past_selected_index:', self.page.session.get('past_selected_index')[key])
        self.page.session.get('sideber').nav_rail.selected_index = self.page.session.get('past_selected_index')[key]

        # 前のページに戻る
        self.page.go(key)

        # 過去ルートがホームだけの場合、戻るボタンを非表示
        if len(self.page.session.get('past_route')) == 0:
            self.page.session.get('eb_return').content.visible = False
            self.page.update()

    @classmethod
    def get_result_view_all(cls, page, *args, **kwargs):
        results = Decedent.get_result_view_all(page)
        return results

    def search_change(self, e):
        # print()
        # print('search_change:', e)
        my_dict = {}
        results = None
        i = 0
        if e.control.data == 'decedent':
            i = 0
        elif e.control.data == 'heir':
            i = 1

        for control in self.page.session.get('/home').search_fields.controls[i].controls:
            if control.value:
                my_dict[control.label] = control.value

        if e.control.data == 'decedent':
            results = Decedent.get_customer(dict=my_dict, page=self.page)
        elif e.control.data == 'heir':
            results = Heir.get_customer(dict=my_dict, page=self.page)

        self.page.session.get('/home').customer_data_table(results)

    @classmethod
    def get_responsible_person_dropdown(cls):
        return ResponsiblePerson.get_responsible_person_dropdown()

    def responsible_person_change(self, e):
        print()
        print('responsible_person_change')

        if self.page.session.get('/home').ch_me_rep_person.value:
            self.page.session.get('/home').ch_me_rep_person.value = False

        if e.control.value == ' ':
            e.control.value = None
            self.page.session.get('/home').ch_me_rep_person.value = True

        self.search_change(e)

    def contractor_change(self, e):
        if self.page.session.get('/home').ch_contractor.value:
            self.page.session.get('/home').ch_contractor.value = False

        self.search_change(e)

    @classmethod
    def get_all_staff(cls, **kwargs):
        results = Staff.get_all_staff()
        return results

    def staff_registration_clicked(self, items):
        # 行削除したものをデータから削除
        # if delete_items
        print('items:', items)
        print(items[0].delete_item)
        container = items[0].controls[0].controls[0]
        content = container.content
        # for item in content.controls:
        #     print('item:', item.value, item)
        # Staff.upsert(content.controls)


def route_change(page: Page, e):
    print()
    print('route_change', e.route)

    if e.route == '/home' or e.route == '/settings':
        asyncio.new_event_loop().run_in_executor(None, utils.ime_on)

    # print(page.controls[0].controls[2].content.controls[0].content)
    # 戻るボタンが非表示の場合は表示する
    print('eb_return:', page.session.get('eb_return').content.visible)
    if not page.session.get('eb_return').content.visible and len(page.session.get('past_route')) > 0:
        page.session.get('eb_return').content.visible = True

    # routeを保存
    past_route = page.session.get('past_route')
    past_route.append(e.route)
    page.session.set('past_route', past_route)
    print('past_route:', page.session.get('past_route'))

    # サイドバーのインデックスを保存（戻るボタンを押したときに使用）
    page.session.get('past_selected_index')[e.route] = page.session.get('sideber').nav_rail.selected_index

    page.session.get('main_body').content = page.session.get(e.route)
    page.update()

    if e.route == '/home':
        page.session.get('main_body').content.tf_kana.focus()

    page.update()
