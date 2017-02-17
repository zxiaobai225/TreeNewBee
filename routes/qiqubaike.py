# *Created by zxiaobai on 17/2/5.

from routes import *


main = Blueprint('qiqu', __name__)


@main.route('')
@current_user_required
def index(user):
    page = request.args.get('page', 0, type=int)
    max_pos = str(int(get_max_pos())-1800000*page)
    content = get_content(QIQU, max_pos)
    result = []
    l = len(content['data'])
    c = content['data']
    for i in range(l):
        hot_comment = c[i].get('hot_comment', '')
        media_data = c[i].get('media_data', '')
        wifi_img_url = ''
        data_gif = ''
        if hot_comment != '':
            hot_comment = hot_comment.get('message', '')

        if media_data != '':
            try:
                wifi_img_url = media_data[0].get('wifi_img_url', '')
            except:
                wifi_img_url = ''
            if media_data[0].get('format', '') == 'GIF':
                data_gif = media_data[0]['origin_img_url'].get('origin_pic_url', '')
        r = dict(
                 avatar=c[i]['avatar'],
                 username=c[i]['user_name'],
                 title=c[i].get('title', ''),
                 content=c[i].get('content', ''),
                 hot_comment=hot_comment,
                 wifi_img_url=wifi_img_url,
                 like=c[i]['_incrs'].get('like', 0),
                 dislike=c[i]['_incrs'].get('dislike', 0),
                 data_gif=data_gif,
                 page=page,
                )
        result.append(r)
    if page == 0:
        return render_template('index.html', user=user, data=result, page=page)
    status, data, message = True, result, '加载成功'
    return api_response(status, data, message)
