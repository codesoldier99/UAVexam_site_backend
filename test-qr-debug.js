// Test script to debug QR code issues in WeChat Mini Program context
const fs = require('fs');
const path = require('path');

// Mock WeChat Mini Program environment
global.wx = {
  createCanvasContext: function(canvasId) {
    console.log('wx.createCanvasContext called with canvasId:', canvasId);
    return {
      setFillStyle: function(color) {
        console.log('ctx.setFillStyle called with color:', color);
      },
      fillRect: function(x, y, w, h) {
        console.log('ctx.fillRect called with:', x, y, w, h);
      },
      draw: function(reserve, callback) {
        console.log('ctx.draw called with reserve:', reserve);
        if (callback) {
          console.log('ctx.draw: calling callback');
          setTimeout(callback, 10); // Simulate async drawing
        }
      }
    };
  },
  getStorageSync: function(key) {
    console.log('wx.getStorageSync called with key:', key);
    // Mock storage data
    if (key === 'candidateInfo') {
      return {
        id: 3,
        username: "candidate_011234",
        email: "zhangsan@example.com",
        role: "candidate",
        full_name: "张三",
        id_card: "110101199001011234"
      };
    }
    if (key === 'candidateId') {
      return 3;
    }
    return null;
  }
};

// Load the QR code library
console.log('Loading QR code library...');
const qrCodePath = path.join(__dirname, 'miniprogram', 'utils', 'weapp-qrcode.js');

// Create a new module context to avoid variable conflicts
const Module = require('module');
const vm = require('vm');

// Create a new module context
const qrModule = new Module();
qrModule.exports = {};

// Create a sandbox with the module context
const sandbox = {
  module: qrModule,
  exports: qrModule.exports,
  require: require,
  console: console,
  wx: global.wx,
  global: global
};

// Read and execute the QR code library in the sandbox
const qrCodeContent = fs.readFileSync(qrCodePath, 'utf8');
vm.createContext(sandbox);
vm.runInContext(qrCodeContent, sandbox);

console.log('QR code library loaded successfully');
console.log('module.exports:', qrModule.exports);

const { QRCode, QRErrorCorrectLevel } = qrModule.exports;
console.log('QRCode constructor:', typeof QRCode);
console.log('QRErrorCorrectLevel:', QRErrorCorrectLevel);

// Test QR code generation similar to the Mini Program
console.log('\n=== Testing QR Code Generation ===');

try {
  // Mock candidate info (same as what would be in storage)
  const candidateInfo = {
    id: 3,
    username: "candidate_011234",
    email: "zhangsan@example.com",
    role: "candidate",
    full_name: "张三",
    id_card: "110101199001011234"
  };

  // Create QR code data (same as in the Mini Program)
  const qrData = {
    candidate_id: candidateInfo.id,
    name: candidateInfo.full_name || candidateInfo.name,
    id_card: candidateInfo.id_card,
    username: candidateInfo.username,
    timestamp: new Date().getTime(),
    type: 'candidate_checkin'
  };

  const qrCodeText = JSON.stringify(qrData);
  console.log('QR code text length:', qrCodeText.length);
  console.log('QR code text:', qrCodeText);

  // Create QR code instance (same parameters as Mini Program)
  console.log('Creating QRCode instance...');
  const qrCodeInstance = new QRCode('qrcode', {
    text: qrCodeText,
    width: 200,
    height: 200,
    colorDark: '#000000',
    colorLight: '#ffffff',
    correctLevel: QRErrorCorrectLevel.H,
    callback: () => {
      console.log('✅ QR code generation callback executed successfully!');
    }
  });

  console.log('✅ QRCode instance created successfully:', typeof qrCodeInstance);
  console.log('QRCode instance properties:', Object.keys(qrCodeInstance));

} catch (error) {
  console.error('❌ Error during QR code generation:', error.message);
  console.error('Error stack:', error.stack);
}

console.log('\n=== Test completed ===');