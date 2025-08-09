# from components.header import AppHeader
# from app.sideber import SideBer
from app.views.views import SideBer, HomeView
# from app.body import HomeBody
from flet import (
    Row,
    Page,
    MainAxisAlignment,
    CrossAxisAlignment,
    VerticalDivider,
    colors,
    Text,
    Column,
    Container,
    ElevatedButton,
    ButtonStyle,
    icons,
)


class MyLayout(Row):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.alignment = MainAxisAlignment.START
        self.vertical_alignment = CrossAxisAlignment.START
        self.expand = True
        # AppHeader(page, 'WEB LAYOUT')

        home_view = Container(
            content=HomeView(page),
            expand=True,  # 残りのスペースを埋める
        )
        page.session.set('home_view', home_view)

        self.eb_return = Container(
            content=ElevatedButton(
                "戻る",
                # style=ButtonStyle(
                #     padding=20,
                #     color=colors.BLUE,
                #     bgcolor=colors.WHITE,
                # ),
                icon=icons.ARROW_BACK,
                # visible=True,
                visible=False,
                on_click=self.return_clicked
            ),
            margin=5,
        )

        self.controls = [
            SideBer(self.page),
            Container(height=self.page.window_height, content=VerticalDivider(thickness=1, color=colors.BLACK)),
            Column([
                self.eb_return,
                self.page.session.get('home_view')
            ])
        ]

    def return_clicked(self, e):
        print('')
        print('return_clicked:')
        # print(self.controls[0].nav_rail)
        # print('self.page.route:', self.page.route)
        # print('self.page.parent:', self.page.parent)
        # print('self.page.parent:', self.page.parent.controls)
        # print('self.page.url:', self.page.url)
        # print("int(page.session.get('page_count')):", int(self.page.session.get('page_count')))
        print('route:', self.page.session.get(f'before_route_{int(self.page.session.get('page_count'))}'))
        self.page.session.remove(f"before_route_{self.page.session.get('page_count')}")
        SideBer.go_page(self.page.session.get('SideBer'), self.page.session.get(f'before_route_{int(self.page.session.get('page_count'))}'))

        # SideBer.go_page(self.page.session.get('SideBer'), self.controls[0].nav_rail)

        # # self.controls[0].nav_rail.selected_index = self.page.session.get('before_selected_index')
        # self.controls[0].content.controls[0].selected_index = self.page.session.get('before_selected_index')
        #
        # self.controls[2].controls[1].content = self.page.session.get('before_content')
        #
        # self.update()
        # print('self.controls[0].content:', self.controls[0].content.controls[0].selected_index)
        # # self.page.update()
        #
        # print('before_selected_index', self.page.session.get('before_selected_index'))
        #
        # # self.page.session.set('before_selected_index', self.controls[0].nav_rail.selected_index)
        # self.page.session.set('selected_index', self.controls[0].nav_rail.selected_index)
        # print('selected_index', self.page.session.get('selected_index'))