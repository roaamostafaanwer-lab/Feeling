from flask import Flask, render_template_string, request

app = Flask(__name__)

STYLE = """
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: 'Tajawal', sans-serif;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
  display: flex; align-items: center; justify-content: center;
  color: #fff; padding: 20px;
}
.card {
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 28px;
  padding: 44px 36px;
  width: 90%; max-width: 480px;
  text-align: center;
  backdrop-filter: blur(12px);
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
  animation: fadeIn 0.5s ease;
}
@keyframes fadeIn { from{opacity:0;transform:translateY(24px)} to{opacity:1;transform:translateY(0)} }
.big-emoji { font-size: 3.5rem; display:block; margin-bottom:16px; animation: bounce 2s infinite; }
@keyframes bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
h2 {
  font-size: 1.8rem; font-weight: 900; margin-bottom: 8px;
  background: linear-gradient(135deg, #a78bfa, #f472b6);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.sub { color: rgba(255,255,255,0.55); margin-bottom: 28px; font-size: 1rem; line-height:1.6; }
input[type=text] {
  width:100%; padding:15px 20px; border-radius:14px;
  border:2px solid rgba(167,139,250,0.4);
  background:rgba(255,255,255,0.07);
  color:#fff; font-size:1.1rem; font-family:'Tajawal',sans-serif;
  text-align:right; outline:none; margin-bottom:18px; transition:all 0.3s;
}
input[type=text]:focus { border-color:#a78bfa; background:rgba(167,139,250,0.1); }
input::placeholder { color:rgba(255,255,255,0.3); }
.btn-main {
  width:100%; padding:15px; border:none; border-radius:50px;
  background:linear-gradient(135deg,#7c3aed,#db2777);
  color:#fff; font-size:1.15rem; font-family:'Tajawal',sans-serif;
  font-weight:700; cursor:pointer;
  box-shadow:0 4px 20px rgba(124,58,237,0.4); transition:all 0.3s;
}
.btn-main:hover { transform:translateY(-3px); box-shadow:0 8px 30px rgba(124,58,237,0.6); }
.moods { display:flex; gap:14px; justify-content:center; flex-wrap:wrap; margin-bottom:10px; }
.mood-btn {
  flex:1; min-width:120px; max-width:140px;
  padding:22px 14px; border-radius:20px;
  border:2px solid rgba(255,255,255,0.12);
  background:rgba(255,255,255,0.05);
  color:#fff; font-size:0.95rem; font-family:'Tajawal',sans-serif;
  font-weight:700; cursor:pointer;
  display:flex; flex-direction:column; align-items:center; gap:10px;
  transition:all 0.3s;
}
.mood-btn .em { font-size:2.6rem; transition:transform 0.3s; }
.mood-btn:hover { transform:translateY(-8px); }
.mood-btn:hover .em { transform:scale(1.2) rotate(5deg); }
.happy:hover { background:rgba(251,191,36,0.2); border-color:#fbbf24; box-shadow:0 0 30px rgba(251,191,36,0.3); }
.sad:hover   { background:rgba(59,130,246,0.2);  border-color:#3b82f6; box-shadow:0 0 30px rgba(59,130,246,0.3); }
.angry:hover { background:rgba(239,68,68,0.2);   border-color:#ef4444; box-shadow:0 0 30px rgba(239,68,68,0.3); }
.wish-box {
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,255,255,0.12);
  border-radius:16px; padding:18px 20px; margin-bottom:14px; text-align:right;
}
.wish-label { font-size:0.9rem; color:#a78bfa; font-weight:700; margin-bottom:8px; }
textarea {
  width:100%; padding:12px; border-radius:12px;
  border:1px solid rgba(255,255,255,0.15);
  background:rgba(255,255,255,0.05);
  color:#fff; font-size:1rem; font-family:'Tajawal',sans-serif;
  text-align:right; outline:none; resize:none; min-height:75px; transition:all 0.3s;
}
textarea:focus { border-color:#a78bfa; background:rgba(167,139,250,0.08); }
textarea::placeholder { color:rgba(255,255,255,0.25); }
.divider { width:50px; height:3px; background:linear-gradient(90deg,#a78bfa,#f472b6); border-radius:10px; margin:18px auto; }
.result-wish {
  background:rgba(255,255,255,0.05); border-radius:16px;
  padding:16px 20px; margin-bottom:12px; text-align:right;
  border-right:4px solid #a78bfa;
}
.result-wish.pink { border-right-color:#f472b6; }
.result-wish .rlabel { font-size:0.85rem; color:#a78bfa; font-weight:700; margin-bottom:6px; }
.result-wish.pink .rlabel { color:#f472b6; }
.result-wish .rtext { color:rgba(255,255,255,0.85); line-height:1.6; }
.data-table { width:100%; border-collapse:collapse; direction:rtl; margin-top:20px; }
.data-table th { background:#7c3aed; color:#fff; padding:12px; font-family:'Tajawal',sans-serif; }
.data-table td { padding:10px 12px; border-bottom:1px solid rgba(255,255,255,0.1); color:rgba(255,255,255,0.85); font-family:'Tajawal',sans-serif; }
</style>
"""

home_page = """<!DOCTYPE html><html lang="ar" dir="rtl">
<head><title>كيف حالك؟</title>""" + STYLE + """</head>
<body><div class="card">
  <span class="big-emoji">✨</span>
  <h2>أهلاً بيك!</h2>
  <p class="sub">بعتلك اللينك ده <strong style="color:#f472b6">{{sender}}</strong> 💌<br>اكتب اسمك الأول عشان نبدأ</p>
  <form method="post" action="/mood">
    <input type="hidden" name="sender" value="{{sender}}">
    <input type="text" name="name" placeholder="اسمك هنا..." required>
    <button class="btn-main" type="submit">يلا نكمل →</button>
  </form>
</div></body></html>"""

