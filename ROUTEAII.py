import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
from streamlit_searchbox import st_searchbox
from google import genai
import math
from datetime import datetime, timedelta

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="RouteAI Enterprise",
    page_icon="🚚",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================


st.markdown("""
<style>

/* ===== FONT ===== */
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800&display=swap');

html,body,[class*="css"]{
    font-family:'Manrope',sans-serif;
}

/* ===== BACKGROUND MESH ===== */

.stApp{

background:
radial-gradient(circle at 12% 18%, #BEE3FF 0%, transparent 22%),
radial-gradient(circle at 88% 12%, #D7C5FF 0%, transparent 24%),
radial-gradient(circle at 78% 82%, #FFD8F4 0%, transparent 20%),
radial-gradient(circle at 20% 88%, #D8F5FF 0%, transparent 22%),
linear-gradient(135deg,#FCFDFF,#F5F8FF,#FFF9FF);

}

/* efek noise tipis */

.stApp:before{
content:"";
position:fixed;
inset:0;
background-image:radial-gradient(rgba(120,120,160,.05) 1px, transparent 1px);
background-size:24px 24px;
pointer-events:none;
}

/* ===== CONTAINER ===== */

.block-container{
max-width:1460px;
padding-top:20px;
}

/* ===== SIDEBAR ===== */

section[data-testid="stSidebar"]{

background:linear-gradient(180deg,#FFFFFF,#EEF5FF);

border-right:1px solid rgba(180,200,255,.45);

box-shadow:10px 0 35px rgba(80,120,255,.06);

}

section[data-testid="stSidebar"] *{
color:#254AA5;
}

/* ===== HERO ===== */

.hero{

background:
linear-gradient(135deg,#5CAEFF,#7D88FF,#B276FF);

border-radius:34px;

padding:46px;

position:relative;

overflow:hidden;

box-shadow:
0 30px 70px rgba(93,130,255,.28);

}

/* blob */

.hero:before{

content:"";

position:absolute;

width:300px;
height:300px;

right:-80px;
top:-100px;

background:rgba(255,255,255,.18);

border-radius:42% 58% 65% 35%;

transform:rotate(20deg);
}

/* blob kedua */

.hero:after{

content:"";

position:absolute;

width:180px;
height:180px;

left:-50px;
bottom:-60px;

background:rgba(255,255,255,.12);

border-radius:60% 40% 35% 65%;
}

/* popup */

.hero-popup{

background:rgba(255,255,255,.16);

backdrop-filter:blur(22px);

border:1px solid rgba(255,255,255,.35);

padding:30px;

border-radius:24px;

max-width:560px;

box-shadow:
0 15px 40px rgba(30,60,180,.18);

}

.hero-popup h1{
margin:0;
color:white!important;
font-size:48px;
font-weight:800;
}

.hero-popup p{
margin-top:12px;
color:white!important;
opacity:.95;
font-size:18px;
line-height:1.6;
}

/* ===== CARD ===== */

.card{

background:rgba(255,255,255,.84);

backdrop-filter:blur(20px);

border:1px solid rgba(255,255,255,.9);

border-radius:26px;

padding:22px;

box-shadow:
0 12px 35px rgba(120,140,255,.08),
0 2px 8px rgba(255,255,255,.7) inset;

transition:.28s;
}

.card:hover{

transform:translateY(-6px);

box-shadow:
0 22px 45px rgba(120,140,255,.18);
}

/* ===== SECTION TITLE ===== */

.section-title{

display:inline-flex;

align-items:center;

gap:10px;

padding:10px 18px;

background:white;

border-radius:999px;

border:1px solid #E2E8FF;

box-shadow:
0 8px 18px rgba(120,140,255,.08);

font-weight:700;

color:#3053B6;
}

/* ===== METRIC ===== */

[data-testid="metric-container"]{

background:white;

border:none;

border-radius:22px;

padding:18px;

box-shadow:
0 15px 28px rgba(100,120,255,.08),
0 3px 8px rgba(255,255,255,.9) inset;

}

[data-testid="metric-container"] label{
color:#7286B7;
}

[data-testid="stMetricValue"]{
color:#2445A8;
font-weight:800;
}

/* ===== BUTTON ===== */

.stButton>button{

height:50px;

border:none;

border-radius:16px;

font-weight:700;

background:
linear-gradient(90deg,#43B0FF,#8C6BFF);

color:white;

box-shadow:
0 10px 22px rgba(100,120,255,.22);

transition:.25s;
}

.stButton>button:hover{

transform:translateY(-3px);

box-shadow:
0 18px 32px rgba(100,120,255,.32);
}

/* ===== INPUT ===== */

.stTextInput input,
.stNumberInput input{

background:white!important;

border:2px solid #E1E9FF!important;

border-radius:15px!important;

}

.stTextInput input:focus,
.stNumberInput input:focus{

border-color:#79A8FF!important;

box-shadow:0 0 0 4px rgba(120,160,255,.18)!important;
}

/* ===== SELECT ===== */

div[data-baseweb="select"]>div{

background:white!important;

border:2px solid #E1E9FF!important;

border-radius:15px!important;
}

/* ===== TAB ===== */

.stTabs [role="tab"]{

background:white;

border-radius:14px;

padding:10px 18px;

margin-right:8px;

box-shadow:0 6px 12px rgba(120,140,255,.06);

}

.stTabs [aria-selected="true"]{

background:linear-gradient(90deg,#6EA8FF,#A47CFF);

color:white;
}

/* ===== PROGRESS ===== */

.stProgress>div>div>div{

background:linear-gradient(90deg,#5CAEFF,#A47CFF);
}

/* ===== SUCCESS ===== */

.stSuccess{

background:#EAFBF1!important;

border-radius:14px;
}

/* ===== HOVER CARD UNTUK SEMUA CONTAINER ===== */

div[data-testid="stVerticalBlock"]>div{

transition:.25s;
}

div[data-testid="stVerticalBlock"]>div:hover{

transform:translateY(-2px);
}
/* ===== CAPACITY ALERT ===== */

.capacity-warning{
    background:linear-gradient(135deg,#FFF1F2,#FFE4E6);
    border-left:6px solid #EF4444;
    border-radius:22px;
    padding:22px;
    margin:15px 0;
    box-shadow:0 12px 28px rgba(239,68,68,.12);
}

.capacity-safe{
    background:linear-gradient(135deg,#ECFDF5,#D1FAE5);
    border-left:6px solid #10B981;
    border-radius:22px;
    padding:22px;
    margin:15px 0;
    box-shadow:0 12px 28px rgba(16,185,129,.12);
}
footer{
visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================

defaults={

    "page":"Dashboard",

    "depot":None,

    "customers":[],

    "results":None,

    "capacity":200,

    "speed":40,

    "fuel_price":13500,

    "fuel_eff":12,

    "chat":[
        {
            "role":"assistant",
            "content":"Halo! Saya RouteAI Copilot. Saya siap membantu menganalisis beberapa alternatif rute."
        }
    ]

}

for k,v in defaults.items():
    st.session_state.setdefault(k,v)

# ==========================================
# SEARCH LOKASI
# ==========================================

@st.cache_data(show_spinner=False)
def search_locations(term):

    if len(term)<2:
        return []

    try:

        r=requests.get(

            "https://nominatim.openstreetmap.org/search",

            params={
                "q":term,
                "format":"jsonv2",
                "limit":6,
                "countrycodes":"id",
                "accept-language":"id"
            },

            headers={"User-Agent":"RouteAI"},

            timeout=10

        )

        return [x["display_name"] for x in r.json()]

    except:
        return []

@st.cache_data(show_spinner=False)
def get_location(place):

    try:

        r=requests.get(

            "https://nominatim.openstreetmap.org/search",

            params={
                "q":place,
                "format":"jsonv2",
                "limit":1,
                "countrycodes":"id",
                "accept-language":"id"
            },

            headers={"User-Agent":"RouteAI"},

            timeout=10

        )

        d=r.json()

        if not d:
            return None

        return{

            "name":d[0]["display_name"],

            "lat":float(d[0]["lat"]),

            "lon":float(d[0]["lon"])

        }

    except:
        return None

# ==========================================
# HAVERSINE
# ==========================================

def haversine(lat1,lon1,lat2,lon2):

    R=6371

    p1=math.radians(lat1)
    p2=math.radians(lat2)

    dp=math.radians(lat2-lat1)
    dl=math.radians(lon2-lon1)

    a=(

        math.sin(dp/2)**2

        +math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2

    )

    return 2*R*math.asin(math.sqrt(a))

# ==========================================
# OSRM
# ==========================================

@st.cache_data(show_spinner=False)
def osrm_route(points):

    coords=";".join(f"{lon},{lat}" for lat,lon in points)

    url=f"https://router.project-osrm.org/route/v1/driving/{coords}"

    try:

        r=requests.get(

            url,

            params={
                "overview":"full",
                "geometries":"geojson"
            },

            timeout=15

        )

        rt=r.json()["routes"][0]

        geom=[[lat,lon] for lon,lat in rt["geometry"]["coordinates"]]

        return{

            "geometry":geom,

            "distance":rt["distance"]/1000,

            "duration":rt["duration"]/60

        }

    except:

        return None

# ==========================================
# ALGORITMA
# ==========================================

def nearest_neighbor(start,customers):

    cur=start

    rem=customers.copy()

    out=[]

    while rem:

        nxt=min(

            rem,

            key=lambda x:haversine(

                cur[0],cur[1],x["lat"],x["lon"]

            )

        )

        out.append(nxt)

        cur=(nxt["lat"],nxt["lon"])

        rem.remove(nxt)

    return out

def fastest_delivery(start,customers):

    return sorted(

        customers,

        key=lambda x:haversine(

            start[0],start[1],x["lat"],x["lon"]

        )

    )

def balanced_route(start,customers):

    return sorted(

        customers,

        key=lambda x:(

            haversine(

                start[0],start[1],x["lat"],x["lon"]

            )

            +x["demand"]*0.3

        )

    )

# ==========================================
# CALCULATE ROUTE
# ==========================================

def calculate_route(start,order,speed):

    pts=[start]

    for c in order:
        pts.append((c["lat"],c["lon"]))

    pts.append(start)

    rt=osrm_route(pts)

    if rt:

        distance=rt["distance"]
        geometry=rt["geometry"]

    else:

        distance=0
        geometry=None

        cur=start

        for c in order:

            distance+=haversine(

                cur[0],cur[1],c["lat"],c["lon"]

            )

            cur=(c["lat"],c["lon"])

        distance+=haversine(

            cur[0],cur[1],start[0],start[1]

        )

    eta=distance/speed*60

    fuel_used=distance/st.session_state.fuel_eff

    fuel_cost=fuel_used*st.session_state.fuel_price

    co2=fuel_used*2.31

    return{

        "order":order,

        "geometry":geometry,

        "distance":distance,

        "eta":eta,

        "fuel_used":fuel_used,

        "fuel_cost":fuel_cost,

        "co2":co2

    }

# ==========================================
# AI GEMINI
# ==========================================

def ai_analysis(question):

    try:

        client=genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

        summary=""

        for n,d in st.session_state.results.items():

            summary+=f"""
{n}
Jarak:{d['distance']:.2f} km
ETA:{d['eta']:.0f} menit
Biaya:Rp{d['fuel_cost']:,.0f}
"""

        prompt=f"""
Kamu adalah RouteAI Copilot.

Jawab dalam Bahasa Indonesia.

Bandingkan ketiga rute bila relevan.

Data:
{summary}

Pertanyaan:
{question}
"""

        res=client.models.generate_content(

            model="gemini-2.5-flash",

            contents=prompt

        )

        return res.text

    except Exception as e:

        q=question.lower()

        best=min(

            st.session_state.results.items(),

            key=lambda x:x[1]["distance"]

        )

        fast=min(

            st.session_state.results.items(),

            key=lambda x:x[1]["eta"]

        )

        if "hemat" in q:
            return f"Rute paling hemat adalah **{best[0]}**."

        if "cepat" in q:
            return f"Rute tercepat adalah **{fast[0]}**."

        if "banding" in q:
            txt="## Perbandingan\n\n"

            for n,d in st.session_state.results.items():

                txt+=f"""**{n}**
- {d['distance']:.2f} km
- {d['eta']:.0f} menit
- Rp{d['fuel_cost']:,.0f}

"""

            return txt

        if "429" in str(e):
            return "Kuota Gemini sedang habis."

        return "AI sementara tidak tersedia."

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🚚 RouteAI")

    st.caption("Enterprise Dashboard")

    st.divider()

    st.session_state.page=st.radio(

        "Menu",

        ["Dashboard","Planner","AI Copilot"],

        index=["Dashboard","Planner","AI Copilot"].index(st.session_state.page)

    )

    st.divider()

    if st.button("🗑 Reset"):

        st.session_state.depot=None
        st.session_state.customers=[]
        st.session_state.results=None
        st.session_state.chat=[{
            "role":"assistant",
            "content":"Halo! Saya siap membantu lagi."
        }]
        st.rerun()

# ==========================================
# DASHBOARD
# ==========================================

if st.session_state.page=="Dashboard":

    st.markdown("""

<div class="hero">

<div class="hero-popup">
<h1>🚚 RouteAI Enterprise</h1>
<p>AI-powered delivery decision support dengan visual premium, real road routing, dan analisis cerdas dalam satu dashboard.</p>
</div>

</div>
""", unsafe_allow_html=True)

    distance=0
    eta=0
    cost=0

    if st.session_state.results:

        best=min(

            st.session_state.results.items(),

            key=lambda x:x[1]["distance"]

        )

        distance=best[1]["distance"]
        eta=best[1]["eta"]
        cost=best[1]["fuel_cost"]

    c1,c2,c3,c4=st.columns(4)

    cards=[
        ("👥","Customers",len(st.session_state.customers)),
        ("📍","Distance",f"{distance:.1f} km"),
        ("⛽","Fuel Cost",f"Rp {cost:,.0f}"),
        ("⏱","ETA",f"{eta:.0f} min")
    ]

    for col,(icon,title,val) in zip([c1,c2,c3,c4],cards):
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:left;">
                <div style="font-size:32px;">{icon}</div>
                <div style="font-size:13px;color:#8090BF;margin-top:8px;">
                    {title}
                </div>
                <div style="font-size:30px;font-weight:800;color:#2445A8;margin-top:6px;">
                    {val}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    left,right=st.columns([1.7,1])

# ==========================================
# PLANNER
# ==========================================

if st.session_state.page == "Planner":

    st.title("🗺 Route Planner")
    st.caption("Rancang pengiriman dan biarkan AI membandingkan beberapa alternatif rute.")

    left, right = st.columns([1, 1.4])

    # ======================================
    # PANEL KIRI
    # ======================================

    with left:

        with st.container(border=True):

            st.subheader("📍 Depot")

            depot_choice = st_searchbox(
                search_locations,
                placeholder="Cari depot...",
                label="Search Depot",
                key="depot_search"
            )

            if depot_choice:
                loc = get_location(depot_choice)
                if loc:
                    st.session_state.depot = loc

            if st.session_state.depot:
                st.success("Depot berhasil dipilih.")
                st.caption(st.session_state.depot["name"])

        st.write("")

        with st.container(border=True):

            st.subheader("🚚 Kendaraan")

            st.session_state.capacity = st.number_input(
                "Kapasitas (kg)",
                min_value=10,
                value=st.session_state.capacity,
                step=10
            )

            st.session_state.speed = st.slider(
                "Kecepatan (km/jam)",
                20, 80,
                st.session_state.speed
            )

        st.write("")

        with st.container(border=True):

            st.subheader("⛽ BBM")

            st.session_state.fuel_price = st.number_input(
                "Harga BBM (Rp/L)",
                min_value=5000,
                value=st.session_state.fuel_price,
                step=500
            )

            st.session_state.fuel_eff = st.slider(
                "Efisiensi BBM (km/L)",
                5, 25,
                st.session_state.fuel_eff
            )

        st.write("")

        with st.container(border=True):

            st.subheader("🌦 Kondisi")

            traffic = st.select_slider(
                "Lalu Lintas",
                options=["Normal", "Padat", "Macet"],
                value="Normal"
            )

            weather = st.selectbox(
                "Cuaca",
                ["☀️ Cerah", "🌤 Mendung", "🌧 Hujan"]
            )

    # ======================================
    # PANEL KANAN
    # ======================================

    with right:

        with st.container(border=True):

            st.subheader("📦 Tambah Customer")

            cname = st.text_input("Nama Customer")

            customer_choice = st_searchbox(
                search_locations,
                placeholder="Cari alamat customer...",
                label="Alamat",
                key="customer_search"
            )

            demand = st.number_input(
                "Demand (kg)",
                min_value=1,
                value=20
            )

            if st.button("➕ Tambah Customer"):

                if cname and customer_choice:

                    loc = get_location(customer_choice)

                    if loc:

                        st.session_state.customers.append({

                            "customer": cname,
                            "address": loc["name"],
                            "lat": loc["lat"],
                            "lon": loc["lon"],
                            "demand": demand

                        })

                        st.rerun()

                else:
                    st.error("Lengkapi nama dan alamat.")

        st.write("")

        st.subheader("📋 Customer List")

        if st.session_state.customers:

            for i, c in enumerate(st.session_state.customers):

                with st.container(border=True):

                    a, b = st.columns([5,1])

                    a.write(f"**{c['customer']}**")
                    a.caption(c["address"])
                    a.caption(f"Demand: {c['demand']} kg")

                    if b.button("🗑", key=f"delete_{i}"):

                        st.session_state.customers.pop(i)
                        st.rerun()

        else:

            st.info("Belum ada customer.")

        st.write("")

        st.subheader("🛰 Live Preview")

        if st.session_state.depot:

            preview = folium.Map(
                location=[
                    st.session_state.depot["lat"],
                    st.session_state.depot["lon"]
                ],
                zoom_start=12
            )

            folium.Marker(
                [
                    st.session_state.depot["lat"],
                    st.session_state.depot["lon"]
                ],
                tooltip="Depot",
                icon=folium.Icon(color="red")
            ).add_to(preview)

            for c in st.session_state.customers:

                folium.Marker(
                    [c["lat"], c["lon"]],
                    tooltip=c["customer"],
                    popup=c["address"],
                    icon=folium.Icon(color="blue")
                ).add_to(preview)

            st_folium(preview, height=350, width=None)

        else:
            st.info("Pilih depot terlebih dahulu.")
# ======================================
# CAPACITY ALERT
# ======================================

total_demand = sum(c["demand"] for c in st.session_state.customers)
capacity = st.session_state.capacity

if total_demand > capacity:

    overload = total_demand - capacity
    trips = math.ceil(total_demand / capacity)

    st.markdown(f"""
<div class="capacity-warning">

<h3>⚠️ Capacity Exceeded</h3>

<p>
Total muatan <b>{total_demand} kg</b> melebihi kapasitas kendaraan
<b>{capacity} kg</b>.
</p>

<p>
Muatan berlebih: <b>{overload} kg</b>
</p>

</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">

    ## 🤖 RouteAI Recommendation

    - **Minimal {trips} trip** atau **{trips} kendaraan** diperlukan.
    - Muatan berlebih sebesar **{overload} kg**.
    - Prioritaskan skenario **Balanced Route** agar distribusi beban lebih merata.
    - Pertimbangkan membagi pengiriman menjadi beberapa perjalanan.

    </div>
    """, unsafe_allow_html=True)

else:

    remaining = capacity - total_demand

    st.success(
        f"✅ Kapasitas masih aman. Sisa kapasitas: **{remaining} kg**."
    )
    st.write("")

    # ======================================
    # GENERATE ROUTE
    # ======================================

    generate = st.button(
    "🚀 Generate Route",
    type="primary",
    disabled=total_demand > capacity
)

    if generate:

        if st.session_state.depot is None:
            st.error("Pilih depot terlebih dahulu.")
            st.stop()

        if len(st.session_state.customers) == 0:
            st.error("Tambahkan minimal satu customer.")
            st.stop()

        actual_speed = st.session_state.speed

        if traffic == "Padat":
            actual_speed *= 0.80

        elif traffic == "Macet":
            actual_speed *= 0.60

        if weather == "🌤 Mendung":
            actual_speed *= 0.95

        elif weather == "🌧 Hujan":
            actual_speed *= 0.80

        depot = (
            st.session_state.depot["lat"],
            st.session_state.depot["lon"]
        )

        customers = st.session_state.customers

        with st.spinner("🤖 AI sedang membandingkan seluruh alternatif rute..."):

            shortest = nearest_neighbor(depot, customers)
            fastest = fastest_delivery(depot, customers)
            balanced = balanced_route(depot, customers)

            st.session_state.results = {

                "Shortest Distance": calculate_route(depot, shortest, actual_speed),

                "Fastest Delivery": calculate_route(depot, fastest, actual_speed),

                "Balanced Route": calculate_route(depot, balanced, actual_speed)

            }

        st.success("Tiga skenario berhasil dibuat.")
        st.rerun()

    # ======================================
    # HASIL SIMULASI
    # ======================================

    if st.session_state.results:

        st.divider()
        st.header("🗺 Route Comparison")

        tabs = st.tabs([
            "🔵 Shortest Distance",
            "🟢 Fastest Delivery",
            "🟠 Balanced Route"
        ])

        colors = {
            "Shortest Distance":"blue",
            "Fastest Delivery":"green",
            "Balanced Route":"orange"
        }

        summary=[]

        for tab, name in zip(tabs, colors.keys()):

            with tab:

                r = st.session_state.results[name]

                m = folium.Map(
                    location=[
                        st.session_state.depot["lat"],
                        st.session_state.depot["lon"]
                    ],
                    zoom_start=12
                )

                folium.Marker(
                    [
                        st.session_state.depot["lat"],
                        st.session_state.depot["lon"]
                    ],
                    tooltip="Depot",
                    icon=folium.Icon(color="red")
                ).add_to(m)

                for i, c in enumerate(r["order"], start=1):

                    folium.Marker(
                        [c["lat"], c["lon"]],
                        tooltip=f"{i}. {c['customer']}",
                        popup=c["address"],
                        icon=folium.DivIcon(
                            html=f"""
                            <div style="
                            background:{colors[name]};
                            color:white;
                            width:28px;
                            height:28px;
                            border-radius:50%;
                            text-align:center;
                            line-height:28px;
                            font-weight:bold;
                            border:2px solid white;">
                            {i}
                            </div>
                            """
                        )
                    ).add_to(m)

                if r["geometry"]:
                    folium.PolyLine(
                        r["geometry"],
                        color=colors[name],
                        weight=6
                    ).add_to(m)

                st_folium(m, height=450, width=None)

                a,b,c,d = st.columns(4)

                a.metric("Distance", f"{r['distance']:.2f} km")
                b.metric("ETA", f"{r['eta']:.0f} min")
                c.metric("Fuel", f"{r['fuel_used']:.2f} L")
                d.metric("Cost", f"Rp{r['fuel_cost']:,.0f}")

                st.metric("CO₂", f"{r['co2']:.2f} kg")

                # Kenapa rute ini dipilih

                if name=="Shortest Distance":
                    st.success("""
**Mengapa dipilih?**

- Jarak paling pendek.
- Biaya BBM paling rendah.
- Cocok untuk efisiensi operasional.
""")

                elif name=="Fastest Delivery":
                    st.info("""
**Mengapa dipilih?**

- ETA tercepat.
- Cocok untuk pesanan prioritas.
""")

                else:
                    st.warning("""
**Mengapa dipilih?**

- Menyeimbangkan jarak dan distribusi beban.
- Cocok untuk operasional harian.
""")

                # Timeline

                st.write("### 📦 Delivery Timeline")

                now = datetime.strptime("08:00","%H:%M")

                seg = r["eta"]/max(len(r["order"]),1)

                timeline=[]

                for x in r["order"]:

                    timeline.append({
                        "Customer":x["customer"],
                        "ETA":now.strftime("%H:%M")
                    })

                    now += timedelta(minutes=seg)

                st.dataframe(
                    pd.DataFrame(timeline),
                    use_container_width=True
                )

                summary.append({

                    "Scenario":name,
                    "Distance":round(r["distance"],2),
                    "ETA":round(r["eta"],1),
                    "Fuel Cost":round(r["fuel_cost"],0),
                    "CO₂":round(r["co2"],2)

                })

        # ======================================
        # ANALYTICS
        # ======================================

        st.divider()
        st.header("📊 Route Analytics")

        summary_df = pd.DataFrame(summary)

        st.dataframe(summary_df, use_container_width=True)

        chart = summary_df.set_index("Scenario")

        x,y = st.columns(2)

        with x:
            st.subheader("Distance Comparison")
            st.bar_chart(chart["Distance"])

        with y:
            st.subheader("Fuel Cost Comparison")
            st.bar_chart(chart["Fuel Cost"])

        best = summary_df.loc[summary_df["Distance"].idxmin()]
        fast = summary_df.loc[summary_df["ETA"].idxmin()]

        saving = (
            (
                summary_df["Distance"].max()
                - best["Distance"]
            )
            / summary_df["Distance"].max()
        )*100

        st.markdown(f"""
<div class="card">

## 🤖 AI Insight

- Rute paling efisien adalah **{best['Scenario']}**.
- Rute tercepat adalah **{fast['Scenario']}**.
- Potensi penghematan mencapai **{saving:.1f}%** dibanding rute terpanjang.

</div>
""", unsafe_allow_html=True)

        # ======================================
        # BEFORE VS AFTER
        # ======================================

        st.divider()
        st.header("⚖ Before vs After")

        depot = (
            st.session_state.depot["lat"],
            st.session_state.depot["lon"]
        )

        before=0
        cur=depot

        for c in st.session_state.customers:

            before+=haversine(cur[0],cur[1],c["lat"],c["lon"])

            cur=(c["lat"],c["lon"])

        before+=haversine(cur[0],cur[1],depot[0],depot[1])

        after=best["Distance"]

        before_cost=(before/st.session_state.fuel_eff)*st.session_state.fuel_price

        after_cost=best["Fuel Cost"]

        l,r = st.columns(2)

        with l:
            st.metric("Before (Urutan Input)", f"{before:.2f} km")
            st.metric("Fuel Cost", f"Rp{before_cost:,.0f}")

        with r:
            st.metric("After AI", f"{after:.2f} km")
            st.metric("Fuel Cost", f"Rp{after_cost:,.0f}")

        # ======================================
        # VEHICLE UTILIZATION
        # ======================================

        st.divider()
        st.header("🚚 Vehicle Utilization")

        total_demand = sum(c["demand"] for c in st.session_state.customers)

        util = min(
            (total_demand/st.session_state.capacity)*100,
            100
        )

        st.metric("Capacity Usage", f"{util:.1f}%")
        st.progress(util/100)

        util_df = pd.DataFrame({
            "Status":["Terpakai","Sisa"],
            "Value":[
                total_demand,
                max(st.session_state.capacity-total_demand,0)
            ]
        })

        st.subheader("Distribusi Kapasitas")
        st.bar_chart(util_df.set_index("Status"))

# ==========================================
# AI COPILOT
# ==========================================

if st.session_state.page=="AI Copilot":

    st.title("🤖 RouteAI Copilot")
    st.caption("AI Decision Support untuk membantu memilih strategi pengiriman terbaik.")

    if st.session_state.results is None:

        st.info("Silakan Generate Route terlebih dahulu di menu Planner.")

    else:

        ranking=sorted(
            st.session_state.results.items(),
            key=lambda x:x[1]["distance"]
        )

        best=ranking[0]

        fastest=min(
            st.session_state.results.items(),
            key=lambda x:x[1]["eta"]
        )

        # ======================================
        # EXECUTIVE SUMMARY
        # ======================================

        st.markdown(f"""
<div class="hero">

<h1>🚚 RouteAI Enterprise</h1>

<p style="font-size:20px;">
AI-Powered Delivery Decision Support System
</p>

<p>
Optimize delivery routes, fuel costs, ETA, and operational decisions
through intelligent route comparison.
</p>

<div style="
display:flex;
gap:18px;
margin-top:20px;
flex-wrap:wrap;
">

<div style="background:rgba(255,255,255,.15);
padding:12px 18px;
border-radius:14px;">
<b>{len(st.session_state.customers)}</b><br>Customers
</div>

<div style="background:rgba(255,255,255,.15);
padding:12px 18px;
border-radius:14px;">
<b>3</b><br>Route Scenarios
</div>

<div style="background:rgba(255,255,255,.15);
padding:12px 18px;
border-radius:14px;">
<b>AI</b><br>Gemini Copilot
</div>

<div style="background:rgba(255,255,255,.15);
padding:12px 18px;
border-radius:14px;">
<b>OSRM</b><br>Real Road Routing
</div>

</div>

</div>
""", unsafe_allow_html=True)

        st.write("")

        # ======================================
        # QUICK ACTION
        # ======================================

        st.subheader("⚡ Quick Action")

        q1,q2,q3=st.columns(3)

        with q1:

            if st.button("💰 Rute Paling Hemat"):

                prompt="Rute mana yang paling hemat?"

                st.session_state.chat.append({
                    "role":"user",
                    "content":prompt
                })

                with st.spinner("AI sedang berpikir..."):
                    ans=ai_analysis(prompt)

                st.session_state.chat.append({
                    "role":"assistant",
                    "content":ans
                })

                st.rerun()

        with q2:

            if st.button("⚡ Rute Tercepat"):

                prompt="Rute mana yang paling cepat?"

                st.session_state.chat.append({
                    "role":"user",
                    "content":prompt
                })

                with st.spinner("AI sedang berpikir..."):
                    ans=ai_analysis(prompt)

                st.session_state.chat.append({
                    "role":"assistant",
                    "content":ans
                })

                st.rerun()

        with q3:

            if st.button("📊 Bandingkan Semua Rute"):

                prompt="Bandingkan ketiga rute."

                st.session_state.chat.append({
                    "role":"user",
                    "content":prompt
                })

                with st.spinner("AI sedang berpikir..."):
                    ans=ai_analysis(prompt)

                st.session_state.chat.append({
                    "role":"assistant",
                    "content":ans
                })

                st.rerun()

        st.divider()

        # ======================================
        # CHAT HISTORY
        # ======================================

        st.subheader("💬 Chat")

        for msg in st.session_state.chat:

            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_question=st.chat_input(
            "Contoh: Mana rute terbaik kalau prioritasnya hemat BBM?"
        )

        if user_question:

            st.session_state.chat.append({
                "role":"user",
                "content":user_question
            })

            with st.chat_message("user"):
                st.markdown(user_question)

            with st.chat_message("assistant"):

                with st.spinner("AI sedang menganalisis..."):
                    answer=ai_analysis(user_question)

                st.markdown(answer)

            st.session_state.chat.append({
                "role":"assistant",
                "content":answer
            })

        st.divider()

        # ======================================
        # REKOMENDASI PERTANYAAN
        # ======================================

        st.subheader("💡 Pertanyaan yang Bisa Dicoba")

        st.markdown("""
- Mana rute yang paling hemat biaya BBM?
- Apa perbedaan Shortest Distance dan Fastest Delivery?
- Kenapa Balanced Route dipilih?
- Customer mana yang paling jauh dari depot?
- Berapa potensi penghematan dibanding rute biasa?
- Jika hujan, strategi mana yang lebih cocok?
- Bagaimana mengurangi emisi CO₂?
""")

        st.divider()

        # ======================================
        # DECISION SUPPORT TABLE
        # ======================================

        st.subheader("🧠 AI Decision Support")

        compare_df=pd.DataFrame([

            {
                "Skenario":"Shortest Distance",
                "Kelebihan":"Hemat BBM",
                "Cocok":"Biaya Operasional"
            },

            {
                "Skenario":"Fastest Delivery",
                "Kelebihan":"ETA Tercepat",
                "Cocok":"Deadline Ketat"
            },

            {
                "Skenario":"Balanced Route",
                "Kelebihan":"Seimbang",
                "Cocok":"Distribusi Harian"
            }

        ])

        st.dataframe(
            compare_df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("""
<div class="card">

### Mengapa AI memberikan beberapa alternatif?

RouteAI tidak hanya mencari satu rute terbaik. Sistem membandingkan
beberapa skenario sehingga pengguna dapat memilih strategi sesuai
prioritas operasional, apakah ingin menghemat biaya, mengejar waktu,
atau menjaga keseimbangan distribusi.

</div>
""",unsafe_allow_html=True)

# ==========================================
# EXPORT REPORT
# ==========================================

st.divider()

if st.session_state.results:

    st.header("📄 Export Report")

    best=min(
        st.session_state.results.items(),
        key=lambda x:x[1]["distance"]
    )

    report=f"""
ROUTEAI ENTERPRISE REPORT
=========================

Tanggal:
{datetime.now().strftime("%d/%m/%Y %H:%M")}

Depot:
{st.session_state.depot["name"]}

Jumlah Customer:
{len(st.session_state.customers)}

REKOMENDASI AI
--------------
{best[0]}

Distance:
{best[1]["distance"]:.2f} km

ETA:
{best[1]["eta"]:.0f} menit

Fuel Used:
{best[1]["fuel_used"]:.2f} L

Fuel Cost:
Rp{best[1]["fuel_cost"]:,.0f}

CO₂:
{best[1]["co2"]:.2f} kg

Generated by RouteAI Enterprise
"""

    csv_data=pd.DataFrame([

        {
            "Scenario":name,
            "Distance (km)":data["distance"],
            "ETA (min)":data["eta"],
            "Fuel Cost":data["fuel_cost"],
            "CO₂":data["co2"]
        }

        for name,data in st.session_state.results.items()

    ])

    c1,c2=st.columns(2)

    with c1:

        st.download_button(
            "📥 Download TXT Report",
            report,
            "RouteAI_Report.txt",
            mime="text/plain"
        )

    with c2:

        st.download_button(
            "📊 Download CSV Summary",
            csv_data.to_csv(index=False),
            "RouteAI_Summary.csv",
            mime="text/csv"
        )

    st.divider()

    # ======================================
    # SUSTAINABILITY SCORE
    # ======================================

    st.header("🌱 Sustainability Score")

    co2=best[1]["co2"]

    if co2<5:
        score=95
        label="Excellent"

    elif co2<10:
        score=82
        label="Good"

    elif co2<20:
        score=68
        label="Moderate"

    else:
        score=50
        label="Needs Improvement"

    st.metric(
        "Sustainability Score",
        f"{score}/100"
    )

    st.progress(score/100)

    st.caption(f"Kategori: **{label}**")

    st.markdown(f"""
<div class="card">

### 🌍 AI Environmental Insight

Estimasi emisi perjalanan sekitar **{co2:.2f} kg CO₂**.

Dengan memilih rute **{best[0]}**, perusahaan dapat mengurangi
jarak tempuh sehingga konsumsi bahan bakar dan emisi karbon menjadi
lebih efisien dibandingkan rute yang lebih panjang.

</div>
""",unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown("""
<div style="
text-align:center;
padding:30px;
background:linear-gradient(135deg,#0B5FFF,#60A5FA);
border-radius:22px;
color:white;
">

<h2>🚚 RouteAI Enterprise</h2>

<p>AI-Powered Delivery Decision Support System</p>

<p>Built with Streamlit • OpenStreetMap • OSRM • Gemini AI</p>

<p>© 2026 RouteAI Enterprise</p>

</div>
""",unsafe_allow_html=True)