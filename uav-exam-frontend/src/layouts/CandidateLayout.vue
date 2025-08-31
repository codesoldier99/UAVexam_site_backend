<style lang="scss" scoped>
.candidate-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  
  .layout-container {
    min-height: 100vh;
  }
  
  .header {
    background-color: #fff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    
    .header-left {
      display: flex;
      align-items: center;
      
      .logo {
        display: flex;
        align-items: center;
        
        .logo-img {
          height: 32px;
          margin-right: 10px;
        }
        
        .logo-text {
          font-size: 18px;
          font-weight: 600;
          color: #303133;
          margin: 0;
        }
      }
    }
    
    .header-right {
      display: flex;
      align-items: center;
      
      .el-menu {
        border-bottom: none;
        margin-right: 20px;
      }
      
      .user-actions {
        margin-left: 20px;
        
        .user-info {
          display: flex;
          align-items: center;
          cursor: pointer;
          
          .username {
            margin: 0 8px;
            font-size: 14px;
          }
        }
      }
    }
  }
  
  .main-content {
    padding: 80px 20px 60px;
    background-color: #f5f7fa;
    min-height: calc(100vh - 60px);
  }
  
  .footer {
    background-color: #fff;
    text-align: center;
    color: #666;
    font-size: 14px;
    padding: 16px;
    box-shadow: 0 -1px 4px rgba(0, 0, 0, 0.05);
  }
}

@media (max-width: 768px) {
  .candidate-layout {
    .header {
      padding: 0 10px;
      
      .logo-text {
        display: none;
      }
      
      .user-info .username {
        display: none;
      }
    }
    
    .main-content {
      padding: 80px 10px 60px;
    }
  }
}
</style>