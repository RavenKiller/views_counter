# views_counter
统计网页浏览量的小插件

## 使用方法
### 服务端
本插件不提供公用服务，使用前需要自己开启服务端。服务端程序文件为`server.py`，使用Python3.8测试。
安装依赖:
```shell
pip install tornado
```
运行程序:
```shell
python server.py 2333
```
可将2333替换为你想要的端口，接口的相对路径为`/views`。
### 前端
导入库：
```html
<script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/RavenKiller/views_counter@v0.1/views_counter.min.js"></script>


```
访问量组件示例：
```html
<!-- 请在data-server-url属性中填入自己的URL -->
<div><span id="vc_page_views" data-server-url="your-server-url/views"></span> page views</div>
<div><span id="vc_site_views" data-server-url="your-server-url/views"></span> site views</div>
<div><span id="vc_page_users" data-server-url="your-server-url/views"></span> page users</div>
<div><span id="vc_site_users" data-server-url="your-server-url/views"></span> site users</div>
```
不同的ID含义：
+ `vc_page_views`: 当前页面的访问量
+ `vc_site_views`: 站点的总访问量
+ `vc_page_users`: 当前页面的用户量
+ `vc_site_users`: 站点的总用户量

只需要设置一个组件的`data-server-url`。当多个组件的`data-server-url`被设置时，优先级最高的一个会生效。优先级为`vc_page_views`>`vc_site_views`>`vc_page_users`>`vc_site_users`
