"""
@Project ：QMS 
@File ：constants.py
@Author ：张建
@Date ：2022/2/17 10:29 下午 
"""

# 系统名称
NAME = "QMS"

# 企业文化
CULTURE = "激情 创新 协作 高效"

# 短信验证码有效时间(s)
SMS_CODE_EXPIRES = 300

# 短信验证码发送周期(s)
SMS_CODE_INTERVAL = 60

# 职位信息
STAFF_ROLE = [(0, "测试"), (1, "开发"), (2, "产品"), (3, "行政"), (4, "客服"), (5, "薪酬"), (6, "管理员")]

# 员工职级
STAFF_RANK = [(0, "初级"), (1, "中级"), (2, "高级"), (3, "资深"), (4, "专家")]

# 接口协议
API_PROTO = [(0, "http"), (1, "https"), (2, "websocket"), (3, 'rpc'), (4, 'grpc')]

# 测试角色
TEST_ROLE = [(0, "tester"), (1, "super_user"), (2, "manager"), (3, "admin")]
