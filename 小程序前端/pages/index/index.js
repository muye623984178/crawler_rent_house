// index.js
const defaultAvatarUrl = 'https://mmbiz.qpic.cn/mmbiz/icTdbqWNOwNRna42FI242Lcia07jQodd2FJGIYQfG0LAJGFxM4FbnQP6yfMxBgJ0F3YRqJCJ1aPAK2dQagdusBZg/0'

Page({
  data: {
    motto: 'Hello World',
    userInfo: {
      avatarUrl: defaultAvatarUrl,
      nickName: '',
    },
    hasUserInfo: false,
    canIUseGetUserProfile: wx.canIUse('getUserProfile'),
    canIUseNicknameComp: wx.canIUse('input.type.nickname'),
  },
  bindViewTap() {
    wx.navigateTo({
      url: '/pages/identity/identity'
    }),
    wx.login({
      success: (res) => {
        if (res.code) {  
          console.log("输出code：" + res.code);  
          // 发送请求到你的服务器接口  
          wx.request({  
            url: 'http://127.0.0.1:5000/login',  
            method: 'POST',  
            data: {  
              code: res.code  
            },  
            success: response => {  
              console.log('服务器返回的用户信息：', response.data);  
              // 在这里处理服务器返回的 openid   
              if (response.data.openid) {  
                // 将获取到的openid保存到全局状态或者本地存储  
                //const openid = response.data.openid;  
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
      },
    })
  },
  onChooseAvatar(e) {
    const { avatarUrl } = e.detail
    const { nickName } = this.data.userInfo
    this.setData({
      "userInfo.avatarUrl": avatarUrl,
      hasUserInfo: nickName && avatarUrl && avatarUrl !== defaultAvatarUrl,
    })
  },
  onInputChange(e) {
    const nickName = e.detail.value
    const { avatarUrl } = this.data.userInfo
    this.setData({
      "userInfo.nickName": nickName,
      hasUserInfo: nickName && avatarUrl && avatarUrl !== defaultAvatarUrl,
    })
  },
  getUserProfile(e) {
    // 推荐使用wx.getUserProfile获取用户信息，开发者每次通过该接口获取用户个人信息均需用户确认，开发者妥善保管用户快速填写的头像昵称，避免重复弹窗
    wx.getUserProfile({
      desc: '展示用户信息', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        console.log(res)
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    })
  },
})