mood_page = """<!DOCTYPE html><html lang="ar" dir="rtl">
<head><title>حالتك إيه؟</title>""" + STYLE + """</head>
<body><div class="card">
  <span class="big-emoji">💭</span>
  <h2>أهلاً {{name}}! 👋</h2>
  <p class="sub">إزيك النهارده؟ اختار اللي بتحس بيه</p>
  <form method="post" action="/wish">
    <input type="hidden" name="name" value="{{name}}">
    <input type="hidden" name="sender" value="{{sender}}">
    <div class="moods">
      <button class="mood-btn happy" name="mood" value="😊 فرحان">
        <span class="em">😊</span>فرحان
      </button>
      <button class="mood-btn sad" name="mood" value="😢 زعلان">
        <span class="em">😢</span>زعلان
      </button>
      <button class="mood-btn angry" name="mood" value="😡 متعصب">
        <span class="em">😡</span>متعصب
      </button>
    </div>
  </form>
</div></body></html>"""

wish_page = """<!DOCTYPE html><html lang="ar" dir="rtl">
<head><title>أمنيتك</title>""" + STYLE + """</head>
<body><div class="card">
  <span class="big-emoji">🌠</span>
  <h2>اتمنى أمنيتك!</h2>
  <p class="sub">{{name}} • {{mood}}</p>
  <form method="post" action="/result">
    <input type="hidden" name="name" value="{{name}}">
    <input type="hidden" name="mood" value="{{mood}}">
    <input type="hidden" name="sender" value="{{sender}}">
    <div class="wish-box">
      <div class="wish-label">🌟 أمنيتك لنفسك</div>
      <textarea name="wish_you" placeholder="اتمنى إن..." required></textarea>
    </div>
    <div class="wish-box">
      <div class="wish-label">💌 أمنيتك لـ {{sender}}</div>
      <textarea name="wish_sender" placeholder="أتمنالك إن..." required></textarea>
    </div>
    <button class="btn-main" type="submit">إرسال 💌</button>
  </form>
</div></body></html>"""

result_page = """<!DOCTYPE html><html lang="ar" dir="rtl">
<head><title>شكراً!</title>""" + STYLE + """</head>
<body><div class="card">
  <span class="big-emoji">💖</span>
  <h2>شكراً يا {{name}}!</h2>
  <p class="sub">ردك اتبعت لـ <strong style="color:#f472b6">{{sender}}</strong> بنجاح ✅</p>
  <div class="divider"></div>
  <div class="result-wish">
    <div class="rlabel">🌟 أمنيتك لنفسك</div>
    <div class="rtext">{{wish_you}}</div>
  </div>
  <div class="result-wish pink">
    <div class="rlabel">💌 أمنيتك لـ {{sender}}</div>
    <div class="rtext">{{wish_sender}}</div>
  </div>
  <p style="color:rgba(255,255,255,0.35);margin-top:20px;font-size:0.9rem">ربنا يحقق أمنياتك كلها 🤍</p>
</div></body></html>"""

@app.route("/")
def home():
    sender = request.args.get("from", "صاحبك")
    return render_template_string(home_page, sender=sender)

@app.route("/mood", methods=["POST"])
def mood():
    name = request.form["name"]
    sender = request.form["sender"]
    return render_template_string(mood_page, name=name, sender=sender)

@app.route("/wish", methods=["POST"])
def wish():
    name = request.form["name"]
    mood_val = request.form["mood"]
    sender = request.form["sender"]
    return render_template_string(wish_page, name=name, mood=mood_val, sender=sender)

@app.route("/result", methods=["POST"])
def result():
    name = request.form["name"]
    mood_val = request.form["mood"]
    sender = request.form["sender"]
    wish_you = request.form["wish_you"]
    wish_sender = request.form["wish_sender"]
    with open("data.txt", "a", encoding="utf-8") as f:
        f.write(f"{sender}|{name}|{mood_val}|{wish_you}|{wish_sender}\n")
    return render_template_string(result_page, name=name, sender=sender,
                                   wish_you=wish_you, wish_sender=wish_sender)

@app.route("/mydata")
def mydata():
    sender = request.args.get("name", "")
    results = []
    try:
        with open("data.txt", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 5 and parts[0] == sender:
                    results.append(parts[1:])
    except:
        pass
    rows = "".join(
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
        for r in results
    )
    return f"""<!DOCTYPE html><html lang="ar" dir="rtl">
<head><title>ردودك</title>{STYLE}</head>
<body style="display:block;padding:30px;background:#0f0c29">
<h2 style="background:linear-gradient(135deg,#a78bfa,#f472b6);-webkit-background-clip:text;
-webkit-text-fill-color:transparent;font-family:Tajawal,sans-serif;font-size:1.8rem;margin-bottom:20px">
📊 ردود الناس عليك يا {sender}</h2>
{"<p style='color:rgba(255,255,255,0.5);font-family:Tajawal,sans-serif'>لا يوجد ردود بعد 😢</p>"
if not results else
f"<table class='data-table'><tr><th>الاسم</th><th>الحالة</th><th>أمنيته</th><th>أمنيته لك</th></tr>{rows}</table>"}
</body></html>"""

if __name__ == "__main__":
    app.run(debug=True)
