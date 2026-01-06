<script lang="ts" setup>
import Loading from '@/theme/asserts/loading.gif'
import { VPButton } from 'vitepress/theme'
</script>


<template>
    <div class="NotFound">
        <img :src="Loading" alt="转圈圈动画" draggable="false" style="user-select: none" />
        <p class="code">404</p>
        <div style="color: var(--vp-c-text-2)">
            小猫咪找不到页面喔<br />
            它可能已经在时间洪流中散佚了<br />
            请跟随小猫咪<br />
        </div>
        <VPButton draggable="false" href="/" text="回到首页" theme="sponsor" />
    </div>
</template>


<style scoped>
.NotFound {
    width: 100%;
    gap: 16px;
    display: inline-flex;
    padding: 64px 24px 96px;
    text-align: center;
    align-items: center;
    flex-direction: column;
    justify-content: center;
}

@media (min-width: 768px) {
    .NotFound {
        padding: 96px 32px 168px;
    }
}

.code {
    line-height: 64px;
    font-size: 64px;
    font-weight: 600;
}
</style>
