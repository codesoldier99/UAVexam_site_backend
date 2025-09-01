import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import relativeTime from 'dayjs/plugin/relativeTime'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'

// 配置 dayjs
dayjs.locale('zh-cn')
dayjs.extend(relativeTime)
dayjs.extend(utc)
dayjs.extend(timezone)

/**
 * 格式化日期时间
 * @param date 日期字符串或Date对象
 * @param format 格式化模板，默认 'YYYY-MM-DD HH:mm:ss'
 * @returns 格式化后的日期字符串
 */
export const formatDateTime = (
  date: string | Date | null | undefined,
  format: string = 'YYYY-MM-DD HH:mm:ss'
): string => {
  if (!date) return '-'
  return dayjs(date).format(format)
}

/**
 * 格式化日期
 * @param date 日期字符串或Date对象
 * @param format 格式化模板，默认 'YYYY-MM-DD'
 * @returns 格式化后的日期字符串
 */
export const formatDate = (
  date: string | Date | null | undefined,
  format: string = 'YYYY-MM-DD'
): string => {
  if (!date) return '-'
  return dayjs(date).format(format)
}

/**
 * 格式化时间
 * @param date 日期字符串或Date对象
 * @param format 格式化模板，默认 'HH:mm:ss'
 * @returns 格式化后的时间字符串
 */
export const formatTime = (
  date: string | Date | null | undefined,
  format: string = 'HH:mm:ss'
): string => {
  if (!date) return '-'
  return dayjs(date).format(format)
}

/**
 * 获取相对时间
 * @param date 日期字符串或Date对象
 * @returns 相对时间字符串，如 "2小时前"
 */
export const getRelativeTime = (date: string | Date | null | undefined): string => {
  if (!date) return '-'
  return dayjs(date).fromNow()
}

/**
 * 判断是否为今天
 * @param date 日期字符串或Date对象
 * @returns 是否为今天
 */
export const isToday = (date: string | Date | null | undefined): boolean => {
  if (!date) return false
  return dayjs(date).isSame(dayjs(), 'day')
}

/**
 * 判断是否为本周
 * @param date 日期字符串或Date对象
 * @returns 是否为本周
 */
export const isThisWeek = (date: string | Date | null | undefined): boolean => {
  if (!date) return false
  return dayjs(date).isSame(dayjs(), 'week')
}

/**
 * 判断是否为本月
 * @param date 日期字符串或Date对象
 * @returns 是否为本月
 */
export const isThisMonth = (date: string | Date | null | undefined): boolean => {
  if (!date) return false
  return dayjs(date).isSame(dayjs(), 'month')
}

/**
 * 获取日期范围
 * @param startDate 开始日期
 * @param endDate 结束日期
 * @returns 日期范围字符串
 */
export const getDateRange = (
  startDate: string | Date | null | undefined,
  endDate: string | Date | null | undefined
): string => {
  if (!startDate || !endDate) return '-'
  const start = formatDate(startDate)
  const end = formatDate(endDate)
  return `${start} ~ ${end}`
}

/**
 * 计算两个日期之间的天数差
 * @param date1 日期1
 * @param date2 日期2
 * @returns 天数差
 */
export const getDaysDiff = (
  date1: string | Date | null | undefined,
  date2: string | Date | null | undefined
): number => {
  if (!date1 || !date2) return 0
  return dayjs(date1).diff(dayjs(date2), 'day')
}

/**
 * 获取当前时间戳
 * @returns 当前时间戳（毫秒）
 */
export const getCurrentTimestamp = (): number => {
  return dayjs().valueOf()
}

/**
 * 时间戳转日期
 * @param timestamp 时间戳（毫秒）
 * @param format 格式化模板
 * @returns 格式化后的日期字符串
 */
export const timestampToDate = (
  timestamp: number,
  format: string = 'YYYY-MM-DD HH:mm:ss'
): string => {
  return dayjs(timestamp).format(format)
}

/**
 * 日期转时间戳
 * @param date 日期字符串或Date对象
 * @returns 时间戳（毫秒）
 */
export const dateToTimestamp = (date: string | Date): number => {
  return dayjs(date).valueOf()
}

/**
 * 获取本周开始和结束日期
 * @returns { start: string, end: string }
 */
export const getThisWeekRange = (): { start: string; end: string } => {
  const start = dayjs().startOf('week').format('YYYY-MM-DD')
  const end = dayjs().endOf('week').format('YYYY-MM-DD')
  return { start, end }
}

/**
 * 获取本月开始和结束日期
 * @returns { start: string, end: string }
 */
export const getThisMonthRange = (): { start: string; end: string } => {
  const start = dayjs().startOf('month').format('YYYY-MM-DD')
  const end = dayjs().endOf('month').format('YYYY-MM-DD')
  return { start, end }
}

/**
 * 获取最近N天的日期范围
 * @param days 天数
 * @returns { start: string, end: string }
 */
export const getRecentDaysRange = (days: number): { start: string; end: string } => {
  const end = dayjs().format('YYYY-MM-DD')
  const start = dayjs().subtract(days - 1, 'day').format('YYYY-MM-DD')
  return { start, end }
}

export default {
  formatDateTime,
  formatDate,
  formatTime,
  getRelativeTime,
  isToday,
  isThisWeek,
  isThisMonth,
  getDateRange,
  getDaysDiff,
  getCurrentTimestamp,
  timestampToDate,
  dateToTimestamp,
  getThisWeekRange,
  getThisMonthRange,
  getRecentDaysRange
}