// pages/jump/jump.js
// pages/webview-page/webview-page.js  
Page({  
  data: {  
    webViewUrl: '' 
    // 这里替换成你要跳转的网页URL  
  },  
  onLoad: function(options) {  
    var href = options.href
    console.log(href)
    this.setData({
      webViewUrl: href
    })
    // 页面加载时执行，这里可以放置一些初始化代码，比如检查URL是否有效等  
    // 如果URL需要动态获取，可以在这里通过API请求等方式获取，然后更新data中的webViewUrl  
  },  
  onWebViewLoad: function(e) {  
    // 网页加载成功时触发  
    console.log('WebView加载成功', e.detail);  
  },  
  onWebViewError: function(e) {  
    // 网页加载失败时触发  
    console.error('WebView加载失败', e.detail);  
  }  
});