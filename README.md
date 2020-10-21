# bet3656-

通过截取js生成令牌：
```def get_token():
    head = """
       function aaa () {
           const jsdom = require("jsdom");
           const { JSDOM } = jsdom;
           const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
           window = dom.window;
           document = window.document;
           XMLHttpRequest = window.XMLHttpRequest;
           location=window.Location;
           navigator=window.navigator;
           var ue=[];
           var de=[];
           var gh=(function() {
                           var e = 0
                             , t = 0
                             , n = 0;
                           return function(o) {
                               e > 0 && e % 2 == 0 && (2 > t ? ue[t++] = o : 3 > n && (de[n++] = o)),
                               e++
                           }
                       })();
       """
    tail = 'return [ue,de];}'
    a = requests.get("https://www.365-868.com/")
    js = head + a.text.split("(boot||(boot={}));(function(){")[1].split('''</script>''')[0][:-6] + tail
    e = execjs.compile(js.replace("boot['gh']", 'gh'), cwd=r'C:\Users\X6TI\AppData\Roaming\npm\node_modules')
    res = e.call('aaa')
    res[0].append('.')
    token1 = ''
    for i in res:
        for j in i:
            token1 += j
    return decryptToken(token1)
```


websocket连接和数据的解析借用[@Chiang97912](https://github.com/Chiang97912/bet365.com)的代码
