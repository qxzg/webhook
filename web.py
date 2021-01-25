#!/bin/python3
from flask import Flask, request, jsonify
from gevent import pywsgi
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkrds.request.v20140815.ModifySecurityIpsRequest import ModifySecurityIpsRequest
import logging
import config

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, filename="log/stdout.log", filemode="a")

def set_rds_security_ips(security_ips):
    client = AcsClient(config.AccessKey_ID, config.AccessKey_Secret, config.Rds_Region)

    request = ModifySecurityIpsRequest()
    request.set_accept_format('json')

    request.set_DBInstanceId(config.Rds_ID)
    request.set_SecurityIps(security_ips)
    request.set_DBInstanceIPArrayName("outside")

    response = client.do_action_with_exception(request)
    logging.info(str(response, encoding='utf-8'))

@app.route('/hook', methods=['POST'])
def post_data():
    """
    """
    post_data = request.json
    logging.info(post_data['msgTYPE'])
    try:
        if request.headers['X-Token'] != config.Token:
            logging.error("token认证无效")
            return "token认证无效", 401
    except:
        return "请求失败", 401
    wan_ip = post_data['netSTATE']['wanIPv4']
    set_rds_security_ips(wan_ip)
    return jsonify({"status": 200})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=13283, debug=False)
    #server = pywsgi.WSGIServer(('0.0.0.0', 8989), app)
    #server.serve_forever()