import type {integer} from '@vue/language-server'
import * as glob from 'glob'
import matter from 'gray-matter'
import fs from 'node:fs'
import * as pathlib from 'path'
import {compile, match} from 'path-to-regexp'
import {normalizePath} from 'vite'
import {type DefaultTheme, defineConfig, type UserConfig} from 'vitepress'
import MarkdownIt from 'markdown-it'


/**
 * 编译 `UserConfig<DefaultTheme.Config>['rewrites']` 并返回重写函数。
 */
function compileRewrites(rewrites: UserConfig['rewrites']) {
    switch (typeof rewrites) {
        case "object":
            const rewriteRules = Object.entries(rewrites || {}).map(
                ([from, to]) => {
                    return {
                        toPath: compile(to),
                        matchUrl: match(from),
                    }
                }
            )
            return (page: string) => {
                for (const {matchUrl, toPath} of rewriteRules) {
                    const res = matchUrl(page)
                    if (res) {
                        return toPath(res.params)
                    }
                }
                return page
            }
        case "function":
            return rewrites
        default:
            return (page: string) => page
    }
}


/**
 * Markdown 文件解析得到的页面信息。
 */
export class Page {

    constructor(public readonly url: string,
                public readonly filepath: string,
                public readonly frontmatter: Record<string, any>,
                public depth: integer = 0,
                public isIndex: boolean = false) {
        this.frontmatter = {...frontmatter}
    }
}


/**
 * 页面信息处理的相关钩子。
 */
export type PageHooks = {

    /**
     * 比较所有文件夹（即所有 xxx/index.md）。
     */
    compareFolder?: (a: Page, b: Page) => number,

    /**
     * 比较所有文件（除了 xxx/index.md）。
     */
    compareFile?: (a: Page, b: Page) => number,

    /**
     * 比较文件与文件夹（即 xxx/index.md）。
     */
    compareItem?: (a: Page, b: Page) => number,
}


export class VitePressConfigurator {
    private pages: Page[] = []
    private locale: string = 'root'

    /**
     * VitePress 配置器。
     *
     * @param configs VitePress 配置。
     * @param hooks 全局排序钩子。可以在单次操作中被覆盖。
     */
    constructor(private configs: UserConfig<DefaultTheme.Config>,
                private hooks?: PageHooks) {
        const markdown = MarkdownIt()
        const rewrite = compileRewrites(this.configs.rewrites)
        const base = this.configs.srcDir ?? '.'
        const pages: Page[] = []
        const files: string[] = glob.sync(['**/**.md'], {
            cwd: this.configs.srcDir ?? '.',
            nodir: true,
            absolute: true,
            ignore: [
                '**/node_modules/**',
                '**/dist/**',
                ...(this.configs.srcExclude ?? []),
            ],
        })
        for (const file of files) {
            const url = normalizePath(
                rewrite(
                    pathlib.relative(base, file).replace(/\\/g, '/')
                )
            ).replace(
                /(^|\/)index\.md$/, '$1'
            ).replace(
                /\.md$/, this.configs.cleanUrls ? '' : '.html'
            )
            const {data: frontmatter} = matter(fs.readFileSync(file, 'utf-8'))
            if (!('title' in frontmatter))
                continue
            // VitePress 将其作为网页标题时会自动编译，因此捞数据的时候也必须编译一次。
            frontmatter.title = markdown.renderInline(frontmatter.title)
            pages.push(new Page(url, file, frontmatter))
        }
        this.pages = pages
    }

    /**
     * 切换要操作的 `local`。
     */
    public goto(local: string = 'root') {
        this.locale = local
        return this
    }

    /**
     * 手动追加一个导航（链接）。
     */
    public pushNavLink(nav: DefaultTheme.NavItemWithLink) {
        this.configs.locales[this.locale].themeConfig.nav.push(nav)
        return this
    }

    /**
     * 手动追加一个导航菜单。
     */
    public pushNavMenu(nav: DefaultTheme.NavItemWithChildren) {
        this.configs.locales[this.locale].themeConfig.nav.push(nav)
        return this
    }

    /**
     * 自动追加一批导航（链接），平铺在导航栏上。
     *
     * @param dir 需要搜索哪个目录下的 Markdown。
     * @param options 可选参数。
     * @param options.hooks 排序钩子。
     */
    public autoNavLinks(dir: string, options?: { hooks?: PageHooks }) {
        this.part(dir, options?.hooks).files.map(page => ({
            text: page.frontmatter.title,
            link: `/${page.url}`,
        })).forEach(nav => {
            this.pushNavLink(nav)
        })
        return this
    }

