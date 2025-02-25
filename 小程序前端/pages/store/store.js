// pages/store/store.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    houseItems: [],
    openid: '',
    favoriteMap: {} // 用于存储房源的收藏状态，key为房源id，value为true或false 
  },
  toggleFavorite: function(e) {  
    var houseId = e.currentTarget.dataset.houseId; // 获取当前房源的id
    var isFavorite = this.data.favoriteMap[houseId] || false; // 获取当前房源的收藏状态，如果未定义则默认为false 
    this.setData({  
      ['favoriteMap.' + houseId]: !isFavorite  
    });
    if (isFavorite){
      wx.request({
        url: 'http://127.0.0.1:5000/insertStore',
        method: 'POST',
        data:{
          openid: this.data.openid,
          houseId: houseId
        },
        success: (res) => {
          console.log(res)

          //console.log(this.data.favoriteMap)
        }

      })
    }//若取消收藏，则将该数据删除
    else{
      wx.request({
        url: 'http://127.0.0.1:5000/deleteStore',
        method: 'POST',
        data:{
          openid: this.data.openid,
          houseId: houseId
        },
        success: (res) => {
          console.log(res)
        }

      })
    };
    wx.showToast({  
      title: isFavorite ? '收藏成功' : '取消收藏成功',  
      icon: 'success',  
      duration: 2000  
    });  
  },  
  goToHouseDetail:function(event){
    var house_href = event.currentTarget.dataset.href
    console.log(house_href)
    wx.navigateTo({
      url: '../jump/jump?href=' + house_href
    });
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    const openid = wx.getStorageSync('openid');
    //console.log(openid)
    this.setData({ openid: openid }); // 将openid添加到页面的data中
    this.fetchData();
  },

  fetchData: function() {  
    wx.request({  
      url: 'http://127.0.0.1:5000/getStoreData',
      method: 'GET',  
      data:{
        openid: this.data.openid
      },
      success: (res) => {  
        // 请求成功，处理返回的数据  
        if (res.data && res.data.length > 0) {
          this.setData({  
            houseItems: res.data,// 将数据设置到页面的 data 中  
          });  
          
        } else {  
          wx.showToast({  
            title: '没有数据',  
            icon: 'none'  
          });  
        }  
      },  
      fail: (err) => {  
        // 请求失败，处理错误  
        wx.showToast({  
          title: '请求失败',  
          icon: 'none'  
        });  
        
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
    this.fetchData()
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