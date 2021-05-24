# sorry，An English version of the readme is not available for this project.
# DataSocial

欢迎大家浏览我的[毕业设计项目](http://cjmdatasocial.top:8000/)   该项目可能在2021/6/15日停止服务。



## 一、项目介绍
这是我的本科毕业设计，它是一个数据交互平台。
### 1.1项目有哪些功能？
- 实现了数据集上传与下载功能，你可以在平台上传你拥有且觉得有价值的数据集，当然你也可以下载那些对你有帮助的数据集，这些都是免费的。
- 作为一个平台，你可以在平台上发布有关数据处理的一些问题（例如如何使用机器学习或深度学习的一些模型对你的数据进行处理），当然这也需要你去支付一些费用；
如果你已经精通数据处理方面的技能，你也可以在在平台帮助他人解决问题以此来获得报酬。
### 1.2项目主要的技术与框架
- 这是一个网站项目（B/S）
  - 前端我使用了Bootstrap框架，考虑到目前也只有我这样20岁的老人才会用PC端浏览网页，其他绝大部分人都是使用移动端来浏览网页，因此响应式布局就很重要了，Bootstrap框架就能很好的解决这个问题。
  - 后端采用了Django框架，不采用像Spring这样基于java的框架原因就是我已经把Java忘光了（2021/5/23是这个情况以后不好说）。
### 1.3项目部署
- 项目部署在阿里云上，没上WSGI，因为这个模块在部署的时候老是抽风，半天搞不好，再一个我对中间件差不多是一窍不通，（2021/5/23是这个情况以后不好说）遂放弃。

## 二、项目结构
### 项目结构
- Readme.md                   // help
- dataset                     // 数据集上传下载模块
- DataSocial                  // 项目
  - settings.py             // 配置
  - urls.py                 // 路由
- dataset_file_savedir        // 存放数据集
- doc                         // 文档
- homepage                    // 首页
- log                         // 日志
- static                      // 静态文件
- task                        // 任务模块
- task_answer_dataset         // 任务回答模块
- task_dataset_file_savedir   // 任务附带数据集文件夹
- templates                   // 模板
- UserRegister                // 用户登录模块
- manage.py                   // 启动文件

## 三、第三方服务&linux上的配置
- 腾讯云短信服务实现登录注册手机短信验证任务
- Crontab实现定时任务
- captcha实现图形验证码
- redis实现服务器端短信验证码的短期存储

## 四、依赖的第三方库
- Django
- django-bootstrap3
- django-crontab
- django-redis 
- Pillow
- PyEmail

## 项目截图
- 项目首页截图
![Image text](https://github.com/Samchengjiaming/README_img/blob/master/homepage.PNG)
- 数据集模块截图
![Image text](https://github.com/Samchengjiaming/README_img/blob/master/dataset.PNG)
- 任务模块截图
![Image text](https://github.com/Samchengjiaming/README_img/blob/master/task.PNG)
- 登录注册模块截图
![Image text](https://github.com/Samchengjiaming/README_img/blob/master/sign_in.PNG)

