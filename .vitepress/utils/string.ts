export function trimPrefix(s: undefined, prefix?: string): undefined;
export function trimPrefix(s: string, prefix?: string): string;
export function trimPrefix(s?: string, prefix?: string) {
    if (s === undefined)
        return undefined
    if (!prefix)
        return s
    if (!s.startsWith(prefix))
        return s
    else
        return s.substring(prefix.length)
}

export function trimSuffix(s: undefined, suffix?: string): undefined;
export function trimSuffix(s: string, suffix?: string): string;
export function trimSuffix(s?: string, suffix?: string) {
    if (s === undefined)
        return undefined
    if (!suffix)
        return s
    if (!s.endsWith(suffix))
        return s
    else
        return s.substring(0, s.length - suffix.length)
}
