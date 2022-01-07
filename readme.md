该项目用于生产环境用于服务升级，URL可以正常访问，DB升级，
springboot等三方包升级做sanity测试

batchattend.py 文件，用于处理APP与ERP之间数据不一致问题调用考勤接口进行同步数据
1.需要有一个Excel文件，用于拼接request请求，然后拼接好的request生成sign
2.将生成的sign拼接到URL中，如/erp_openapi/stu_course/attend?name=1&sign='+server_sign