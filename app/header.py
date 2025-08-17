from flet import (
    AppBar,
    colors,
    Icon,
    icons,
    Page,
    Text,
    TextAlign
)


class AppHeader(AppBar):
    def __init__(self, page: Page, page_title: str = "遺言・相続管理システム Ver1.0.0"):
        super().__init__()
        self.page = page
        self.page_title = page_title

        self.page.appbar = AppBar(
            leading=Icon(icons.TRIP_ORIGIN_ROUNDED),
            leading_width=100,
            title=Text(value=self.page_title, size=32, text_align=TextAlign.CENTER),
            center_title=False,
            toolbar_height=75,
            bgcolor=colors.SURFACE_VARIANT,
        )
