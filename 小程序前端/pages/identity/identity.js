// pages/identity/identity.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    openid: '',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    const openId = wx.getStorageSync('openid');
    this.setData({ openid: openId }); // 将openid添加到页面的data中
  },
  toUser:function(){
    wx.showToast({  
      title: '用户登录成功',  
      icon: 'success',  
      duration: 2000  
    }),
    wx.switchTab({
      url: '/pages/home/home'
    })
  },
  toAdmin:function(){
    wx.request({
      url: 'http://127.0.0.1:5000/judgeIdentity',
      method: 'POST',
      data:{
        openid: this.data.openid,
      },
      success: (res) => {
        //console.log(res)
        if(res.data.flag == 'true'){
          wx.showToast({  
            title: '管理员登录成功',  
            icon: 'success',  
            duration: 2000  
          }),
          wx.redirectTo({
            url: '/pages/admin/admin'
          })
        }
        else{
          wx.showToast({  
            title: '您无管理员身份',  
            icon: 'success',  
            duration: 2000  
          })
        }
      }
    });
    

  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})