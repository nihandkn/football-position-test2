from flask import Flask, request, render_template_string

app = Flask(__name__)


# ============================================================
# POZİSYONLAR
# ============================================================

POSITION_NAMES = {
    "QB": "Quarterback",
    "RB": "Running Back",
    "WR": "Wide Receiver",
    "TE": "Tight End",
    "OL": "Offensive Line",
    "DL": "Defensive Line",
    "LB": "Linebacker",
    "DB": "Defensive Back"
}


POSITION_DESCRIPTIONS = {
    "QB":
        "Oyunu yönlendirme, karar verme ve pas atma becerilerinin "
        "ön planda olduğu pozisyon.",

    "RB":
        "Topla koşma, çeviklik, hız ve temas altında ilerleme "
        "becerisinin önemli olduğu pozisyon.",

    "WR":
        "Hız, rota koşma ve top yakalama becerisinin "
        "ön plana çıktığı pozisyon.",

    "TE":
        "Top yakalama ile fiziksel mücadeleyi birleştiren "
        "çok yönlü hücum pozisyonu.",

    "OL":
        "Takım arkadaşlarına alan açma, blok yapma ve fiziksel "
        "gücün ön planda olduğu pozisyon.",

    "DL":
        "Rakibin hücumunu fiziksel güç ve patlayıcılıkla "
        "bozmaya çalışan savunma pozisyonu.",

    "LB":
        "Top taşıyan oyuncuyu durdurma, oyunu okuma, hız ve "
        "fiziksel mücadelenin birlikte kullanıldığı pozisyon.",

    "DB":
        "Rakip receiver'ları savunma, pasları kesme, hız ve "
        "reaksiyon becerisinin önemli olduğu pozisyon."
}


# ============================================================
# SORULAR
# ============================================================

