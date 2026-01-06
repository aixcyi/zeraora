// https://vitepress.dev/guide/custom-theme
import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme-without-fonts'
import { h } from 'vue'
import '@catppuccin/vitepress/theme/macchiato/maroon.css'
import NotFound from './NotFound.vue'
import './style/index.css'
import './style/fonts.css'
import './style/custome-block.css'


export default {
    extends: DefaultTheme,
    Layout: () => {
        return h(DefaultTheme.Layout, null, {
            // https://vitepress.dev/guide/extending-default-theme#layout-slots
            'not-found': () => h(NotFound),
        })
    },
    enhanceApp({ app, router, siteData }) {
        // ...
    }
} satisfies Theme
