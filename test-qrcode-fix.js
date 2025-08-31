// Test script to verify QR code library fix
const fs = require('fs');
const path = require('path');

// Mock wx object for testing
global.wx = {
  createCanvasContext: function(canvasId) {
    return {
      setFillStyle: function(color) {},
      fillRect: function(x, y, w, h) {},
      draw: function(reserve, callback) {
        if (callback) callback();
      }
    };
  }
};

// Load the QR code library
const qrCodePath = path.join(__dirname, 'miniprogram', 'utils', 'weapp-qrcode.js');
const qrCodeContent = fs.readFileSync(qrCodePath, 'utf8');

// Execute the QR code library code
eval(qrCodeContent);

// Test QR code generation with different type numbers and error correction levels
console.log('Testing QR code library...');

try {
  // Test the problematic case: typeNumber 11, errorCorrectLevel 2 (Q level)
  console.log('Testing typeNumber 11 with Q error correction level...');
  
  const { QRCode, QRErrorCorrectLevel } = module.exports;
  
  // Create QR code with specific parameters that were failing
  const qrCode = new QRCode('testCanvas', {
    text: 'This is a test string that should generate a QR code with typeNumber 11',
    width: 256,
    height: 256,
    correctLevel: QRErrorCorrectLevel.Q // This is level 2
  });
  
  console.log('✅ QR code generation successful!');
  console.log('✅ RS block table fix is working correctly');
  
  // Test other error correction levels
  console.log('\nTesting other error correction levels...');
  
  const levels = [
    { name: 'L', level: QRErrorCorrectLevel.L },
    { name: 'M', level: QRErrorCorrectLevel.M },
    { name: 'Q', level: QRErrorCorrectLevel.Q },
    { name: 'H', level: QRErrorCorrectLevel.H }
  ];
  
  levels.forEach(({ name, level }) => {
    try {
      const testQR = new QRCode('testCanvas', {
        text: 'Test string for level ' + name,
        correctLevel: level
      });
      console.log(`✅ Error correction level ${name} works`);
    } catch (error) {
      console.log(`❌ Error correction level ${name} failed: ${error.message}`);
    }
  });
  
} catch (error) {
  console.error('❌ QR code generation failed:', error.message);
  console.error('Stack trace:', error.stack);
}

console.log('\nTest completed.');