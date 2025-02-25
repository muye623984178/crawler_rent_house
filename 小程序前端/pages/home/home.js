// pages/home/home.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    showWebView1: false,
    showWebView2: false,
    showWebView3: false,
    ziRuUrl: 'https://www.ziroom.com/',
    lianJiaUrl: 'https://bj.lianjia.com/',
    woAiWoJiaUrl: 'https://www.5i5j.com/',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

  },
  goToZiRu:function(event){
    wx.navigateTo({
      url: '../jump/jump?href=' + this.data.ziRuUrl
    }); 
  },
  goToLianJia:function(event){
    wx.navigateTo({
      url: '../jump/jump?href=' + this.data.lianJiaUrl
    });  
  },
  goToWoAiWoJia:function(event){
    wx.navigateTo({
      url: '../jump/jump?href=' + this.data.woAiWoJiaUrl
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