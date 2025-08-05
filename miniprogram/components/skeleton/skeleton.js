Component({
  properties: {
    // 是否显示骨架屏
    show: {
      type: Boolean,
      value: false
    },
    // 骨架屏类型：dashboard, list, cards, table, stats
    type: {
      type: String,
      value: 'list'
    },
    // 行数
    rows: {
      type: Number,
      value: 3
    },
    // 列数（表格用）
    columns: {
      type: Number,
      value: 3
    },
    // 文本行数
    lines: {
      type: Number,
      value: 1
    },
    // 是否显示头像
    avatar: {
      type: Boolean,
      value: false
    },
    // 是否显示副标题
    subtitle: {
      type: Boolean,
      value: false
    },
    // 自定义高度
    height: {
      type: String,
      value: 'auto'
    }
  },

  data: {
    
  },

  methods: {
    
  }
})