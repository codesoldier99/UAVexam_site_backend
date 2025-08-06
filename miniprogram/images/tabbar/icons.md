# TabBar 图标说明

由于无法直接创建 PNG 文件，请根据以下 SVG 代码创建对应的图标：

## 1. 二维码图标 (qrcode.png / qrcode-active.png)
```svg
<!-- 普通状态 -->
<svg width="48" height="48" viewBox="0 0 48 48" fill="none">
  <rect x="6" y="6" width="14" height="14" rx="2" stroke="#7A7E83" stroke-width="2"/>
  <rect x="28" y="6" width="14" height="14" rx="2" stroke="#7A7E83" stroke-width="2"/>
  <rect x="6" y="28" width="14" height="14" rx="2" stroke="#7A7E83" stroke-width="2"/>
  <rect x="9" y="9" width="8" height="8" rx="1" fill="#7A7E83"/>
  <rect x="31" y="31" width="8" height="8" rx="1" fill="#7A7E83"/>
  <rect x="9" y="31" width="8" height="8" rx="1" fill="#7A7E83"/>
</svg>

<!-- 激活状态 - 将 #7A7E83 替换为 #667eea -->
```

## 2. 考试安排图标 (schedule.png / schedule-active.png)
```svg
<!-- 普通状态 -->
<svg width="48" height="48" viewBox="0 0 48 48" fill="none">
  <rect x="8" y="10" width="32" height="30" rx="4" stroke="#7A7E83" stroke-width="2"/>
  <line x1="16" y1="6" x2="16" y2="14" stroke="#7A7E83" stroke-width="2"/>
  <line x1="32" y1="6" x2="32" y2="14" stroke="#7A7E83" stroke-width="2"/>
  <line x1="8" y1="18" x2="40" y2="18" stroke="#7A7E83" stroke-width="2"/>
  <circle cx="16" cy="26" r="2" fill="#7A7E83"/>
  <circle cx="24" cy="26" r="2" fill="#7A7E83"/>
  <circle cx="32" cy="26" r="2" fill="#7A7E83"/>
</svg>
```

## 3. 实时看板图标 (dashboard.png / dashboard-active.png)
```svg
<!-- 普通状态 -->
<svg width="48" height="48" viewBox="0 0 48 48" fill="none">
  <rect x="6" y="6" width="36" height="24" rx="4" stroke="#7A7E83" stroke-width="2"/>
  <rect x="10" y="34" width="8" height="8" rx="2" fill="#7A7E83"/>
  <rect x="20" y="34" width="8" height="8" rx="2" fill="#7A7E83"/>
  <rect x="30" y="34" width="8" height="8" rx="2" fill="#7A7E83"/>
  <line x1="12" y1="14" x2="36" y2="14" stroke="#7A7E83" stroke-width="2"/>
  <line x1="12" y1="20" x2="30" y2="20" stroke="#7A7E83" stroke-width="2"/>
</svg>
```

## 4. 个人信息图标 (profile.png / profile-active.png)
```svg
<!-- 普通状态 -->
<svg width="48" height="48" viewBox="0 0 48 48" fill="none">
  <circle cx="24" cy="16" r="8" stroke="#7A7E83" stroke-width="2"/>
  <path d="M8 40c0-8.837 7.163-16 16-16s16 7.163 16 16" stroke="#7A7E83" stroke-width="2"/>
</svg>
```

## 使用说明：
1. 将以上 SVG 代码保存为对应的 SVG 文件
2. 使用在线工具或设计软件将 SVG 转换为 48x48 像素的 PNG 文件
3. 为每个图标创建两个版本：
   - 普通状态：使用 #7A7E83 颜色
   - 激活状态：使用 #667eea 颜色
4. 将文件命名为：
   - qrcode.png / qrcode-active.png
   - schedule.png / schedule-active.png
   - dashboard.png / dashboard-active.png
   - profile.png / profile-active.png

## 临时解决方案：
如果暂时没有图标文件，可以先使用文字图标，修改 custom-tab-bar/index.js 中的配置。