QUESTIONS = [

    {
        "type": "choice",
        "question":
            "Bir takım oyununda seni en çok hangisi heyecanlandırır?",
        "answers": {

            "A) Topla rakip oyuncuları geçmek": {
                "RB": 5,
                "WR": 2,
                "DB": 1
            },

            "B) Takım arkadaşına yardım etmek ve fiziksel mücadele etmek": {
                "OL": 5,
                "DL": 3,
                "TE": 3,
                "LB": 2
            },

            "C) Oyunu okuyup doğru anda doğru kararı vermek": {
                "QB": 5,
                "LB": 4,
                "DB": 3
            },

            "D) Topla koşan oyuncuyu yere indirip koşusunu engellemek": {
                "LB": 5,
                "DL": 4,
                "DB": 3
            },

            "E) Top havadayken gidip onu kapmak": {
                "WR": 5,
                "TE": 4,
                "DB": 3
            },

            "F) Rakibin top tutmasını engellemek": {
                "DB": 5,
                "LB": 2
            }
        }
    },

    {
        "type": "choice",
        "question":
            "Kendini fiziksel olarak nasıl tanımlarsın?",
        "answers": {

            "A) Hızlı ve çevik": {
                "WR": 5,
                "DB": 5,
                "RB": 4
            },

            "B) Güçlü ve iri ya da şişman": {
                "OL": 5,
                "DL": 5,
                "TE": 2
            },

            "C) Hem güçlü hem hareketli": {
                "LB": 5,
                "TE": 4,
                "DL": 3,
                "RB": 2
            },

            "D) Uzun ve atletik": {
                "WR": 4,
                "TE": 5,
                "QB": 2,
                "DB": 2
            },

            "E) Küçük/orta yapılı ama çok hareketli": {
                "RB": 5,
                "DB": 4,
                "WR": 4
            },

            "F) Henüz bilmiyorum": {
                "QB": 1,
                "RB": 1,
                "WR": 1,
                "TE": 1,
                "OL": 1,
                "DL": 1,
                "LB": 1,
                "DB": 1
            }
        }
    },

    {
        "type": "choice",
        "question":
            "20 metrelik bir yarışta arkadaşlarına göre genelde…",
        "answers": {

            "A) En hızlılardanım": {
                "WR": 5,
                "DB": 5,
                "RB": 5
            },

            "B) Ortalardayım": {
                "QB": 2,
                "LB": 2,
                "TE": 2,
                "RB": 2
            },

            "C) Çok hızlı değilim ama ilk birkaç metrem iyidir": {
                "DL": 5,
                "RB": 4,
                "LB": 3
            },

            "D) Hızlı değilim ama daha güçlüyüm": {
                "OL": 5,
                "DL": 5,
                "TE": 3
            },

            "E) Hiç bilmiyorum": {
                "QB": 1,
                "RB": 1,
                "WR": 1,
                "TE": 1,
                "OL": 1,
                "DL": 1,
                "LB": 1,
                "DB": 1
            }
        }
    },

    {
        "type": "choice",
        "question":
            "Hangisinde daha iyi olduğunu düşünüyorsun?",
        "answers": {

            "A) İtmek, çekmek, fiziksel mücadeleye girmek": {
                "OL": 5,
                "DL": 5,
                "LB": 3,
                "TE": 3
            },

            "B) Bir şeyi yakalamak (el-göz koordinasyonu)": {
                "WR": 5,
                "TE": 5,
                "DB": 3,
                "RB": 2
            },

            "C) Bir şeyi uzağa/doğru atmak": {
                "QB": 7
            },

            "D) Koşmak": {
                "RB": 5,
                "WR": 5,
                "DB": 4
            },

            "E) Hızlı yön değiştirmek": {
                "RB": 5,
                "DB": 5,
                "WR": 4
            },

            "F) Strateji kurmak ve çevremi okumak": {
                "QB": 5,
                "LB": 4,
                "DB": 3
            },

            "G) Hiçbir fikrim yok, denemem lazım": {
                "QB": 1,
                "RB": 1,
                "WR": 1,
                "TE": 1,
                "OL": 1,
                "DL": 1,
                "LB": 1,
                "DB": 1
            }
        }
    },

    {
        "type": "choice",
        "question":
            "Top sana geldi. Önünde de seni durdurmaya çalışan biri var. "
            "İlk içgüdün?",
        "answers": {

            "A) Hızımla yanından geçerim": {
                "WR": 4,
                "RB": 5,
                "DB": 2
            },

            "B) Ani yön değiştiririm": {
                "RB": 5,
                "WR": 3,
                "DB": 3
            },

            "C) Üzerine gider ve çarpışırım": {
                "RB": 5,
                "TE": 4,
                "LB": 3,
                "DL": 2
            },

            "D) Boş alanı bulmaya çalışırım": {
                "RB": 4,
                "WR": 3,
                "QB": 2
            },

            "E) Topu başka birine vermenin yolunu ararım": {
                "QB": 5,
                "RB": 2
            }
        }
    },

    {
        "type": "choice",
        "question":
            "Savunmada hangisi sana daha eğlenceli geliyor?",
        "answers": {

            "A) En öndeki yoğun fiziksel mücadeleye girmek": {
                "DL": 6,
                "LB": 3
            },

            "B) Top kimdeyse bulup yakalamak": {
                "LB": 6,
                "DB": 3,
                "DL": 2
            },

            "C) Rakibin koşacağı alanları önceden kapatmak": {
                "LB": 5,
                "DB": 4
            },

            "D) Hızlı bir oyuncuyu bire bir takip etmek, yapışmak": {
                "DB": 7
            },

            "E) Geride durup oyunun nereye gittiğini okumak": {
                "DB": 5,
                "LB": 4
            },

            "F) Hiç bilmiyorum ama denemek isterim": {
                "DL": 1,
                "LB": 1,
                "DB": 1
            }
        }
    },

    {
        "type": "choice",
        "question":
            "Hangisi sana daha çok benziyor?",
        "answers": {

            "A) İlk hamleyi yapan kişi olmayı severim": {
                "DL": 5,
                "RB": 4,
                "LB": 3
            },

            "B) Önce gözlemler, sonra harekete geçerim": {
                "DB": 4,
                "LB": 4,
                "QB": 3
            },

            "C) Baskı altında hızlı karar verebilirim": {
                "QB": 6,
                "LB": 3,
                "DB": 2
            },

            "D) Bana net bir görev verildiğinde çok iyi uygularım": {
                "OL": 5,
                "DL": 4,
                "TE": 2
            },

            "E) Rakibimin ne yapacağını çözmeye çalışmayı severim": {
                "DB": 5,
                "LB": 5,
                "QB": 3
            }
        }
    },

    {
        "type": "choice",
        "question":
            "Fiziksel temasa yaklaşımın nasıl?",
        "answers": {

            "A) Severim. Fiziksel mücadele beni motive eder.": {
                "OL": 5,
                "DL": 5,
                "LB": 5,
                "TE": 3,
                "RB": 2
            },

            "B) Sorun değil, alışabilirim.": {
                "RB": 3,
                "TE": 3,
                "LB": 3,
                "DB": 2
            },

            "C) Emin değilim, önce denemek isterim.": {
                "WR": 2,
                "DB": 2,
                "QB": 2,
                "RB": 1
            },

            "D) Temassız oynamayı tercih ederim.": {
                "WR": 4,
                "QB": 4,
                "DB": 2
            }
        }
    },

    {
        "type": "choice",
        "question":
            "Hangisi sana daha eğlenceli geliyor?",
        "answers": {

            "A) Birinin yakalayamayacağı kadar hızlı koşmak": {
                "WR": 5,
                "RB": 5,
                "DB": 3
            },

            "B) Havadan gelen zor bir topu yakalamak": {
                "WR": 6,
                "TE": 5,
                "DB": 3
            },

            "C) Birini fiziksel olarak durdurmak": {
                "LB": 5,
                "DL": 5,
                "OL": 3
            },

            "D) Arkadaşımın sayı yapabilmesi için önünü açmak": {
                "OL": 6,
                "TE": 4
            },

            "E) Rakibin ne yapacağını önceden fark etmek": {
                "DB": 5,
                "LB": 5,
                "QB": 3
            },

            "F) Herkesi yönlendirip oyunu yönetmek": {
                "QB": 7
            }
        }
    },

    {
        "type": "measurements",
        "question": "Boy ve kilo",
        "subtitle":
            "Boyunu santimetre, kilonu kilogram olarak yaz."
    },

    {
        "type": "choice",
        "question":
            "Daha önce düzenli spor yaptın mı?",
        "answers": {

            "A) Hayır, ilk kez başlayacağım": {
                "QB": 1,
                "RB": 1,
                "WR": 1,
                "TE": 1,
                "OL": 1,
                "DL": 1,
                "LB": 1,
                "DB": 1
            },

            "B) Fitness / bodybuilding": {
                "OL": 4,
                "DL": 4,
                "LB": 3,
                "TE": 3
            },

            "C) Futbol / futsal": {
                "WR": 4,
                "DB": 4,
                "RB": 4,
                "QB": 2
            },

            "D) Basketbol": {
                "WR": 5,
                "TE": 4,
                "DB": 3,
                "QB": 2
            },

            "E) Voleybol": {
                "WR": 4,
                "TE": 4,
                "DB": 2
            },

            "F) Atletizm": {
                "WR": 5,
                "RB": 5,
                "DB": 5
            },

            "G) Dövüş sporları": {
                "LB": 5,
                "DL": 4,
                "RB": 3,
                "OL": 3
            },

            "H) Rugby / Amerikan futbolu / flag football": {
                "QB": 3,
                "RB": 3,
                "WR": 3,
                "TE": 3,
                "OL": 3,
                "DL": 3,
                "LB": 3,
                "DB": 3
            },

            "I) Başka bir spor": {
                "QB": 1,
                "RB": 1,
                "WR": 1,
                "TE": 1,
                "OL": 1,
                "DL": 1,
                "LB": 1,
                "DB": 1
            }
        }
    },

    {
        "type": "choice",
        "question":
            "Sporda seni en iyi tanımlayan özellik hangisi?",
        "answers": {

            "A) Güç": {
                "OL": 5,
                "DL": 5,
                "LB": 4,
                "TE": 3
            },

            "B) Hız": {
                "WR": 5,
                "DB": 5,
                "RB": 5
            },

            "C) Çeviklik": {
                "RB": 5,
                "DB": 5,
                "WR": 4
            },

            "D) Dayanıklılık": {
                "LB": 4,
                "WR": 3,
                "DB": 3,
                "RB": 3
            },

            "E) Koordinasyon": {
                "WR": 5,
                "TE": 4,
                "DB": 3,
                "QB": 3
            },

            "F) Oyun zekâsı": {
                "QB": 6,
                "LB": 5,
                "DB": 4
            },

            "G) Rekabetçilik": {
                "LB": 3,
                "RB": 3,
                "DB": 3,
                "DL": 3
            },

            "H) Henüz bilmiyorum": {
                "QB": 1,
                "RB": 1,
                "WR": 1,
                "TE": 1,
                "OL": 1,
                "DL": 1,
                "LB": 1,
                "DB": 1
            }
        }
    },

    {
        "type": "choice",
        "question":
            "Takım içinde hangi rol sana daha doğal gelir?",
        "answers": {

            "A) Nerede ihtiyaç varsa orada olayım": {
                "LB": 4,
                "TE": 3,
                "RB": 2,
                "DB": 2
            },

            "B) Diğerlerinin işini kolaylaştırayım": {
                "OL": 6,
                "TE": 4,
                "LB": 2
            },

            "C) Topu bana verin": {
                "RB": 5,
                "WR": 5,
                "TE": 3
            },

            "D) Rakibin en iyi oyuncusunu bana verin": {
                "DB": 6,
                "LB": 4
            },

            "E) Önce öğreneyim, sonra karar veririm": {
                "QB": 2,
                "LB": 2,
                "DB": 2,
                "TE": 2
            }
        }
    },

    {
        "type": "choice",
        "question":
            "Son oyun. Kazanmak için tek bir görev seçmen gerekiyor:",
        "answers": {

            "A) Rakibin top taşıyan oyuncusunu durdurmak": {
                "LB": 6,
                "DL": 4,
                "DB": 3
            },

            "B) Topla rakiplerin arasından geçmek": {
                "RB": 6,
                "WR": 3
            },

            "C) Takım arkadaşına doğru pası atmak": {
                "QB": 7
            },

            "D) 30 metre koşup topu yakalamak": {
                "WR": 7,
                "TE": 4
            },

            "E) Havadan gelen rakip pasını kesmek": {
                "DB": 7,
                "LB": 3
            },

            "F) Takım arkadaşın için karşındakileri durdurmak": {
                "OL": 7,
                "TE": 4
            }
        }
    }

]


