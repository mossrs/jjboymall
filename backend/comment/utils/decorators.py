from flask import g, redirect, current_app

"""
自定义一个装饰器，验证某些请求是否已经登录过了。如果已经登录了继续访问。
本质上就是一个登录拦截 主要用于用户访问某些需要登陆的页面 
因为我加了请求钩子 如果请求钩子里有说明就可以
"""


def login_required(func):
    def wrapper(*args, **kwargs):
        try:
            g.user_id
        except Exception as e:
            current_app.logger.info(e)
            # 因为我们只是想要用户在访问某些界面时需要登陆时才能访问 此时一定有token所以也就有g.user_id
            # 当有g.user_id时不报错就会else 执行对应请求资源
            # 当没有g.user_id时就会报错我们先通知下日志在直接重定向
            # 这个重定向使用redirect 里面跟重定向的url 和 可加可不加的参数
            # 如果使用url_for 来重定向 则需要endpoint='user.userloginresource'(这里面是重定向的资源类)
            # redirect(url_for(endpoint='user.userloginresource'))  即蓝图名.目标资源类名
            return redirect('/user/login')
        else:
            return func(*args, **kwargs)
    return wrapper


