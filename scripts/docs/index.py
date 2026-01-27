#!/usr/bin/python3

"""
为 Zeraora 构建符号索引并生成 Markdown 文档。
"""

import inspect
from collections import defaultdict
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from types import ModuleType
from typing import Any

from typing_extensions import NamedTuple

# 拥有此属性的模块不会收录进索引，也不会出现在文档中。
DUNDER_UNRELEASED = '__unreleased__'

PROJECT_ROOT = Path(__file__).absolute().parent.parent.parent


@dataclass
class Template:
    """
    模板。存储模板位置和目标位置，提供模板加载与内容渲染。
    """

    source: Path
    """模板位置。"""

    target: Path
    """渲染结果输出位置。"""

    def __call__(self, **kwargs):
        with self.source.absolute().open('r', encoding='UTF-8') as f:
            template = f.read()
        with self.target.absolute().open('w', encoding='UTF-8') as f:
            f.write(template % kwargs)


class DocTemplateSet:
    symbols = Template(
        source=PROJECT_ROOT / './scripts/docs/symbols.template.md',
        target=PROJECT_ROOT / './docs/symbols.md',
    )
    modules = Template(
        source=PROJECT_ROOT / './scripts/docs/modules.template.md',
        target=PROJECT_ROOT / './docs/modules.md',
    )


class SymbolInfo(NamedTuple):
    module: ModuleType
    module_name: str
    symbol: Any
    symbol_name: str
    define: str
    kind: str

    @property
    def initial(self) -> str:
        return self.symbol_name[:1].upper()


class IndexGenerator:

    def __init__(self):
        self.symbols: list[SymbolInfo] = list()
        self.modules: dict[ModuleType, list[SymbolInfo]] = defaultdict(list)
        self.indexes: dict[str, list[SymbolInfo]] = defaultdict(list)

    @staticmethod
    def typeSymbol(symbol) -> tuple[str, str]:
        match inspect.isclass(symbol), inspect.isfunction(symbol):
            case True, _ if inspect.isabstract(symbol):
                return 'class', '抽象类'
            case True, _ if type in inspect.getmro(symbol):
                return 'class', '元类'
            case True, _ if {'__get__', '__set__'} <= set(symbol.__dict__):
                return 'class', '描述器类'
            case True, _:
                return 'class', ''

            case _, True if inspect.isgeneratorfunction(symbol):
                return 'def', '生成器函数'
            case _, True:
                return 'def', ''
            case _:
                return '', ''

    def scan(self):
        import zeraora

        # noinspection PyShadowingNames
        def find():
            yield zeraora, zeraora.__name__, '__version__'
            for symbol_name in dir(zeraora):
                if not symbol_name.startswith('_'):
                    yield zeraora, zeraora.__name__, symbol_name

            for _, module_name, _ in iter_modules(zeraora.__path__):
                module = import_module(f'{zeraora.__name__}.{module_name}')
                if hasattr(module, DUNDER_UNRELEASED):
                    continue
                for symbol_name in module.__all__:
                    yield module, module_name, symbol_name

        self.symbols = []
        for module, module_name, symbol_name in find():
            symbol = getattr(module, symbol_name)
            define, kind = self.typeSymbol(symbol)
            self.symbols.append(
                SymbolInfo(module, module_name, symbol, symbol_name, define, kind)
            )
        return self

    def part(self):
        self.modules.clear()
        self.indexes.clear()
        for info in self.symbols:
            self.modules[info.module].append(info)
            self.indexes[info.initial].append(info)
        self.indexes['特殊'] = self.indexes.pop('_', [])
        for array in self.indexes.values():
            array.sort(key=lambda t: t[3])
        return self

    def cook(self):
        from zeraora.string import StringBuilder

        builder = StringBuilder()
        for module, symbols in self.modules.items():
            builder.writeline(f'## <pre>{module.__name__}</pre> {{#{module.__name__}}}\n')
            for _, _, _, symbol_name, define, kind in symbols:
                builder.writeline(
                    f'- _{define}_ [`{symbol_name}`](/module/{module.__name__}#{symbol_name})，{kind}'
                    if define and kind else
                    f'- _{define}_ [`{symbol_name}`](/module/{module.__name__}#{symbol_name})'
                    if define else
                    f'- [`{symbol_name}`](/module/{module.__name__}#{symbol_name})'
                )
            else:
                builder.writeline()
        DocTemplateSet.modules(body=builder.build())

        builder = StringBuilder()
        builder.writeline('首字母', *[f'[{i}](#{i})' for i in sorted(self.indexes.keys())], sep=' ｜ ')
        builder.writeline()
        for initial in sorted(self.indexes.keys()):
            builder.writeline(f'## {initial}\n')
            for module, _, _, symbol_name, define, kind in self.indexes[initial]:
                builder.writeline(
                    f'- _{define}_ <pre>{module.__name__}.</pre>[`{symbol_name}`](/module/{module.__name__}#{symbol_name})，{kind}'
                    if define and kind else
                    f'- _{define}_ <pre>{module.__name__}.</pre>[`{symbol_name}`](/module/{module.__name__}#{symbol_name})'
                    if define else
                    f'- [](#) <pre>{module.__name__}.</pre>[`{symbol_name}`](/module/{module.__name__}#{symbol_name})'
                    # 这里如果不加“[](#)”会导致 HTML 后面的 Markdown 渲染失败
                )
            else:
                builder.writeline()
        DocTemplateSet.symbols(body=builder.build())

        return self


# noinspection PyPackageRequirements
def main():
    import django
    from django.conf import settings, global_settings

    settings.configure(
        global_settings,
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'rest_framework.authtoken',
        ],
    )
    django.setup()
    IndexGenerator().scan().part().cook()
    print('索引文档生成完毕。')


if __name__ == '__main__':
    main()
