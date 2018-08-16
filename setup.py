from setuptools import setup, find_packages

# setup(
#     name='office_helper',  # 应用名
#     version='2.0',  # 版本号
#     author='Chuck Lin',
#     author_email='mikumiku.lch@hotmail.com',
#     license='MIT',
#     packages=['./', 'attendance_spider', 'mail_sender', 'make_document', 'printer_operator'],  # 包括在安装包内的Python包
#     include_package_data=True,  # 启用清单文件MANIFEST.in
#     exclude_package_date={'': ['.gitignore']},
#     install_requires=[  # 依赖列表
#         'python-docx>=0.8.6'
#     ]
# )


setup(
    name='office_helper',  # 应用名
    version='2.0',  # 版本号
    author='Chuck Lin',
    author_email='mikumiku.lch@hotmail.com',
    description='敏感词作弊机器人',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,  # 启用清单文件MANIFEST.in
    # exclude_package_date={'': ['.gitignore']},  # 忽略 gitignore 中忽略的内容
    install_requires=[  # 依赖列表
        'python-docx>=0.8.6'
    ]
)
