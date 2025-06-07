from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = '임의의_시크릿키'

# 메일 설정
app.config['MAIL_SERVER'] = 'smtp.naver.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True   # 587+TLS
app.config['MAIL_USERNAME'] = 'calm2hyeon@naver.com'
app.config['MAIL_PASSWORD'] = 'NM9EHJGUY5P8'  # 또는 앱 비밀번호

mail = Mail(app)

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
            recipients=[app.config['MAIL_USERNAME']],  # 네이버 메일 본인 계정
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

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/postlist')
def postlist():
    return render_template('postlist.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return "Post not found", 404
    return render_template('post.html', post=post)

@app.route('/about')
def about():
    return render_template('about.html')

# 샘플 포스트 데이터 (여기서 id, title, date, subtitle, content 등)
posts = [
    {
        "id": 1,
        "title": "과유불급은 인생의 진리 중 하나라고 생각한다.",
        "subtitle": "오버아닌가?, 너무한데?, 지나친데?, 그렇게까지?, 너무 나간것 같은데? 같은 생각이 문득 든다면 우선 일시멈춤하려고 노력한다.",
        "date": "June 08, 2025",
        "content": """
            <p>제곧내. 냉무</p>
        """,
        "bg_image": "assets/img/post-2025060801-image.jpg"
    },
    {
        "id": 2,
        "title": "공홈과 백화점이 정도라고 생각한다.",
        "subtitle": "중요하고 고가의 물건일수록 물건의 공식 판매처(온/오프라인)나 백화점 등에서 사는 것이 정도(正道)라고 느껴왔다.",
        "date": "June 08, 2025",
        "content": """
            <p>싼건 이유가 있다는 내 아내의 명언과 일맥상통한다. 화장품을 예를들어 설명해보자면, 인터넷 최저가로 구매하면 유통기한을 먼저 확인한다. 테무에서 산 1,000원에 10개짜리 양말은? 양말 모양의 스타킹이었다. 물건이 아니더라도 여행도 마찬가지다. 하얏트월드 가입하고 공홈에서 예약하면, 수많은 중개업체를 통해 예약하는 것과 비슷하거나 오히려 더 저렴할 때도 있었다. 심지어 호텔 멤버십으로서 제공되는 서비스도 더 많았다.(진짜로) 여행하니까 생각이 이어지는데 대한항공 공홈에서 항공권을 구매하면 같은 economy 좌석일지라도 앞쪽이냐 뒷쪽이냐에 따라 금액이 다른걸 직접 확인할 수 있다. 난 해외 파견/출장이 많았던 관계로 소속했던 회사에서 끊어주는 대한항공 economy 석을 많이 경험했다. 회사에서 항공권을 끊어줄 때 보통 economy에서 가장 앞쪽에 비싼 좌석을 준다. business 좌석 업그레이드 경험도 있었다.</p>
        """,
        "bg_image": "assets/img/post-2025060802-image.jpg"
    },
    # 여기에 추가 포스트 넣으면 됨
]

if __name__ == '__main__':
    app.run(debug=True)