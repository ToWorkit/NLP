#coding=utf-8
import web
import rank.rec_func as rec
urls = (
    '/', 'index',
    '/test', 'test',
)

app = web.application(urls, globals())
render = web.template.render('templates/')
web.template.Template.globals['render'] = render

class index:
    def GET(self,user_id=None):
        param = web.input()
        user_id = param.user_id
        ret_lst = rec.rec_func(user_id)
        return render.index(ret_lst)

class test:
    def GET(self):
        print(web.input())
        return '222'

if __name__ == "__main__":
    app.run()
