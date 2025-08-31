// pages/candidate/qrcode/qrcode-enhanced.js
const app = getApp();
const api = require('../../../utils/api');

console.log('qrcode-enhanced: 开始导入QRCode模块');
try {
  const qrModule = require('../../../utils/weapp-qrcode.js');
  console.log('qrcode-enhanced: QRCode模块导入成功', qrModule);
  const { QRCode, QRErrorCorrectLevel } = qrModule;
  console.log('qrcode-enhanced: QRCode构造函数', QRCode);
  console.log('qrcode-enhanced: QRErrorCorrectLevel', QRErrorCorrectLevel);
} catch (error) {
  console.error('qrcode-enhanced: QRCode模块导入失败', error);
}

const { QRCode, QRErrorCorrectLevel } = require('../../../utils/weapp-qrcode.js');

Page({
  data: {
    loading: true,
    candidateInfo: null,
    qrCodeText: '',
    qrCodeGenerated: false,
    errorMessage: '',
    refreshInterval: 60000, // 1 minute refresh interval
    lastRefreshTime: '',
    countdown: 60,
    showCountdown: false,
    canvasRefreshKey: 0,
    refreshing: false // 刷新状态
  },

  onLoad: function() {
    console.log('=== qrcode-enhanced页面onLoad开始 ===');
    console.log('页面数据初始状态:', this.data);
    
    this.loadData();
    // Set up auto-refresh timer
    this.setRefreshTimer();
    
    console.log('=== qrcode-enhanced页面onLoad完成 ===');
  },

  onUnload: function() {
    // Clear the refresh timer when leaving the page
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }
    if (this.countdownTimer) {
      clearInterval(this.countdownTimer);
    }
  },

  onShow: function() {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({
        selected: 0
      });
    }
    
    // If we already have data but it might be stale, refresh it
    if (this.data.candidateInfo && !this.data.loading) {
      this.loadData();
    }
  },

  loadData: function() {
    console.log('loadData: 开始加载数据');
    this.setData({
      loading: true,
      errorMessage: ''
    });

    // 从本地存储获取考生信息
    const candidateInfo = wx.getStorageSync('candidateInfo');
    const candidateId = wx.getStorageSync('candidateId');
    
    console.log('loadData: 获取到的考生信息', candidateInfo);
    console.log('loadData: 获取到的考生ID', candidateId);
    
    if (!candidateInfo || !candidateId) {
      console.log('loadData: 缺少考生信息，显示错误');
      this.setData({
        loading: false,
        errorMessage: '未找到考生信息，请重新登录'
      });
      return;
    }

    // 使用本地存储的考生信息
    this.setData({
      candidateInfo: candidateInfo,
      loading: false
    });
    
    console.log('loadData: 开始生成二维码');
    // 生成二维码
    this.generateQRCode();
    
    // 更新最后刷新时间
    const now = new Date();
    this.setData({
      lastRefreshTime: now.toLocaleTimeString()
    });
    
    // 开始倒计时
    this.startCountdown();
  },


  generateQRCode: function() {
    console.log('generateQRCode: 开始生成二维码');
    try {
      const { candidateInfo } = this.data;
      console.log('generateQRCode: 当前考生信息', candidateInfo);
      
      if (!candidateInfo) {
        console.log('generateQRCode: 缺少考生信息');
        throw new Error('缺少生成二维码所需的考生信息');
      }
      
      // 从本地存储获取完整的考生信息，包括身份证
      const storedCandidateInfo = wx.getStorageSync('candidateInfo');
      console.log('generateQRCode: 本地存储的完整考生信息', storedCandidateInfo);
      
      // 🆕 获取考试安排信息
      const currentExam = wx.getStorageSync('currentExam');
      console.log('generateQRCode: 当前考试安排信息', currentExam);
      
      // Create QR code data - 包含考试安排信息
      // 🔧 修正姓名获取逻辑，优先从存储的完整信息中获取
      let candidateName = storedCandidateInfo?.full_name || 
                         storedCandidateInfo?.name || 
                         candidateInfo.full_name || 
                         candidateInfo.name;
      
      // 清理姓名中的空白字符，如果清理后为空则使用默认值
      candidateName = candidateName ? candidateName.trim() : '';
      if (!candidateName) {
        console.warn('考生姓名为空，使用默认值');
        candidateName = '考生';
      }
      
      console.log('最终使用的考生姓名:', candidateName);
      
      // 🔧 简化方案：使用URL编码处理中文字符，避免数据过长
      const encodedName = encodeURIComponent(candidateName);
      console.log('URL编码后的姓名:', encodedName);
      
      const qrData = {
        candidate_id: candidateInfo.id,
        name: encodedName, // 使用URL编码的姓名
        id_card: storedCandidateInfo?.id_card || candidateInfo.id_card || '未提供',
        username: candidateInfo.username || storedCandidateInfo?.username || `candidate_${candidateInfo.id}`,
        // 🆕 添加考试安排信息
        schedule_id: currentExam?.schedule_id || null,
        venue_id: currentExam?.venue_id || null,
        exam_session: currentExam?.exam_session || 'morning', // 添加考试场次
        exam_date: currentExam?.exam_date || null,
        timestamp: new Date().getTime(),
        type: 'candidate_checkin'
      };
      
      // 验证关键信息是否存在
      if (!qrData.schedule_id || !qrData.venue_id) {
        console.warn('二维码缺少考试安排信息:', {
          schedule_id: qrData.schedule_id,
          venue_id: qrData.venue_id
        });
      }
      
      console.log('generateQRCode: 二维码数据', qrData);
      
      // Convert to JSON string
      const qrCodeText = JSON.stringify(qrData);
      console.log('generateQRCode: 二维码文本长度', qrCodeText.length);
      console.log('generateQRCode: 二维码文本内容', qrCodeText);
      
      this.setData({
        qrCodeText: qrCodeText
      });
      
      // 确保Canvas元素已准备就绪
      // 简化Canvas处理，直接生成QR码
      console.log('generateQRCode: 开始创建QRCode实例');
      
      // 添加短暂延迟确保页面渲染完成
      setTimeout(() => {
        try {
          // Create QR code instance - 平衡数据长度和纠错能力
          const qrCodeInstance = new QRCode('qrcode', {
            text: qrCodeText,
            width: 200,
            height: 200,
            colorDark: '#000000',
            colorLight: '#ffffff',
            correctLevel: QRErrorCorrectLevel.L, // 使用低纠错级别，减少数据量
            callback: () => {
              console.log('generateQRCode: 二维码生成成功回调');
              this.setData({
                qrCodeGenerated: true
              });
            }
          });
          
          console.log('generateQRCode: QRCode实例创建完成', qrCodeInstance);
          
          // 备用成功检查
          setTimeout(() => {
            if (!this.data.qrCodeGenerated) {
              console.log('generateQRCode: 回调未执行，手动设置生成状态');
              this.setData({
                qrCodeGenerated: true
              });
            }
          }, 1000);
          
        } catch (qrError) {
          console.error('generateQRCode: QRCode实例创建失败', qrError);
          this.setData({
            errorMessage: '二维码创建失败: ' + qrError.message
          });
        }
      }, 200);
      
    } catch (error) {
      console.error('generateQRCode: 生成二维码时发生错误', error);
      console.error('generateQRCode: 错误堆栈', error.stack);
      this.setData({
        errorMessage: '生成二维码失败: ' + error.message
      });
    }
  },

  refreshQRCode: function() {
    // 设置刷新状态
    this.setData({
      refreshing: true
    });
    
    // 延迟一下显示刷新效果
    setTimeout(() => {
      this.loadData();
      // 刷新完成后重置状态
      setTimeout(() => {
        this.setData({
          refreshing: false
        });
      }, 500);
    }, 300);
  },

  setRefreshTimer: function() {
    // Clear any existing timer
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }
    
    // Set up a new timer to refresh every minute
    this.refreshTimer = setInterval(() => {
      this.refreshQRCode();
    }, this.data.refreshInterval);
  },

  startCountdown: function() {
    // Clear any existing countdown
    if (this.countdownTimer) {
      clearInterval(this.countdownTimer);
    }
    
    // Reset countdown
    this.setData({
      countdown: 60,
      showCountdown: true
    });
    
    // Start countdown timer
    this.countdownTimer = setInterval(() => {
      let countdown = this.data.countdown - 1;
      
      if (countdown <= 0) {
        clearInterval(this.countdownTimer);
        this.setData({
          showCountdown: false
        });
      } else {
        this.setData({
          countdown: countdown
        });
      }
    }, 1000);
  },

  ensureCanvasReady: function(callback) {
    console.log('ensureCanvasReady: 检查Canvas是否准备就绪');
    
    // 使用wx.createSelectorQuery检查Canvas元素
    const query = wx.createSelectorQuery();
    query.select('#qrcode').boundingClientRect((rect) => {
      console.log('ensureCanvasReady: Canvas元素信息', rect);
      
      if (rect && rect.width > 0 && rect.height > 0) {
        console.log('ensureCanvasReady: Canvas已准备就绪');
        callback();
      } else {
        console.log('ensureCanvasReady: Canvas未准备就绪，延迟重试');
        setTimeout(() => {
          this.ensureCanvasReady(callback);
        }, 100);
      }
    }).exec();
  },

  forceCanvasRedraw: function() {
    console.log('forceCanvasRedraw: 强制Canvas重绘');
    
    // 方法1: 通过修改Canvas的display样式触发重绘
    const query = wx.createSelectorQuery();
    query.select('#qrcode').context((res) => {
      console.log('forceCanvasRedraw: Canvas上下文', res);
    }).exec();
    
    // 方法2: 通过setData触发视图更新
    this.setData({
      canvasRefreshKey: Date.now()
    });
    
    // 方法3: 延迟后再次触发更新
    setTimeout(() => {
      this.setData({
        qrCodeGenerated: this.data.qrCodeGenerated
      });
    }, 50);
  }
});