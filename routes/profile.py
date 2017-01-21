# *Created by zxiaobai on 17/1/11.
from routes import *
from werkzeug.utils import secure_filename
from models.user import User

main = Blueprint('profile', __name__)

UPLOAD_FOLDER = 'static/avatar'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@main.route('/update', methods=['POST'])
@current_user_required
def update(user):
    form = request.form
    user.update(form)
    msg = '修改成功'
    return api_response(True, message=msg)


@main.route('/upload', methods=['GET', 'POST'])
@current_user_required
def upload(user):
    if request.method == 'GET':
        return redirect(url_for('node.index'))

    elif request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            fname = user.username +secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, fname))
            user.avatar = fname
            user.save()
            return redirect(url_for('user.profile', username=user.username))
        return redirect(url_for('user.profile', username=user.username))
