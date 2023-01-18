import typing

from starlette.datastructures import URL, Headers
from starlette.responses import PlainTextResponse, RedirectResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

ENFORCE_DOMAIN_WILDCARD = "Domain wildcard patterns must be like '*.example.com'."


class BlockedHostMiddleware:
    """
    Middleware блокирует запросы из запрещенных подсетей (black list).

    app.add_middleware(
        BlockedHostMiddleware, blocked_hosts=['*', 'example.com', '*.example.com']
    )

    '*' Блокирует все хосты
    'example.com' Блокирует конкретный домен
    '*.example.com' Блокирует все адресы относяшиеся к домену
    """

    def __init__(
            self,
            app: ASGIApp,
            blocked_hosts: typing.Optional[typing.Sequence[str]] = None,
            www_redirect: bool = True,
    ) -> None:
        if blocked_hosts is None:
            blocked_hosts = []

        for pattern in blocked_hosts:
            assert "*" not in pattern[1:], ENFORCE_DOMAIN_WILDCARD
            if pattern.startswith("*") and pattern != "*":
                assert pattern.startswith("*."), ENFORCE_DOMAIN_WILDCARD
        self.app = app
        self.blocked_hosts = list(blocked_hosts)
        self.blocked_all = "*" in blocked_hosts
        self.www_redirect = www_redirect

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if self.blocked_all:
            await self.invalid_host(False, receive, scope, send)

        headers = Headers(scope=scope)
        host = headers.get("host", "").split(":")[0]
        is_valid_host = False
        found_www_redirect = False
        for pattern in self.blocked_hosts:
            if host == pattern or (pattern.startswith("*") and host.endswith(pattern[1:])):
                is_valid_host = True
                break
            elif "www." + host == pattern:
                found_www_redirect = True

        if is_valid_host:
            await self.invalid_host(found_www_redirect, receive, scope, send)
        else:
            await self.app(scope, receive, send)

    async def invalid_host(self, found_www_redirect, receive, scope, send):
        if found_www_redirect and self.www_redirect:
            url = URL(scope=scope)
            redirect_url = url.replace(netloc="www." + url.netloc)
            response = RedirectResponse(url=str(redirect_url))
        else:
            response = PlainTextResponse("Invalid host header", status_code=400)
        await response(scope, receive, send)
