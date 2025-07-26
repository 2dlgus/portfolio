from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = '임의의_시크릿키'

app.config['TEMPLATES_AUTO_RELOAD'] = True

# Neon DB 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hyeonlee_owner:npg_eHGtCD6OMw1d@ep-spring-mountain-a1d4pr8r-pooler.ap-southeast-1.aws.neon.tech/hyeonlee?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 메일 설정
app.config['MAIL_SERVER'] = 'smtp.naver.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'calm2hyeon@naver.com'
app.config['MAIL_PASSWORD'] = 'NM9EHJGUY5P8'
mail = Mail(app)

ADMIN_PASSWORD = "1604"

# Post 모델
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(400))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text)
    bg_image = db.Column(db.String(200))

    def __repr__(self):
        return f"<Post {self.title}>"

@app.template_filter('format_number')
def format_number(value):
    return f"{int(value):,}"

# 홈(메인)
@app.route('/')
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('index.html', posts=posts)

# 게시글 목록
@app.route('/postlist')
def postlist():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('postlist.html', posts=posts)

# 게시글 상세
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

# 새 글 작성 (관리자 비밀번호 필요)
@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form.get('title', '')
        subtitle = request.form.get('subtitle', '')
        content = request.form.get('content', '')
        bg_image = request.form.get('bg_image', '')
        admin_pw = request.form.get('admin_pw', '')

        # 비밀번호 체크
        if admin_pw != ADMIN_PASSWORD:
            flash("비밀번호가 일치하지 않습니다.", "danger")
            # 값 유지
            return redirect(url_for('new_post', title=title, subtitle=subtitle, content=content, bg_image=bg_image))

        post = Post(
            title=title,
            subtitle=subtitle,
            content=content,
            bg_image=bg_image,
            date=datetime.now()
        )
        db.session.add(post)
        db.session.commit()
        flash("새 글이 등록되었습니다!", "success")
        return redirect(url_for('postlist'))

    # GET (혹은 비번 오류시 값 복원)
    title = request.args.get('title', '')
    subtitle = request.args.get('subtitle', '')
    content = request.args.get('content', '')
    bg_image = request.args.get('bg_image', '')
    return render_template("new_post.html", title=title, subtitle=subtitle, content=content, bg_image=bg_image)

# 게시글 삭제 (관리자 비번 필요)
@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    admin_pw = request.form.get('admin_pw', '')
    if admin_pw != ADMIN_PASSWORD:
        flash("비밀번호가 일치하지 않습니다.", "danger")
        return redirect(url_for('postlist'))

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("글이 삭제되었습니다.", "success")
    return redirect(url_for('postlist'))

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        if request.form.get('admin_pw') != ADMIN_PASSWORD:
            flash("비밀번호가 일치하지 않습니다.", "danger")
            return redirect(url_for('edit_post', post_id=post.id))

        post.title = request.form.get('title')
        post.subtitle = request.form.get('subtitle')
        post.bg_image = request.form.get('bg_image')
        post.content = request.form.get('content')
        db.session.commit()

        flash("글이 수정되었습니다.", "success")
        return redirect(url_for('post', post_id=post.id))

    return render_template('edit_post.html', post=post)

# Insight 페이지
@app.route("/insight")
def insight():
    return render_template("insight.html")

@app.route('/insight/goal', methods=['GET', 'POST'])
def insight_goal():
    result = None

    if request.method == 'POST':
        try:
            principal = float(request.form['principal'])
            monthly = float(request.form['monthly'])
            target_amount = float(request.form.get('target_amount') or 0)
            expected_return = float(request.form.get('expected_return') or 0)
            years = int(request.form['years'])
            purpose = request.form.get('purpose', '')

            # 입력 유효성
            if not expected_return and not target_amount:
                flash("목표 금액 또는 수익률 중 하나는 필수입니다.", "danger")
                return redirect(url_for('insight_goal'))

            if not expected_return and target_amount:
                expected_return = 100 * ((target_amount / (principal + monthly * 12 * years)) ** (1/years) - 1)
            elif not target_amount and expected_return:
                target_amount = principal * ((1 + expected_return / 100) ** years)
                for i in range(1, years + 1):
                    target_amount += monthly * 12 * ((1 + expected_return / 100) ** (years - i))

            # 수익률 기준 종목 추천
            etf_data = {
                "VOO": 12.2,
                "QQQ": 16.5,
                "SPY": 11.8,
                "ARKK": 23.1
            }

            stock_data = {
                "AAPL": 17.2,
                "META": 18.0,
                "TSLA": 27.3,
                "JNJ": 8.3
            }

            def closest_match(data, value):
                return min(data.items(), key=lambda x: abs(x[1] - value))

            etf_match = closest_match(etf_data, expected_return)
            stock_match = closest_match(stock_data, expected_return)

            result = {
                'principal': principal,
                'monthly': monthly,
                'target_amount': round(target_amount),
                'expected_return': round(expected_return, 1),
                'years': years,
                'purpose': purpose,
                'etf': etf_match,
                'stock': stock_match,
            }

        except Exception as e:
            flash("입력값을 확인해주세요.", "danger")
            print("🔴 Error:", e)
            return redirect(url_for('insight_goal'))

    return render_template('insight_goal.html', result=result)

@app.route("/macro")
def macro():
    return render_template("macro.html")

@app.route("/rules")
def rules():
    return render_template("rules.html")

@app.route("/myprinciples")
def myprinciples():
    return render_template("myprinciples.html")

@app.route("/mlpredict")
def mlpredict():
    return render_template("mlpredict.html")

# About, Contact 등 기타 페이지
@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        msg = Message(
            subject=f"Portfolio Contact from {name}",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],
            body=f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
        )
        try:
            mail.send(msg)
            flash("메일이 성공적으로 전송되었습니다!", "success")
        except Exception as e:
            print("메일 전송 실패:", e)
            flash("메일 전송에 실패했습니다. 다시 시도해주세요.", "danger")
        return redirect(url_for('contact'))
    return render_template("contact.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)