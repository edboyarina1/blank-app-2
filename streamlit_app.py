import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Функция для подключения к SQLite
def init_db():
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY,
            name TEXT,
            earnings INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()
    return conn

def load_leaderboard():
    conn = init_db()
    df = pd.read_sql_query("SELECT name, earnings, timestamp FROM leaderboard ORDER BY earnings DESC", conn)
    conn.close()
    return df

def save_result_to_db(name, earnings):
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leaderboard (name, earnings, timestamp) VALUES (?, ?, ?)", 
                   (name, earnings, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def simulate_job_application(input_iq):
    original_iq = 85
    hiring_threshold = 91
    undetectable_range = 15

    if input_iq < hiring_threshold:
        return "Вас не взяли на работу.", 0
    elif input_iq > original_iq + undetectable_range:
        cost = 3 * (input_iq - original_iq)
        return f"Вы были уволены. Вы потратили {cost} рублей.", -cost
    else:
        earnings = 100 - 3 * (input_iq - original_iq)
        return f"Вас взяли на работу. Ваш доход составил {earnings} рублей.", earnings

# Заголовок приложения
st.title("Симуляция приема на работу / Job Application Simulation")

# Выбор языка
language = st.selectbox("Выберите язык / Choose Language", ["Русский", "English"])

# Описание игры на двух языках
if language == "Русский":
    st.header("Ваше IQ: 85")
    st.markdown("""
    ### Описание игры "Симуляция приема на работу"

    Вам предстоит пройти собеседование в компанию, указав свой уровень IQ. Чем выше ваш IQ, тем больше шансов получить работу, но есть риск быть пойманным за фальсификацию.

    **Условия**:
    - За успешное прохождение собеседования вы получите 100 рублей.
    - За каждый балл IQ выше исходного уровня вы заплатите 3 рубля.

    **Возможные исходы**:
    1. **Вас взяли на работу** — вы получите 100 рублей минус стоимость повышения IQ.
    2. **Вас не взяли на работу** — вы ничего не заработаете.
    3. **Вас уволили за фальсификацию** — вы потеряете деньги, потраченные на повышение IQ.

    **Победитель** — тот, кого приняли на работу и у кого в итоге осталось больше всего денег.

    Введите желаемый уровень IQ и нажмите "Проверить результат". Попробуйте несколько раз!

    Удачи!
    """)
else:
    st.header("Your IQ: 85")
    st.markdown("""
    ### Game Description "Job Application Simulation"

    You need to go through a job interview by indicating your IQ level. The higher your IQ, the more likely you are to get hired, but there's a risk of being caught for fraud.

    **Conditions**:
    - If you successfully pass the interview, you will receive 100 rubles.
    - For each point of IQ above the base level, you will pay 3 rubles.

    **Possible Outcomes**:
    1. **You are hired** — you will receive 100 rubles minus the cost of raising your IQ.
    2. **You are not hired** — you earn nothing.
    3. **You are fired for fraud** — you lose the money spent on raising your IQ.

    **The winner** is the one who gets hired and has the most money left.

    Enter the desired IQ level and click "Check Result." Try multiple times!

    Good luck!
    """)

# Поле для ввода имени
name = st.text_input("Введите ваше имя / Enter your name")

# Ввод уровня IQ
input_iq = st.number_input("Введите уровень IQ / Enter your IQ:", min_value=50, max_value=150, step=1)

# Кнопка для проверки результата
if st.button("Проверить результат / Check Result"):
    # Вычисление результата
    result, earnings = simulate_job_application(input_iq)

    # Отображение результата
    st.write(result)

    # Сохранение результата в SQLite
    save_result_to_db(name, earnings)

# Загрузка и отображение текущего рейтинга
leaderboard = load_leaderboard()
if not leaderboard.empty:
    # Отображение таблицы только с именами
    st.markdown("### Рейтинг / Leaderboard")
    st.table(leaderboard[["name"]])
else:
    st.write("Рейтинг пока пуст / Leaderboard is empty")