    /**
     * 自动追加一个导航菜单。
     *
     * @param dir 需要搜索哪个目录下的 Markdown。
     * @param options 可选参数。
     * @param options.text 菜单的标题，不指定则使用 `index.md` 的 `title` 字段。
     * @param options.deep 是否递归搜索该目录。
     * @param options.hooks 排序钩子。
     */
    public autoNavMenu(dir: string, options?: { text?: string, deep?: boolean, hooks?: PageHooks }) {
        if (!options?.deep) {
            const {files, index} = this.part(dir, options?.hooks)
            this.pushNavMenu({
                text: options?.text ?? index?.frontmatter?.title ?? '(无标题)',
                items: files.map(page => ({
                    text: page.frontmatter.title,
                    link: `/${page.url}`,
                }))
            })
        } else {
            const {text, items} = this.deepNav(dir, options?.hooks)
            this.pushNavMenu({
                text: options?.text ?? text ?? '(无标题)',
                items,
            })
        }
        return this
    }

    /**
     * 手动追加一个侧边栏。
     *
     * @param path 侧边栏在哪个 URL 路径下触发。
     * @param sidebar 侧边栏数据。
     */
    public pushSidebar(path: string, sidebar: DefaultTheme.SidebarItem[]) {
        this.configs.locales[this.locale].themeConfig.sidebar[path] = sidebar
        return this
    }

    /**
     * 自动追加一个侧边栏。
     *
     * @param path 侧边栏在哪个 URL 路径下触发。
     * @param dir 需要展示哪个目录下的 Markdown。
     * @param options 可选参数。
     * @param options.collapsed 是否收起当前目录。子目录会使用当前目录的设置。
     * @param options.deep 是否递归搜索该目录。
     * @param options.hooks 排序钩子。
     */
    public autoSidebar(
        path: string,
        dir: string,
        options?: { collapsed?: boolean, deep?: boolean, hooks?: PageHooks },
    ) {
        if (!options?.deep) {
            const {files} = this.part(dir, options?.hooks)
            this.pushSidebar(path, files.map(
                page => ({text: page.frontmatter.title, link: `/${page.url}`})
            ))
        } else {
            this.pushSidebar(path, this.deepSidebar(
                dir, options?.collapsed, options?.hooks,
            ))
        }
        return this
    }

    /**
     * 返回 VitePress 构建好的配置。
     */
    public define() {
        return defineConfig(this.configs)
    }

    /**
     * 从整个项目中，提取目标目录下的子孙 Markdown 文件（夹）：
     *
     * - 所有子孙文件夹 `folders`
     * - 所有子孙文件 `files`
     * - 所有子孙文件（夹）`items`
     * - 首页 `index`
     */
    private part(dir: string, hooks?: PageHooks) {
        const root = pathlib.join(pathlib.resolve(dir), '/')
        const pages = this.pages.filter(page => page.filepath.startsWith(root))
        for (const page of pages) {
            const parts = page.filepath.slice(root.length).split(/[\\/]/)
            page.depth = parts.length - 1
            page.isIndex = parts[page.depth].match(/^index\.md$/) !== null
        }
        const folders = pages
            .filter(page => page.depth === 1 && page.isIndex)
            .sort((hooks ?? this.hooks)?.compareFolder)
        const files = pages
            .filter(page => page.depth === 0 && !page.isIndex)
            .sort((hooks ?? this.hooks)?.compareFile)
        const index = pages
            .filter(page => page.depth === 0 && page.isIndex)[0]
        const items = [...folders, ...files]
            .sort((hooks ?? this.hooks)?.compareItem)
        return {
            folders, files, items, index,
        }
    }

    private deepNav(dir: string, hooks?: PageHooks) {
        const {items: pages, index} = this.part(dir, hooks)
        const items = []
        for (const page of pages) {
            if (!page.isIndex)
                items.push({text: page.frontmatter.title, link: `/${page.url}`})
            else
                items.push(this.deepNav(pathlib.join(page.filepath, '../'), hooks))
        }
        return {
            text: index?.frontmatter?.title,
            items,
        }
    }

    private deepSidebar(dir: string, collapsed?: boolean, hooks?: PageHooks) {
        const {items: pages} = this.part(dir, hooks)
        const items: DefaultTheme.SidebarItem[] = []
        for (const page of pages) {
            if (!page.isIndex)
                items.push({
                    text: page.frontmatter.title,
                    link: `/${page.url}`,
                })
            else
                items.push({
                    text: page.frontmatter.title,
                    items: this.deepSidebar(pathlib.join(page.filepath, '../'), collapsed, hooks),
                    collapsed: collapsed,
                })
        }
        return items
    }
}
