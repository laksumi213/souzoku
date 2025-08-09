from flet import (
    Page,
    Container,
    Divider,
    NavigationRailDestination,
    NavigationRail,
    icons,
    Row,
    colors,
    border_radius,
    alignment,
    CrossAxisAlignment,
    Text
)
# from state import State
# from customerselection import CustomerSelection
# from top import CustomerList
# from settings import Settings
# from labelcreate import Label


class SideBer(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.session.set('selected_index', 0)
        self.page.session.set('SideBer', self)

        self.nav_rail = NavigationRail(
            selected_index=0,
            height=self.page.window.height,
            destinations=[
                NavigationRailDestination(
                    icon=icons.MANAGE_ACCOUNTS,
                    label_content=Text("顧客一覧", color=colors.BLACK),
                    data='/home',
                ),
                NavigationRailDestination(
                    icon=icons.MANAGE_ACCOUNTS,
                    label_content=Text("手続き", color=colors.BLACK),
                    data='/home/procedure',
                ),
                NavigationRailDestination(
                    icon=icons.SETTINGS,
                    selected_icon=icons.SETTINGS,
                    label_content=Text("設定", color=colors.BLACK),
                    data='/settings'
                ),
            ],
            bgcolor=colors.AMBER_50,
            # on_change=lambda e: self.go_page(self.nav_rail)
            on_change=lambda e: self.go_page(self.nav_rail.destinations[self.nav_rail.selected_index].data)
            # on_change=lambda e: self.go_page(self.nav_rail.destinations[self.nav_rail.selected_index].data, self.nav_rail.selected_index)
        )

        self.content = Row(
            controls=[
                self.nav_rail,
                # Container(
                #     bgcolor=colors.BLACK26,
                #     border_radius=border_radius.all(30),
                #     height=480,
                #     alignment=alignment.center_right,
                #     width=2
                # ),
            ],
            expand=True,
            vertical_alignment=CrossAxisAlignment.START,
        )

    # def go_page(self, route, selected_index=None):
    #     print('')
    #     print('go_page:')
    #     # 戻るボタンが非表示の場合は表示する
    #     if not self.page.controls[0].controls[2].controls[0].content.visible:
    #         self.page.controls[0].controls[2].controls[0].content.visible = True
    #
    #     print('route:', route)
    #     # print("int(page.session.get('page_count')):", self.page.session.get('page_count'))
    #     # print("int(page.session.get('page_count')):", int(self.page.session.get('page_count')))
    #     # print(f'before_route_{self.page.session.get('page_count')}:',
    #     #       self.page.session.get(f'before_route_{self.page.session.get('page_count')}'))
    #     # print('before_route:', self.page.session.get(f'before_route_{int(self.page.session.get('page_count'))}'))
    #
    #     # self.page.go(e.destinations[e.selected_index].data)
    #     self.page.go(route)

    # def go_page(self, data, e):
    #     # 戻るボタンが非表示の場合は表示する
    #     if not self.page.controls[0].controls[2].controls[0].content.visible:
    #         self.page.controls[0].controls[2].controls[0].content.visible = True
    #
    #     self.page.session.set('before_selected_index', self.page.session.get('selected_index'))
    #     print('before_selected_index:', self.page.session.get('before_selected_index'))
    #     self.page.session.set('selected_index', e)
    #     print('selected_index:', self.page.session.get('selected_index'))
    #
    #     print('data:', data)
    #     self.page.go(data)