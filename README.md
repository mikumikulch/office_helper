# About

办公小助手是一个帮助你脱离繁琐的事务工作的自动化脚本应用。
小助手拥有诸如自动填写打印加班审批单、调休审批单、智能化打卡小助手等功能。

# Version

**Version 2.0**  

- 支持自动填写加班审批表，并通过邮件发送到指定邮箱。
- 支持每日不受距离限制，自动出勤退勤打卡功能。

# Features

- 自动填写调休单填写功能锐意制作中
- 调休日期、节假日自动禁止打卡功能锐意制作中

```
对 features 有任何好的建议，请在 issue 提出。
对项目有兴趣愿意贡献代码，请与作者取得联系，一同让生活变的更美好。
```

# Environment

|环境|版本|支持|备注|
|--|--|--|--|
|操作系统|unix-like/windows|是|无|
|python|python3.x|是|无|


# How to work

1. 请在本机安装好 python3 运行环境。
2. clone 或者下载本项目 zip 包。
3. 将源代码打包后，采用 command 或 cron/tab 或者 automator 等方式运行。
4. 项目运行需要自定义一份配置文件。如果你对 python 十分了解，请阅读代码后自行开发。
5. 同样你也可以邀请作者为您量身定制并协助部署一套办公小助手。我会视心情是否接受。
6. 请作者喝一杯咖啡，可极大提高邀请的成功率。 -> 
https://www.gitbook.com/book/mikumikulch/chucklin_blog 
价格随缘，扫码支付即可。

### 打包与分发

推荐使用 setuptools 打包项目成为 wheels 的方式对代码进行分发。
你可以参照项目中的 setup.py 与 MANIFEST.in 文件对配置进行调整以满足你的需求。

注意，由于我使用了 MIT 协议，所以请务必不要忘记原作者署名，谢谢。
 
```shell
cd {workspace_root_path}
python3 setup.py sdist bdist_wheel
```

# License


项目严格遵守 [MIT License](https://choosealicense.com/licenses/mit/) 。你可以在署名原作者的情况下采用任何方式使用本代码，
但原作者不承担代码使用后的风险，也没有技术支持的义务。
