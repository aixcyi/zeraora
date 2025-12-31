if (!String.prototype.trimPrefix) {
    String.prototype.trimPrefix = function (this: string, prefix?: string): string {
        if (!prefix)
            return this
        if (!this.startsWith(prefix))
            return this
        else
            return this.substring(prefix.length)
    }
}
if (!String.prototype.trimSuffix) {
    String.prototype.trimSuffix = function (this: string, suffix?: string): string {
        if (!suffix)
            return this
        if (!this.endsWith(suffix))
            return this
        else
            return this.substring(0, this.length - suffix.length)
    }
}