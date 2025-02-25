// logs.js  
const util = require('../../utils/util.js');  
  
Page({  
  data: {  
    logs: [],  
  },  
  onLoad() {  
    this.setData({  
      logs: (wx.getStorageSync('logs') || []).map(log => {  
        return {  
          date: util.formatTime(new Date(log)),  
          timeStamp: log  
        }  
      })  
    });   
  },  
  wxLogin() {  
    wx.login({  
      success: res => {  
        if (res.code) {  
          console.log("输出code：" + res.code);  
          // 发送请求到你的服务器接口  
          wx.request({  
            url: 'http://127.0.0.1:5000/login', // 替换成你的服务器地址和端口号  
            method: 'POST',  
            data: {  
              code: res.code  
            },  
            success: response => {  
              console.log('服务器返回的用户信息：', response.data);  
              // 在这里处理服务器返回的 openid  
              // 例如，保存到全局状态或本地存储  
              if (response.data.openid) {  
                wx.setStorageSync('openid', response.data.openid);  
              }  
            },  
            fail: error => {  
              console.error('请求服务器失败：', error);  
              // 处理请求失败的情况  
            }  
          });  
        } else {  
          console.log('登录失败！' + res.errMsg);  
          // 处理登录失败的情况  
        }  
      }  
    });  
  },    
});