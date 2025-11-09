import streamlit as st
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
mail_host = "stmp@youstmp.com"  # SMTP服务器
mail_user = "a@youemail.com"  # 完整邮箱地址
mail_pass = "youpassword"  # 这里是授权码或邮箱密码

receivers = ['send@email.com']#这里填要发送的人
st.set_page_config(
    page_title="ExScriptRMK建议反馈",  # 这里设置标签页标题
    page_icon="index.ico",              # 可选：设置标签页图标，可以是Emoji或图片
    layout="centered"            # 可选：设置页面布局，"centered" 或 "wide"
)
if 'last_click_time' not in st.session_state:
    st.session_state.last_click_time = 0
CLICK_INTERVAL = 60
st.title('ExScriptRMK建议反馈网站')
send = st.text_input('请输入你要反馈的问题', max_chars=1000, help='最大长度为1000字符')
def send_email_action():
    current_time = time.time()
    # 检查当前时间与上次点击时间的间隔是否大于设定的间隔
    if current_time - st.session_state.last_click_time > CLICK_INTERVAL:
        # 执行发送邮件的核心逻辑
        # 这里替换成你实际的SMTP发送代码
        # send_email_function() 
        
        message = MIMEText(f'{send}\n该消息为自动发送请不要进行回信', 'plain', 'utf-8')
        message['From'] = formataddr(("ExScriptRMK建议反馈功能", "suppot@tywmc.cn"))
        message['To'] = Header("TYW", 'utf-8')    # 收件人显示名称
        message['Subject'] = Header('ExScriptRMK建议反馈功能', 'utf-8')
        try:
            # 关键步骤：创建SMTP_SSL对象，强制使用SSL加密连接
            smtp_obj = smtplib.SMTP_SSL(mail_host, 465)
            # 登录邮箱
            smtp_obj.login(mail_user, mail_pass)
            # 发送邮件
            smtp_obj.sendmail(mail_user, receivers, message.as_string())
            st.success("邮件发送成功！") # 发送成功提示
            # 关闭连接
            smtp_obj.quit()

        except smtplib.SMTPException as e:
            st.success(f"邮件发送失败，错误：{e}")
        
        # 更新最后一次成功点击的时间戳为当前时间
        st.session_state.last_click_time = current_time
    else:
        # 计算还需要等待多久
        wait_time = CLICK_INTERVAL - int(current_time - st.session_state.last_click_time)
        st.warning(f"操作过于频繁，请等待 {wait_time} 秒后再试。")

# 在页面上创建按钮，并绑定处理函数
if st.button("发送邮件", on_click=send_email_action):
    # 注意：由于使用了on_click，主要逻辑在send_email_action函数中执行
    # 这里可以留空，或者放置一些与按钮关联性不强的后续操作
    pass
