from injector import Module, provider

from yandex_music import Client as YandexMusicAPI


class YandexMusicAPITokenAuthModule(Module):
    def __init__(self, token: str) -> None:
        self._token = token

    @provider
    def provide_api(self) -> YandexMusicAPI:
        YandexMusicAPI.notice_displayed = True
        return YandexMusicAPI(token=self._token)
