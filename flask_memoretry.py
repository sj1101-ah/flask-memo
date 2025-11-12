from flask import Flask, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

memo = []

print("123")

@app.route("/")
def main():
    item = ""
    q = request.args.get("q", "")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if q:
        filtered = []
        for i, m in enumerate(memo):
            if q.lower() in m['title'].lower():
                filtered.append((i, m))
    else:
        filtered = [(i, m) for i, m in enumerate(memo)]

    if not filtered:
        item += '<h3>메모가 없습니다.</h3>'
    else:
        for i, m in filtered:
            title = m['title']
            if m.get('underline', False):
                title = f"<s>{title}</s>"
            item += f'<li><input type="checkbox" name="delete_button" value="{i}"><a href="/update/{i}/">{title}</a> {m["now"]}</li>'
    return f'''
    <h1>메모장</h1>
    <form method="GET">
        <input type="text" name="q" value="{q}", placeholder="검색어 입력">
        <input type="submit" value="검색">
    </form>
    <form method="POST">
        <ol><h3>{item}</h3></ol>
        <input type="button" value="생성" onclick="location.href='/new/'">
        <input type="submit" value="삭제" formaction="/delete/">
        <input type="submit" value="밑줄긋기" formaction="/underline/">
    </form>
    '''

@app.route("/new/")
def new_memo():
    return f'''
    <form action="/save/" method="POST">
        <p><input type="text" placeholder="제목" maxlength="50" size="48" required name="title"></p>
        <p><textarea placeholder="내용" maxlength="1000" cols="50" required name="main"></textarea></p>
        <input type="submit" value="저장하기">
    </form>
    '''

@app.route("/save/", methods=['POST'])
def save_memo():
    global memo
    title = request.form['title']
    main = request.form['main']
    id = request.form.get("id")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if id is None:
        memo.append({'title':title, 'main':main, 'now':now})
    else:
        memo[int(id)] = {'title':title, 'main':main, 'now':now}
    return redirect(url_for('main'))


@app.route("/update/<int:id>/")
def update_memo(id):
    m = memo[id]
    return f'''
    <form action="/save/" method="POST">
        <input hidden name="id" value="{id}">
        <p><input type="text" placeholder="제목" maxlength="50" size="48" required name="title" value="{m['title']}"></p>
        <p><textarea placeholder="내용" maxlength="1000" cols="50" required name="main">{m['main']}</textarea></p>
        <input type="submit" value="수정하기">
    </form>
    '''

@app.route("/delete/", methods=['POST'])
def delete_memo():
    global memo
    a = request.form.getlist("delete_button")
    a = sorted(map(int, a), reverse=True)

    for i in a:
        del memo[i]

    return redirect(url_for('main'))


@app.route("/underline/", methods=['POST'])
def underline_memo():
    global memo
    a = request.form.getlist("delete_button")
    a = map(int, a)

    for i in a:
        memo[i]['underline'] = not memo[i].get('underline', False)
    
    return redirect(url_for('main'))



app.run(port=5000, debug=True)