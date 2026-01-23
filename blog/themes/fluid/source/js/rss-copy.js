document.addEventListener("DOMContentLoaded", function () {
    const rssUrl = "https://fogpost.top/rss.xml";
    const rssBtn = document.querySelector(".nav-rss-copy a");
  
    if (!rssBtn) return;
  
    rssBtn.addEventListener("click", function (e) {
      e.preventDefault();
  
      if (navigator.clipboard) {
        navigator.clipboard.writeText(rssUrl).then(() => {
          alert("RSS 地址已复制：\n" + rssUrl);
        });
      } else {
        // 旧浏览器兜底
        const input = document.createElement("input");
        input.value = rssUrl;
        document.body.appendChild(input);
        input.select();
        document.execCommand("copy");
        document.body.removeChild(input);
        alert("RSS 地址已复制：\n" + rssUrl);
      }
    });
  });
  