# ============================================================
# HTML
# ============================================================

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">

<head>
<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Football Position Test</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #050505;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
    min-height: 100vh;
}

.container {
    width: 92%;
    max-width: 560px;
    margin: auto;
    padding: 35px 18px 50px 18px;
}

.logo {
    color: #800020;
    font-weight: 900;
    font-size: 15px;
    letter-spacing: 4px;
    margin-bottom: 30px;
}

h1 {
    font-size: 36px;
    margin-bottom: 15px;
}

.subtitle {
    color: #999;
    line-height: 1.5;
    margin-bottom: 35px;
}

input {
    width: 100%;
    padding: 18px;
    margin-bottom: 14px;
    background: #111;
    border: 1px solid #333;
    color: white;
    border-radius: 8px;
    font-size: 17px;
}

input:focus {
    outline: none;
    border-color: #800020;
}

button {
    width: 100%;
    padding: 19px;
    border: none;
    border-radius: 8px;
    background: #800020;
    color: white;
    font-weight: bold;
    font-size: 18px;
    cursor: pointer;
}

.answer {
    display: block;
    background: #111;
    border: 2px solid #800020;
    border-radius: 10px;
    padding: 20px;
    margin: 14px 0;
    cursor: pointer;
}

.answer input {
    display: none;
}

