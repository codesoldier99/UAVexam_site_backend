// Simple QR code test
console.log('Testing QR code generation...');

// Mock wx for testing
global.wx = {
  createCanvasContext: () => ({
    setFillStyle: () => {},
    fillRect: () => {},
    draw: (reserve, callback) => {
      console.log('Canvas draw called');
      if (callback) callback();
    }
  })
};

try {
  // Load QR module directly
  const qrModule = require('./miniprogram/utils/weapp-qrcode.js');
  console.log('QR module loaded:', !!qrModule);
  console.log('QRCode available:', !!qrModule.QRCode);
  console.log('QRErrorCorrectLevel available:', !!qrModule.QRErrorCorrectLevel);
  
  const { QRCode, QRErrorCorrectLevel } = qrModule;
  
  // Test simple QR generation
  console.log('Creating QR code...');
  const qr = new QRCode('test', {
    text: 'Hello World',
    width: 100,
    height: 100,
    correctLevel: QRErrorCorrectLevel.H
  });
  
  console.log('✅ QR code created successfully');
  
} catch (error) {
  console.error('❌ Error:', error.message);
}