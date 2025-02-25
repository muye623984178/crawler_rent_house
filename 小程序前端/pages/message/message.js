// pages/message/message.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    houseItems: [],
    openid: '',
    searchInfo: '', // 搜索框的信息
    selectedPlace: '北京', // 初始化地点信息
    places: [], // 特定的地点选项
    currentPage: 1, // 当前页码 
    favoriteMap: {} // 用于存储房源的收藏状态，key为房源id，value为true或false 
  },
  setPlace:function(){
    wx.request({
      url: 'http://127.0.0.1:5000/setPlace',
      method: 'GET',
      success: (res) => {
        console.log(res)
        this.setData({
          places: res.data
        })
        //console.log(this.data.favoriteMap)
      }

    })
  },
  onPlaceChange: function(e) {
    // 更新选择的地点
    this.setData({
      selectedPlace: this.data.places[e.detail.value],
      houseItems: [], // 清空现有的房源数据
      currentPage: 1, // 重置当前页码为1
      searchInfo: ''
    });
    // 重新加载对应地区的房源数据
    this.loadDataByArea(1);
  },

  toggleFavorite: function(e) {  
    var houseId = e.currentTarget.dataset.houseId; // 获取当前房源的id  
    var isFavorite = this.data.favoriteMap[houseId] || false; // 获取当前房源的收藏状态，如果未定义则默认为false       
    // 切换收藏状态  
    this.setData({  
      ['favoriteMap.' + houseId]: !isFavorite  
    });    
    //console.log(isFavorite)
    //若收藏，则添加该数据到数据库中
    if (!isFavorite){
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
      title: isFavorite ? '已取消收藏' : '收藏成功',  
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
  loadDataByArea: function(page) {  
    const that = this;  
    wx.request({  
      url: 'http://127.0.0.1:5000/getDataByArea_page',   
      data: {  
        page: page, // 传入页码参数  
        area: that.data.selectedPlace
      },  
      success: function(res) {   
        const newData = res.data;   
        that.setData({  
          // 将数据追加到 list 数组中  
          houseItems: that.data.houseItems.concat(newData), 
          // 更新当前页码  
          currentPage: page  
        });  
        console.log(res)
      },  
      fail: function(error) {  
        // 处理请求失败的情况  
        console.error('请求数据失败', error);  
      }  
    });  
  },  
  judgeStore:function(openId){
    //console.log('judgeStore' + '运行');
    wx.request({
      url: 'http://127.0.0.1:5000/judgeStore',
      method: 'POST',
      data: {
        openid: openId
      },
      success: (res) => {  
        //console.log(res);
        if (res.data) {
          this.setData({  
            favoriteMap: res.data,// 将数据设置到页面的 data 中  
          });  
          
        } else {  
          wx.showToast({  
            title: '没有数据',  
            icon: 'none'  
          });  
        }  
      },  
      fail: (err) => {  
        wx.showToast({  
          title: '请求失败',  
          icon: 'none'  
        });  
      }  
    })
  },
  onInput: function(e) {
    // 当用户输入时，会触发这个函数
    this.setData({
      searchInfo: e.detail.value
    });
  },
  findData:function(){
    const that = this;  
    console.log(that.data.searchInfo),
    wx.request({  
      url: 'http://127.0.0.1:5000/findData',   
      method: 'GET',
      data: {  
        word: that.data.searchInfo,
        area: that.data.selectedPlace
      },  
      success: function(res) {    
        console.log(res)
        that.setData({   
          houseItems: res.data
        });  
      },  
      fail: function(error) {  
        // 处理请求失败的情况  
        console.error('请求数据失败', error);  
      }  
    }); 
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    const openId = wx.getStorageSync('openid');
    this.setData({ openid: openId }); // 将openid添加到页面的data中
    //this.loadData(1);
    this.setPlace();
    this.loadDataByArea(1);
    this.judgeStore(openId);
    //console.log(this.data.selectedPlace)
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {
    const openId = this.data.openid;
    //console.log(openId)
    
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    //console.log(this.data.favoriteMap)
    const openId = wx.getStorageSync('openid');
    console.log(this.data.selectedPlace);
    this.judgeStore(openId)
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
  onReachBottom: function() {  
    // 调用loadData方法并传入下一页的页码  
    //this.loadData(this.data.currentPage + 1);  
    this.loadDataByArea(this.data.currentPage + 1);
    this.setData({
      searchInfo:''
    })
  }, 

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})