.answer:has(input:checked) {
    background: #800020;
}

.question-block {
    margin-bottom: 70px;
}

.question-number {
    color: #800020;
    font-size: 13px;
    font-weight: bold;
    margin-bottom: 10px;
}

.question-title {
    font-size: 27px;
    font-weight: 800;
    margin-bottom: 15px;
}

.progress-background {
    width: 100%;
    height: 6px;
    background: #222;
    margin-bottom: 35px;
}

.progress {
    height: 100%;
    background: #800020;
}

.position {
    color: #800020;
    font-size: 48px;
    font-weight: 900;
}

.ranking {
    background: #111;
    padding: 18px;
    margin-bottom: 12px;
    border-left: 5px solid #800020;
}

.percent {
    float: right;
    color: #800020;
    font-weight: bold;
}

.result-poster {
    width: 100%;
    margin-top: 35px;
    border-radius: 12px;
}

</style>

</head>

<body>

<div class="container">

{% if page == "start" %}

<div class="logo">
FOOTBALL POSITION TEST
</div>

<h1>
Hangi pozisyonda oynamalısın?
</h1>

<div class="subtitle">
Soruları cevapla ve sana en uygun Amerikan futbolu pozisyonunu bul.
</div>

<form method="POST" action="/quiz">

<input
type="text"
name="name"
placeholder="Ad"
required>

<input
type="text"
name="surname"
placeholder="Soyad"
required>

<input
type="text"
name="class_name"
placeholder="Sınıf"
required>

<button type="submit">
TESTE BAŞLA
</button>

</form>

{% endif %}


{% if page == "quiz" %}

<form method="POST" action="/result">

<input type="hidden" name="name" value="{{ name }}">
<input type="hidden" name="surname" value="{{ surname }}">
<input type="hidden" name="class_name" value="{{ class_name }}">

{% for q in questions %}

{% set question_index = loop.index0 %}

<div class="question-block">

