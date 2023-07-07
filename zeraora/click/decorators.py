from functools import update_wrapper
from typing import Any, Callable

try:
    import click
except ImportError as e:
    raise ImportError('需要安装click框架：\npip install click') from e


def pass_context_without_exit(f: Callable[..., Any]) -> Callable[..., Any]:
    """
    将上下文作为被装饰的方法的第一个参数，并取消自动退出。（不能与 click.pass_context 连用）

    >>> import click
    >>>
    >>> @click.command('ratio')
    >>> @click.argument('argument')
    >>> @pass_context_without_exit
    >>> def calculating(ctx, argument):
    >>>     pass
    >>>
    >>> if __name__ == '__main__':
    >>>     calculating(['dummy'])
    >>>     print('calculate completed.')
    """

    def new_func(*args, **kwargs):
        ctx = click.get_current_context()
        ctx.exit = lambda: ()
        return f(ctx, *args, **kwargs)

    return update_wrapper(new_func, f)
