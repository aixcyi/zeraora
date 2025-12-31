declare global {
    interface String {
        /**
         * 去除前缀。
         */
        trimPrefix(prefix?: string): string;

        /**
         * 去除前缀。
         */
        trimSuffix(suffix?: string): string;
    }
}
export {}