<div class="question-number">
SORU {{ loop.index }} / {{ questions|length }}
</div>

<div class="progress-background">

<div class="progress"
style="width: {{ (loop.index / questions|length) * 100 }}%">
</div>

</div>

<div class="question-title">
{{ q.question }}
</div>


{% if q.type == "measurements" %}

<div class="subtitle">
{{ q.subtitle }}
</div>

<input
type="number"
name="height"
placeholder="Boy (cm)"
required>

<input
type="number"
name="weight"
placeholder="Kilo (kg)"
required>


{% else %}

{% for answer in q.answers.keys() %}

<label class="answer">

<input
type="radio"
name="q{{ question_index }}"
value="{{ answer }}"
required>

{{ answer }}

</label>

{% endfor %}

{% endif %}

</div>

{% endfor %}


<button type="submit">
SONUCU GÖSTER
</button>

</form>

{% endif %}


{% if page == "result" %}

<div class="logo">
FOOTBALL POSITION TEST
</div>

<div class="position">
{{ best_position }}
</div>

<h2>
{{ best_name }}
</h2>

<p>
{{ description }}
</p>

<h3>
EN UYGUN 3 POZİSYON
</h3>

{% for result in top_three %}

<div class="ranking">

<strong>
#{{ loop.index }}
{{ result[1] }}
</strong>

<span class="percent">
{{ result[2] }}%
</span>

</div>

{% endfor %}


<img
src="{{ url_for('static', filename='5.png') }}"
class="result-poster"
alt="Join the Team">

{% endif %}

</div>

</body>
</html>
"""


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def start():
    return render_template_string(
        PAGE_TEMPLATE,
        page="start"
    )


@app.route("/quiz", methods=["POST"])
def quiz():

    return render_template_string(

        PAGE_TEMPLATE,

        page="quiz",

        name=request.form.get("name"),

        surname=request.form.get("surname"),

        class_name=request.form.get("class_name"),

        questions=QUESTIONS

    )


# ============================================================
# BOY / KİLO
# ============================================================

def add_measurement_scores(scores, height, weight):

    if height <= 170:
        scores["RB"] += 3
        scores["DB"] += 3
        scores["WR"] += 2

    elif height <= 185:
        scores["QB"] += 2
        scores["RB"] += 2
        scores["WR"] += 3
        scores["DB"] += 2
        scores["LB"] += 2

    else:
        scores["TE"] += 4
        scores["WR"] += 3
        scores["QB"] += 2
        scores["OL"] += 2
        scores["DL"] += 2


    if weight <= 70:
        scores["WR"] += 3
        scores["DB"] += 3
        scores["RB"] += 2

    elif weight <= 90:
        scores["RB"] += 3
        scores["DB"] += 2
        scores["WR"] += 2
        scores["QB"] += 2
        scores["LB"] += 2

    elif weight <= 105:
        scores["LB"] += 4
        scores["TE"] += 4
        scores["DL"] += 2
        scores["OL"] += 2

    else:
        scores["OL"] += 5
        scores["DL"] += 5
        scores["TE"] += 3


# ============================================================
# RESULT
# ============================================================

@app.route("/result", methods=["POST"])
def result():

    scores = {
        "QB": 0,
        "RB": 0,
        "WR": 0,
        "TE": 0,
        "OL": 0,
        "DL": 0,
        "LB": 0,
        "DB": 0
    }


    for index, question in enumerate(QUESTIONS):

        if question["type"] != "choice":
            continue

        answer = request.form.get(
            f"q{index}"
        )

        if answer:

            points = question[
                "answers"
            ][answer]

            for position, value in points.items():
                scores[position] += value


    height = int(
        request.form.get("height", 0)
    )

    weight = int(
        request.form.get("weight", 0)
    )


    add_measurement_scores(
        scores,
        height,
        weight
    )


    sorted_scores = sorted(

        scores.items(),

        key=lambda x: x[1],

        reverse=True

    )


    best_position = sorted_scores[0][0]

    max_score = sorted_scores[0][1]


    top_three = []


    for position, score in sorted_scores[:3]:

        percentage = round(
            score / max_score * 100
        )

        top_three.append(

            (
                position,
                POSITION_NAMES[position],
                percentage
            )

        )


    return render_template_string(

        PAGE_TEMPLATE,

        page="result",

        best_position=best_position,

        best_name=POSITION_NAMES[
            best_position
        ],

        description=POSITION_DESCRIPTIONS[
            best_position
        ],

        top_three=top_three

    )


# ============================================================
# LOCAL RUN
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)