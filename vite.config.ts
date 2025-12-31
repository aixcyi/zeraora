import {resolve} from 'path'
import {defineConfig} from 'vite'


// https://vite.dev/config/
export default defineConfig({
    plugins: [],
    resolve: {
        alias: {
            '@': resolve(__dirname, './.vitepress'),
        },
    },
    css: {
        preprocessorOptions: {
            scss: {api: 'modern-compiler'},
        },
    }
})
