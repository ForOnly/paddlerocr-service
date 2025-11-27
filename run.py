# @description: 
# @author: licanglong
# @date: 2025/11/20 11:41
import logging
import multiprocessing
import os
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS

# 设置环境变量
os.environ["APP_PATH"] = os.getenv('APP_PATH') or os.path.abspath(os.path.dirname(__file__))  # noqa

from app.App import App
from app.core import BizException
from app.models.Result import SysResult

App.DEFAULT_LOG_FILE = "logs/app.log"


class AppImpl(App):

    def create_app(self):
        from app.blueprints.base import base_bp
        app = Flask(__name__)

        # 初始化扩展
        # db.init_app(app)
        CORS(app, supports_credentials=True)
        app.config['JSON_AS_ASCII'] = False
        # 注册 Blueprint
        app.register_blueprint(base_bp)

        @app.before_request
        def before():
            pass

        @app.after_request
        def after_request(response):
            """为每个请求添加 CORS 头"""
            return response

        @app.errorhandler(404)
        def handle_404_error(e):
            # 打印请求路径
            logging.error(f"error request url: {request.path}")
            logging.exception(e)
            return jsonify(SysResult.fail(code=404, msg=str(e)))

        @app.errorhandler(BizException)
        def biz_error_handle(e):
            logging.exception(e.message)
            return jsonify(SysResult.fail(msg=e.message or "服务异常", code=e.code))

        @app.errorhandler(Exception)
        def exception_handle(e):
            logging.exception(e)
            return jsonify(SysResult.fail(msg="服务异常"))

        return app

    def run(self):
        _app = self.create_app()
        try:
            if getattr(sys, 'frozen', False):
                from waitress import serve

                if sys.platform == "win32":
                    import msvcrt

                    multiprocessing.freeze_support()
                    serve(_app, host='0.0.0.0', port=5566)
                    msvcrt.getch()
                else:
                    serve(_app, host='0.0.0.0', port=5566)

            else:
                _app.run(host="0.0.0.0", port=5566)

        except KeyboardInterrupt:
            logging.warning("程序终止!!")


if __name__ == '__main__':
    AppImpl().start()
