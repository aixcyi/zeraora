import { type PageHooks, VitePressConfigurator } from './utils/vitepress'
import { trimSuffix } from './utils/string'


// https://vitepress.dev/zh/reference/site-config
const configurator = new VitePressConfigurator({
    srcDir: './docs',
    outDir: './dist-docs',
    cacheDir: './cache',
    srcExclude: [
        './cache',
        './dist*',
        './venv*',
        './test',
        './zeraora',
        '**/README.md',
        '**/*.template.md',
    ],
    base: '/zeraora/',
    head: [
        [ 'link', { rel: 'icon', href: '/favicon.ico', type: 'image/ico' } ],
        [ 'link', {
            rel: 'stylesheet',
            href: 'https://cdn-font.hyperos.mi.com/font/css?family=MiSans_VF:VF:Chinese_Simplify,Latin&display=swap'
        } ],
    ],
    locales: {
        root: {
            lang: 'zh-CN',
            label: '简体中文',
            title: "Zeraora",
            titleTemplate: ":title × Zeraora",
            description: "Zeraora 文档",
            themeConfig: {
                // https://vitepress.dev/zh/reference/default-theme-config
                langMenuLabel: '切换语言',
                sidebarMenuLabel: '目录',
                darkModeSwitchLabel: '颜色主题',
                darkModeSwitchTitle: '切换到深色主题',
                lightModeSwitchTitle: '切换到浅色主题',
                returnToTopLabel: '回到顶部',
                outline: { label: '大纲' },
                editLink: {
                    text: '前往 GitHub 编辑此页',
                    pattern: 'https://github.com/aixcyi/Zeraora/tree/main/docs/:path',
                },
                docFooter: { prev: '上一篇', next: '下一篇' },
                lastUpdated: {
                    text: '最后提交时间',
                    formatOptions: { dateStyle: 'full', timeStyle: 'medium' }
                },
                nav: [],
                sidebar: {},
                socialLinks: [
                    { icon: 'github', link: 'https://github.com/aixcyi/Zeraora', ariaLabel: 'GitHub 仓库' },
                    { icon: 'qq', link: 'https://qm.qq.com/q/9RfmeydwNq', ariaLabel: 'QQ 群' },
                ],
            },
        },
    },
    lastUpdated: true,
    markdown: {
        theme: {
            light: 'catppuccin-macchiato',
            dark: 'catppuccin-macchiato',
        },
        anchor: {
            slugify(str: string): string {
                // 匹配 "# title ｛#fragement｝" 这样的结构
                let result;
                result = str.match(/^.*\{#(\w+)}$/)
                if (result) {
                    return result[1]
                }
                // 匹配 "# function(*args, **kwargs)" 这样的结构
                result = str.match(/^(\w+)\([^)]*\)$/)
                if (result) {
                    return result[1]
                }
                // 避免 VitePress 将 '__init__' 编译成 'init'
                return str
            },
        },
        container: {
            tipLabel: '提示',
            warningLabel: '注意',
            dangerLabel: '当心',
            infoLabel: '信息',
            detailsLabel: '详细信息',
        },
    },
    vite: {
        resolve: {
            alias: {
                '@': __dirname,
            },
        },
    },
}, {
    compareFolder: (a, b) => a.url.localeCompare(b.url),
    compareFile: (a, b) => trimSuffix(a.url, '.html').localeCompare(trimSuffix(b.url, '.html')),
    compareItem: () => 1,
})

const hooksOrdered: PageHooks = {
    compareFile: (a, b) => a.frontmatter.order - b.frontmatter.order,
}

configurator
    .goto('root')
    .autoSidebar('/', './docs/', { hooks: hooksOrdered })
    .autoSidebar('/module/', './docs/module/', { deep: true })
    .autoNavMenu('./docs/module/')
    .pushNavLink({ text: '模块索引', link: '/modules' })
    .pushNavLink({ text: '符号索引', link: '/symbols' })
    .pushNavLink({ text: '更新日志', link: '/changelog' })
    .pushNavMenu({
        text: '更多',
        items: [
            { text: '发行说明', link: '/releases' },
            { text: '如何参与贡献？', link: '/contributing' },
            { text: '路狐领航', link: 'https://www.navifox.net/' },
            { text: '文档月饼盒', link: 'https://docs.navifox.net/' },
        ],
    })

export default configurator.define()
