import streamlit as st
import duckdb
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="📚 마당출판사 DuckDB 관리", layout="wide")

DB_PATH = "madang.duckdb"

CSV_CUSTOMER = "madang_csv/Customer_madang.csv"
CSV_BOOK     = "madang_csv/Book_madang.csv"
CSV_ORDERS   = "madang_csv/Orders_madang.csv"

@st.cache_resource
def get_conn():
    # DuckDB 파일 연결 (없으면 자동 생성)
    return duckdb.connect(DB_PATH)

def initialize_db(conn):
    # 테이블이 이미 있으면 skip
    tables = conn.execute("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema='main';
    """).fetchdf()

    if not tables.empty:
        return

    # CSV → 테이블 자동 생성
    conn.execute(f"""
        CREATE TABLE Customer AS
        SELECT * FROM read_csv_auto('{CSV_CUSTOMER}', header=True);
    """)

    conn.execute(f"""
        CREATE TABLE Book AS
        SELECT * FROM read_csv_auto('{CSV_BOOK}', header=True);
    """)

    conn.execute(f"""
        CREATE TABLE Orders AS
        SELECT * FROM read_csv_auto('{CSV_ORDERS}', header=True);
    """)

    st.success("CSV → DuckDB 초기화 완료!")


# DB 연결 + 초기화
conn = get_conn()
initialize_db(conn)

# 공용 함수
def df(q, params=None):
    return conn.execute(q, params or {}).fetchdf()

def exec(q, params=None):
    conn.execute(q, params or {})

st.title("📚 마당출판사 관리 (DuckDB)")

menu = st.sidebar.radio("메뉴 선택", ["📘 도서관리", "👤 고객관리", "💰 주문관리", "📊 매출분석"])

# ---------------------- 📘 도서관리 ----------------------
if menu == "📘 도서관리":
    st.subheader("📘 도서 목록")
    st.dataframe(df("SELECT * FROM Book ORDER BY bookid;"), use_container_width=True)

    with st.expander("➕ 신규 도서 등록"):
        c1, c2, c3, c4 = st.columns(4)
        bookid = c1.number_input("도서ID", min_value=1, step=1)
        bookname = c2.text_input("도서명")
        publisher = c3.text_input("출판사")
        price = c4.number_input("가격", min_value=0, step=1000)
        if st.button("등록"):
            exec("INSERT INTO Book VALUES (?, ?, ?, ?);", [bookid, bookname, publisher, price])
            st.success("등록 완료!")
            st.experimental_rerun()

    with st.expander("✏️ 도서 가격 수정/삭제"):
        books = df("SELECT bookid, bookname, price FROM Book ORDER BY bookid;")
        sel = st.selectbox("도서 선택", books["bookid"].astype(str) + " - " + books["bookname"])
        sel_id = int(sel.split(" - ")[0])
        new_price = st.number_input("새 가격", min_value=0, step=1000)
        colA, colB = st.columns(2)
        if colA.button("가격 수정"):
            exec("UPDATE Book SET price=? WHERE bookid=?;", [new_price, sel_id])
            st.success("수정 완료"); st.experimental_rerun()
        if colB.button("도서 삭제"):
            exec("DELETE FROM Book WHERE bookid=?;", [sel_id])
            st.warning("삭제 완료"); st.experimental_rerun()

# ---------------------- 👤 고객관리 ----------------------
elif menu == "👤 고객관리":
    st.subheader("👤 고객 목록")
    st.dataframe(df("SELECT * FROM Customer ORDER BY custid;"), use_container_width=True)

    with st.expander("➕ 신규 고객 등록"):
        c1, c2, c3, c4 = st.columns(4)
        custid = c1.number_input("고객ID", min_value=1, step=1)
        name = c2.text_input("이름")
        address = c3.text_input("주소")
        phone = c4.text_input("전화번호")
        if st.button("고객 등록"):
            exec("INSERT INTO Customer VALUES (?, ?, ?, ?);", [custid, name, address, phone])
            st.success("등록 완료!"); st.experimental_rerun()

# ---------------------- 💰 주문관리 ----------------------
elif menu == "💰 주문관리":
    st.subheader("💰 주문 목록")
    st.dataframe(df("""
        SELECT o.orderid, c.name AS 고객명, b.bookname AS 도서명, o.saleprice, o.orderdate
        FROM Orders o
        LEFT JOIN Customer c ON o.custid=c.custid
        LEFT JOIN Book b ON o.bookid=b.bookid
        ORDER BY o.orderid;
    """), use_container_width=True)

# ---------------------- 📊 매출분석 ----------------------
elif menu == "📊 매출분석":
    st.subheader("📊 고객별/출판사별/월별 매출")

    df_cust = df("""
        SELECT c.name AS 고객명, COUNT(*) AS 구매횟수, SUM(o.saleprice) AS 총매출
        FROM Orders o JOIN Customer c ON o.custid=c.custid
        GROUP BY c.name ORDER BY 총매출 DESC;
    """)
    st.write("### 🧍 고객별 매출")
    st.dataframe(df_cust, use_container_width=True)

    df_pub = df("""
        SELECT b.publisher AS 출판사, SUM(o.saleprice) AS 매출합계
        FROM Orders o JOIN Book b ON o.bookid=b.bookid
        GROUP BY b.publisher ORDER BY 매출합계 DESC;
    """)
    st.write("### 🏢 출판사별 매출")
    st.bar_chart(df_pub.set_index("출판사"))

    df_month = df("""
        SELECT strftime(orderdate, '%Y-%m') AS 월, SUM(saleprice) AS 월매출
        FROM Orders GROUP BY 1 ORDER BY 1;
    """)
    st.write("### 📆 월별 매출 추이")
    st.line_chart(df_month.set_index("월"))



