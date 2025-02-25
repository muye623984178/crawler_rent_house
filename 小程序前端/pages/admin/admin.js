// pages/admin/admin.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    name:'xxx',
    statu:'正常'
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    const openId = wx.getStorageSync('openid');
    this.setData({ openid: openId }); // 将openid添加到页面的data中
    this.getName(openId);
  },
  getName: function(openId){
    const that = this;
    //console.log(openId)
    wx.request({
      url: 'http://127.0.0.1:5000/getName',
      method: 'POST',
      data:{
        openid: openId
      },
      success: (res) => {
        //console.log(res)
        that.setData({
          name: res.data.name
        })
      },
      fail: function(error) {  
        // 请求失败的处理  
        console.error('请求失败:', error);  
      }  
    })
    
  },
  crawl: function(e) {
    const platform = e.currentTarget.dataset.platform;
    console.log('爬取数据操作，平台：', platform);
    const that = this;
    that.setData({
      statu: platform + "爬虫ing"
    })
     wx.request({
        url: 'http://127.0.0.1:5000/crawl',
        method: 'POST',
        data:{
          platform: platform
        },
        success: (res) => {
          console.log(res)
          that.setData({
            statu: platform + "爬虫成功"
          })
        },
        fail: function(error) {  
          // 请求失败的处理  
          console.error('请求失败:', error);  
          that.setData({
            statu: platform + "爬虫失败"
          })
        }  
      })
  },
  export: function(e) {
    const platform = e.currentTarget.dataset.platform;
    console.log('导出数据操作，平台：', platform);
    const that = this;
    that.setData({
      statu: platform + "进行信息导出"
    });
    wx.request({
      url: 'http://127.0.0.1:5000/export',
      method: 'POST',
      data: {
        platform: platform
      },
      success: function(res) {
        // 获取服务器返回的文件下载地址
        var downloadUrl = res.data.download_url; // 确保服务器返回了这个字段
        console.log(res)
        wx.downloadFile({
          url: downloadUrl,
          success: function(downloadRes) {
            // 打开文件
            wx.openDocument({
              filePath: downloadRes.tempFilePath,
              success: function(openRes) {
                console.log('打开文档成功');
                that.setData({
                  statu: platform + "文件导出成功"
                });
              },
              fail: function(openError) {
                console.error('打开文档失败:', openError);
                that.setData({
                  statu: platform + "文件打开失败"
                });
              }
            });
          },
          fail: function(downloadError) {
            console.error('下载文件失败:', downloadError);
            that.setData({
              statu: platform + "文件下载失败"
            });
          }
        });
      },
      fail: function(requestError) {
        // 请求失败的处理
        console.error('请求失败:', requestError);
        that.setData({
          statu: platform + "文件导出请求失败"
        });
      }
    });
  },
  refresh: function(e) {
    const platform = e.currentTarget.dataset.platform;
    console.log('更新数据操作，平台：', platform);
    const that = this;
    that.setData({
      statu: platform + "更新房屋信息ing"
    })
     wx.request({
        url: 'http://127.0.0.1:5000/refresh',
        method: 'POST',
        data:{
          platform: platform
        },
        success: (res) => {
          console.log(res)
          that.setData({
            statu: platform + "更新成功"
          })
        },
        fail: function(error) {  
          // 请求失败的处理  
          console.error('请求失败:', error);  
          that.setData({
            statu: platform + "更新失败"
          })
        }  
      })
  },
  processData: function(e) {
    const that = this;
    that.setData({
      statu: "数据整合与清洗ing"
    })
     wx.request({
        url: 'http://127.0.0.1:5000/processData',
        method: 'POST',
        success: (res) => {
          console.log(res)
          that.setData({
            statu: "数据处理成功"
          })
        },
        fail: function(error) {  
          // 请求失败的处理  
          console.error('请求失败:', error);  
          that.setData({
            statu: platform + "数据处理失败"
          })
        }  
      })
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