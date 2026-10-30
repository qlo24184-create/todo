import json
from datetime import date
from pathlib import Path

import streamlit as st

# 花蓮觀光旅遊網 UX 優化展示版
# 本程式為獨立展示原型，並非官方網站實際修改。
# 將本程式與 hualien_trip_checklist.json 放在同一資料夾。

st.set_page_config(
    page_title="花蓮旅遊網｜UX 優化展示版",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

TODO_FILE = Path(__file__).with_name("hualien_trip_checklist.json")
DAILY_LIMIT = 10

# -----------------------------
# 多語系文字
# -----------------------------
TEXT = {
    "繁體中文": {
        "brand": "花蓮旅遊網",
        "nav": "首頁　｜　景點探索　｜　推薦行程　｜　旅行清單",
        "hero_title": "探索花蓮，從山海開始",
        "hero_sub": "用更簡單的方式，規劃你的花蓮旅行。",
        "search": "搜尋景點、地區或活動",
        "search_button": "搜尋",
        "popular": "熱門旅遊服務",
        "tickets": "熱門票券",
        "tickets_desc": "快速掌握體驗活動與預約資訊",
        "itinerary": "推薦行程",
        "itinerary_desc": "依旅遊天數探索花蓮",
        "assistant": "AI 旅遊小助理",
        "assistant_desc": "詢問景點、交通與行程規劃",
        "accessibility": "無障礙設定",
        "accessibility_desc": "調整文字大小與顯示對比",
        "attractions": "景點探索",
        "region": "選擇地區",
        "kind": "景點類型",
        "all": "全部",
        "north": "北區",
        "central": "中區",
        "south": "南區",
        "coast": "海岸景觀",
        "nature": "自然景觀",
        "culture": "文化體驗",
        "family": "親子休閒",
        "days": "選擇旅遊天數",
        "recommend": "產生推薦行程",
        "trip_list": "我的旅行待辦事項",
        "basic": "旅遊基本資料（選填）",
        "start": "開始日期",
        "end": "結束日期",
        "adults": "大人人數",
        "children": "小孩人數",
        "rooms": "客房需求（可複選）",
        "other_room": "其他房型需求",
        "save_basic": "儲存旅遊基本資料",
        "save_tasks": "儲存完成狀態",
        "add_task": "新增旅行待辦事項",
        "task_name": "待辦事項名稱",
        "task_details": "補充說明（選填）",
        "add": "新增事項",
        "all_tasks": "全部事項",
        "done": "已完成",
        "remaining": "尚未完成",
        "ask": "輸入你的問題",
        "send": "送出問題",
        "remaining_quota": "今日剩餘免費詢問額度",
        "quota_warning": "溫馨提醒：免費詢問額度即將用完。",
        "quota_end": "今日免費使用額度已用完，歡迎明日再來詢問。",
        "font": "文字大小",
        "contrast": "高對比模式",
        "normal": "一般",
        "large": "放大",
        "xlarge": "特大",
        "footer": "UX 優化展示原型｜非花蓮官方網站實際修改",
        "no_result": "找不到符合條件的景點，請調整搜尋文字或分類。"
    },
    "English": {
        "brand": "Hualien Travel",
        "nav": "Home　｜　Explore　｜　Itineraries　｜　My Checklist",
        "hero_title": "Discover Hualien, from mountains to sea",
        "hero_sub": "Plan your Hualien trip with a simpler experience.",
        "search": "Search attractions, areas or activities",
        "search_button": "Search",
        "popular": "Popular Travel Services",
        "tickets": "Popular Tickets",
        "tickets_desc": "Explore activities and booking information",
        "itinerary": "Suggested Itineraries",
        "itinerary_desc": "Explore Hualien by trip length",
        "assistant": "AI Travel Assistant",
        "assistant_desc": "Ask about attractions, transport and itineraries",
        "accessibility": "Accessibility",
        "accessibility_desc": "Adjust text size and contrast",
        "attractions": "Explore Attractions",
        "region": "Region",
        "kind": "Attraction Type",
        "all": "All",
        "north": "North",
        "central": "Central",
        "south": "South",
        "coast": "Coastal",
        "nature": "Nature",
        "culture": "Culture",
        "family": "Family",
        "days": "Trip length",
        "recommend": "Generate itinerary",
        "trip_list": "My Travel Checklist",
        "basic": "Trip Details (Optional)",
        "start": "Start date",
        "end": "End date",
        "adults": "Adults",
        "children": "Children",
        "rooms": "Room preferences (multiple)",
        "other_room": "Other room needs",
        "save_basic": "Save trip details",
        "save_tasks": "Save checklist",
        "add_task": "Add a travel task",
        "task_name": "Task name",
        "task_details": "Details (optional)",
        "add": "Add task",
        "all_tasks": "Total",
        "done": "Completed",
        "remaining": "Remaining",
        "ask": "Ask a question",
        "send": "Send",
        "remaining_quota": "Free questions remaining today",
        "quota_warning": "Friendly reminder: your free question limit is nearly reached.",
        "quota_end": "Your free questions for today have been used. Please come back tomorrow.",
        "font": "Text size",
        "contrast": "High contrast",
        "normal": "Normal",
        "large": "Large",
        "xlarge": "Extra large",
        "footer": "UX improvement prototype | Not an actual modification of the official Hualien website",
        "no_result": "No matching attractions. Try another keyword or category."
    }
}

# -----------------------------
# 預設待辦資料
# -----------------------------
DEFAULT_DATA = {
    "hualien_trip_checklist": {
        "title": "花蓮旅行待辦事項清單",
        "updated_at": "2026-10-30",
        "trip_info": {
            "start_date": "", "end_date": "", "adults": 0, "children": 0,
            "room_needs": [], "room_other": ""
        },
        "categories": [
            {
                "id": "pre_trip_planning",
                "category_name": "一、行前 14 天～1 個月（預訂與規劃）",
                "items": [
                    {"id": "p001", "task": "交通車票／機票預訂", "details": "預訂台鐵或確認航班；如需租車／機車，請提早預約。", "completed": False},
                    {"id": "p002", "task": "住宿安排", "details": "依行程動線分區入住，確認停車位及住宿備品。", "completed": False},
                    {"id": "p003", "task": "景點與活動預約", "details": "預約熱門體驗，出發前確認景點最新開放狀態。", "completed": False},
                    {"id": "p004", "task": "路況與氣象查詢", "details": "查詢蘇花路廊及中橫最新路況與天氣。", "completed": False}
                ]
            },
            {
                "id": "packing_and_confirmation",
                "category_name": "二、行前 3 天（打包與確認）",
                "items": [
                    {"id": "k001", "task": "證件與票券", "details": "準備身分證、健保卡、駕照及足夠現金。", "completed": False},
                    {"id": "k002", "task": "衣物與防曬", "details": "準備透氣衣物、防風外套、好走的鞋及玩水用品。", "completed": False},
                    {"id": "k003", "task": "3C 與隨身用品", "details": "攜帶手機、行動電源、充電線、防蚊液、防曬乳及常備藥品。", "completed": False}
                ]
            },
            {
                "id": "on_arrival",
                "category_name": "三、抵達花蓮後（落地檢核）",
                "items": [
                    {"id": "a001", "task": "交通與導航設定", "details": "檢查車輛油量／電量，建議下載離線地圖。", "completed": False},
                    {"id": "a002", "task": "行程踩點順序檢查", "details": "依北、中、南花蓮分區順遊，避免折返。", "completed": False}
                ]
            }
        ]
    }
}

ATTRACTIONS = [
    {"name": "七星潭", "region": "北區", "kind": "海岸景觀", "desc": "欣賞海灣、礫石灘與太平洋景色。"},
    {"name": "太魯閣周邊", "region": "北區", "kind": "自然景觀", "desc": "出發前請確認園區及道路最新開放資訊。"},
    {"name": "松園別館", "region": "中區", "kind": "文化體驗", "desc": "感受歷史建築與林蔭環境。"},
    {"name": "東大門夜市", "region": "中區", "kind": "親子休閒", "desc": "品嚐花蓮在地小吃與夜市美食。"},
    {"name": "鯉魚潭", "region": "中區", "kind": "自然景觀", "desc": "湖畔散步、騎乘自行車與親水活動。"},
    {"name": "雲山水", "region": "中區", "kind": "自然景觀", "desc": "欣賞湖泊、落羽松與田園景致。"},
    {"name": "石梯坪", "region": "南區", "kind": "海岸景觀", "desc": "欣賞海蝕地形與海岸景觀。"},
    {"name": "瑞穗牧場", "region": "南區", "kind": "親子休閒", "desc": "適合親子休閒與牧場體驗。"},
    {"name": "北回歸線標誌公園", "region": "南區", "kind": "文化體驗", "desc": "認識花蓮南區地理與地方特色。"}
]

# -----------------------------
# 資料讀寫
# -----------------------------
def save_data(data):
    with TODO_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_data():
    if not TODO_FILE.exists():
        save_data(DEFAULT_DATA)
        return json.loads(json.dumps(DEFAULT_DATA, ensure_ascii=False))
    try:
        with TODO_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        checklist = data["hualien_trip_checklist"]
        checklist.setdefault("trip_info", DEFAULT_DATA["hualien_trip_checklist"]["trip_info"].copy())
        for key, value in DEFAULT_DATA["hualien_trip_checklist"]["trip_info"].items():
            checklist["trip_info"].setdefault(key, value)
        if not isinstance(checklist.get("categories"), list):
            raise ValueError("categories 必須是清單")
        return data
    except (json.JSONDecodeError, KeyError, ValueError, TypeError) as exc:
        st.error(f"待辦 JSON 格式錯誤：{exc}")
        st.stop()


def all_items(data):
    return [item for cat in data["hualien_trip_checklist"]["categories"] for item in cat["items"]]


def add_task(category_id, task, details):
    data = load_data()
    cats = data["hualien_trip_checklist"]["categories"]
    used = {item["id"] for item in all_items(data)}
    n = 1
    while f"custom{n:03d}" in used:
        n += 1
    for cat in cats:
        if cat["id"] == category_id:
            cat["items"].append({
                "id": f"custom{n:03d}", "task": task.strip(),
                "details": details.strip(), "completed": False
            })
            save_data(data)
            return True
    return False


# -----------------------------
# Session 狀態：語言、客服額度、日期重置
# -----------------------------
if "language" not in st.session_state:
    st.session_state.language = "繁體中文"
if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0
if "quota_date" not in st.session_state:
    st.session_state.quota_date = date.today().isoformat()
if "font_scale" not in st.session_state:
    st.session_state.font_scale = "一般"
if "high_contrast" not in st.session_state:
    st.session_state.high_contrast = False

today = date.today().isoformat()
if st.session_state.quota_date != today:
    st.session_state.chat_count = 0
    st.session_state.quota_date = today

# -----------------------------
# 頂部導覽：語系快速切換 + 無障礙入口
# -----------------------------
top1, top2, top3 = st.columns([5, 1.4, 1.8])
with top1:
    st.markdown("## 🌊 花蓮旅遊網")
with top2:
    st.session_state.language = st.selectbox(
        "Language / 語言",
        ["繁體中文", "English"],
        index=["繁體中文", "English"].index(st.session_state.language),
        label_visibility="collapsed"
    )
with top3:
    with st.popover("♿ 無障礙設定"):
        st.session_state.font_scale = st.radio(
            "文字大小",
            ["一般", "放大", "特大"],
            index=["一般", "放大", "特大"].index(st.session_state.font_scale)
        )
        st.session_state.high_contrast = st.toggle(
            "高對比模式", value=st.session_state.high_contrast
        )

lang = TEXT[st.session_state.language]
font_css = {"一般": "1rem", "放大": "1.15rem", "特大": "1.3rem"}[st.session_state.font_scale]
if st.session_state.high_contrast:
    st.markdown(
        f"""<style>
        html, body, [data-testid="stAppViewContainer"] {{
            font-size: {font_css} !important;
            background-color: #000000 !important;
            color: #ffffff !important;
        }}
        [data-testid="stMarkdownContainer"], p, label, span, h1, h2, h3 {{
            color: #ffffff !important;
        }}
        [data-testid="stHeader"] {{background: #000000 !important;}}
        </style>""",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"<style>html, body, [data-testid='stAppViewContainer'] {{font-size:{font_css};}}</style>",
        unsafe_allow_html=True
    )

st.caption(lang["nav"])
st.divider()

# -----------------------------
# 精簡 Hero：控制首頁首屏高度
# -----------------------------
hero_left, hero_right = st.columns([1.25, 1])
with hero_left:
    st.title(lang["hero_title"])
    st.write(lang["hero_sub"])
    search_text = st.text_input(
        lang["search"],
        placeholder="例如：七星潭、壽豐、親子、海岸" if st.session_state.language == "繁體中文" else "e.g. Qixingtan, Shoufeng, family"
    )
with hero_right:
    st.image(
        "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1000",
        caption="花蓮山海風景｜首頁主視覺示意",
        use_container_width=True
    )

# -----------------------------
# 熱門服務：置於首屏下方
# -----------------------------
st.subheader(lang["popular"])
# 依月份切換季節活動內容（示範資料，正式上線需串接官方公告）
month = date.today().month
if month in (3, 4, 5):
    current_season = "春季"
    seasonal_activities = [
        ("賞螢生態體驗", "春季限定", "依生態環境及場域公告開放，建議事先確認場次與預約方式。"),
        ("春日花海與農村慢遊", "花況限定", "依花況及農事時程安排，出發前確認活動日期。")
    ]
elif month in (6, 7, 8):
    current_season = "夏季"
    seasonal_activities = [
        ("賞鯨與海洋體驗", "夏季熱門", "受海象及天候影響，請向業者確認出航與預約資訊。"),
        ("溪谷親水活動", "夏季限定", "留意天氣、溪流水位及安全公告，勿前往公告禁止區域。")
    ]
elif month in (9, 10, 11):
    current_season = "秋季"
    seasonal_activities = [
        ("縱谷稻田與農村慢遊", "秋季風景", "依作物生長及收成時程欣賞田園景觀。"),
        ("部落文化與地方體驗", "地方活動", "依主辦單位公告確認活動日期及報名方式。")
    ]
else:
    current_season = "冬季"
    seasonal_activities = [
        ("溫泉暖冬之旅", "冬季限定", "可規劃瑞穗、安通等溫泉區，請先確認營業及預約資訊。"),
        ("冬季山海景觀慢遊", "四季皆宜", "依天候與道路狀況安排，出發前確認交通及景點開放資訊。")
    ]

if "seasonal_notice_read" not in st.session_state:
    st.session_state.seasonal_notice_read = False

svc1, svc2, svc3, svc4 = st.columns(4)
with svc1:
    st.markdown("### 🎟️ " + lang["tickets"])
    st.write(lang["tickets_desc"])
    st.caption("展示入口：熱門體驗、票券與預約資訊")
with svc2:
    st.markdown("### 🗺️ " + lang["itinerary"])
    st.write(lang["itinerary_desc"])
    st.caption("展示入口：一日遊、二日遊與三日遊")
with svc3:
    st.markdown("### 🤖 " + lang["assistant"])
    st.write(lang["assistant_desc"])
    st.caption("展示入口：旅遊問答與額度管理")
with svc4:
    st.markdown("### 🌸 季節限定活動")
    st.write("依花蓮四季特色，探索當季限定體驗與節慶活動。")
    st.caption("春賞螢、夏海洋、秋縱谷、冬溫泉")
    with st.popover("查看當季活動"):
        st.markdown(f"**{current_season}活動推薦**")
        for activity_name, tag, description in seasonal_activities:
            st.markdown(f"**{activity_name}** · {tag}")
            st.caption(description)

# 網站內通知中心：進站即可查看，不會傳送至瀏覽器或 LINE
st.divider()
notice_col1, notice_col2 = st.columns([4, 1])
with notice_col1:
    st.subheader("🔔 當季限定活動通知")
    st.caption(f"花蓮 {current_season}活動資訊｜網站內通知")
with notice_col2:
    if not st.session_state.seasonal_notice_read:
        st.metric("未讀通知", "2 則")
    else:
        st.metric("未讀通知", "0 則")

with st.container(border=True):
    if not st.session_state.seasonal_notice_read:
        st.markdown(f"🟢 **{current_season}限定活動上架提醒**")
    else:
        st.markdown(f"**{current_season}限定活動資訊**")
    for activity_name, tag, description in seasonal_activities:
        st.markdown(f"**{activity_name}**　`{tag}`")
        st.caption(description)
    st.caption("提醒：目前為展示用通知內容，實際活動日期、名額、報名連結及是否成團，請以主辦單位最新公告為準。")
    if not st.session_state.seasonal_notice_read:
        if st.button("✓ 標示為已讀", key="mark_seasonal_read"):
            st.session_state.seasonal_notice_read = True
            st.rerun()
    else:
        if st.button("重新查看未讀提醒", key="reset_seasonal_read"):
            st.session_state.seasonal_notice_read = False
            st.rerun()

st.divider()

# -----------------------------
# 景點搜尋與分類
# -----------------------------
st.subheader("🔎 " + lang["attractions"])
filter1, filter2 = st.columns(2)
with filter1:
    region_options = [lang["all"], lang["north"], lang["central"], lang["south"]]
    region_choice = st.selectbox(lang["region"], region_options)
with filter2:
    kind_options = [lang["all"], lang["coast"], lang["nature"], lang["culture"], lang["family"]]
    kind_choice = st.selectbox(lang["kind"], kind_options)

region_map = {
    lang["north"]: "北區", lang["central"]: "中區", lang["south"]: "南區"
}
kind_map = {
    lang["coast"]: "海岸景觀", lang["nature"]: "自然景觀",
    lang["culture"]: "文化體驗", lang["family"]: "親子休閒"
}
filtered = []
for place in ATTRACTIONS:
    if region_choice != lang["all"] and place["region"] != region_map.get(region_choice):
        continue
    if kind_choice != lang["all"] and place["kind"] != kind_map.get(kind_choice):
        continue
    if search_text.strip() and search_text.strip().lower() not in (
        place["name"] + place["region"] + place["kind"] + place["desc"]
    ).lower():
        continue
    filtered.append(place)

if filtered:
    cols = st.columns(3)
    for i, place in enumerate(filtered):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"**{place['name']}**")
                st.caption(f"{place['region']}｜{place['kind']}")
                st.write(place["desc"])
else:
    st.info(lang["no_result"])

st.divider()

# -----------------------------
# 行程推薦（示範規則）
# -----------------------------
st.subheader("🧭 " + lang["itinerary"])
days = st.radio(lang["days"], [1, 2, 3], horizontal=True, format_func=lambda x: f"{x} 天")
if st.button(lang["recommend"], use_container_width=True):
    plans = {
        1: ["七星潭", "松園別館", "東大門夜市"],
        2: ["第一天：七星潭、松園別館、東大門夜市", "第二天：鯉魚潭、雲山水"],
        3: ["第一天：七星潭、松園別館、東大門夜市", "第二天：鯉魚潭、雲山水", "第三天：瑞穗牧場、石梯坪"]
    }
    st.session_state.recommended_plan = plans[days]
if "recommended_plan" in st.session_state:
    for step in st.session_state.recommended_plan:
        st.write("• " + step)
    st.caption("此為示範行程規則，實際出發前請確認交通、營業及景點開放資訊。")

st.divider()

# -----------------------------
# AI 客服：額度顯示、預警、用完提示
# -----------------------------
st.subheader("🤖 " + lang["assistant"])
st.caption(lang["assistant_desc"])
remaining = max(0, DAILY_LIMIT - st.session_state.chat_count)
st.progress(st.session_state.chat_count / DAILY_LIMIT, text=f"{lang['remaining_quota']}：{remaining}/{DAILY_LIMIT}")

if remaining == 0:
    st.error(lang["quota_end"])
elif remaining <= 3:
    st.warning(f"{lang['quota_warning']} {remaining}/{DAILY_LIMIT}")

question = st.text_input(lang["ask"], key="assistant_question")
if st.button(lang["send"], key="send_question"):
    if not question.strip():
        st.warning("請先輸入問題。")
    elif st.session_state.chat_count >= DAILY_LIMIT:
        st.error(lang["quota_end"])
    else:
        st.session_state.chat_count += 1
        # 此處為互動流程示範，尚未連接真正的生成式 AI 服務。
        st.info("朱鸝啾啾：收到你的問題！這是客服流程展示原型，目前尚未連接真正的 AI API。")
        st.rerun()

st.divider()

# -----------------------------
# 旅行待辦事項：保留既有功能
# -----------------------------
data = load_data()
checklist = data["hualien_trip_checklist"]
categories = checklist["categories"]
trip_info = checklist["trip_info"]

st.subheader("🧳 " + lang["trip_list"])
st.markdown("#### " + lang["basic"])

def parse_date(value):
    try:
        return date.fromisoformat(value) if value else None
    except (TypeError, ValueError):
        return None

with st.form("trip_info_form"):
    d1, d2 = st.columns(2)
    with d1:
        start_date = st.date_input(
            lang["start"], value=parse_date(trip_info.get("start_date")),
            min_value=date(2026, 1, 1), max_value=date(2026, 12, 31),
            format="YYYY/MM/DD"
        )
    with d2:
        end_date = st.date_input(
            lang["end"], value=parse_date(trip_info.get("end_date")),
            min_value=date(2026, 1, 1), max_value=date(2026, 12, 31),
            format="YYYY/MM/DD"
        )
    p1, p2 = st.columns(2)
    with p1:
        adults = st.slider(lang["adults"], 0, 20, int(trip_info.get("adults", 0)))
    with p2:
        children = st.slider(lang["children"], 0, 20, int(trip_info.get("children", 0)))
    rooms = st.multiselect(
        lang["rooms"], ["單人", "雙人", "其他"],
        default=[r for r in trip_info.get("room_needs", []) if r in ["單人", "雙人", "其他"]]
    )
    other_room = st.text_input(lang["other_room"], value=trip_info.get("room_other", ""))
    save_trip = st.form_submit_button(lang["save_basic"], use_container_width=True)

if save_trip:
    if start_date and end_date and end_date < start_date:
        st.error("結束日期不可早於開始日期。")
    else:
        trip_info.update({
            "start_date": start_date.isoformat() if start_date else "",
            "end_date": end_date.isoformat() if end_date else "",
            "adults": adults,
            "children": children,
            "room_needs": rooms,
            "room_other": other_room.strip()
        })
        save_data(data)
        st.success("旅遊基本資料已儲存。")
        st.rerun()

items = all_items(data)
done_count = sum(1 for item in items if item.get("completed", False))
total_count = len(items)
remaining_count = total_count - done_count

m1, m2, m3 = st.columns(3)
m1.metric(lang["all_tasks"], total_count)
m2.metric(lang["done"], done_count)
m3.metric(lang["remaining"], remaining_count)
st.progress(done_count / total_count if total_count else 0)

with st.form("checklist_form"):
    updated = {}
    for ci, category in enumerate(categories):
        st.markdown(f"##### {category['category_name']}")
        for item in category["items"]:
            updated[(ci, item["id"])] = st.checkbox(
                item["task"], value=bool(item.get("completed", False)),
                key=f"todo_{category['id']}_{item['id']}"
            )
            if item.get("details"):
                st.caption(item["details"])
    save_checklist = st.form_submit_button(lang["save_tasks"], use_container_width=True)

if save_checklist:
    for ci, category in enumerate(categories):
        for item in category["items"]:
            item["completed"] = updated[(ci, item["id"])]
    save_data(data)
    st.success("待辦事項已儲存。")
    st.rerun()

st.markdown("#### ➕ " + lang["add_task"])
category_labels = {c["category_name"]: c["id"] for c in categories}
with st.form("add_task_form", clear_on_submit=True):
    selected_label = st.selectbox("選擇分類", list(category_labels.keys()))
    task_name = st.text_input(lang["task_name"])
    task_details = st.text_area(lang["task_details"])
    add_clicked = st.form_submit_button(lang["add"], use_container_width=True)
if add_clicked:
    if not task_name.strip():
        st.warning("請輸入待辦事項名稱。")
    elif add_task(category_labels[selected_label], task_name, task_details):
        st.success("新增成功。")
        st.rerun()

with st.expander("📦 匯出旅行清單 JSON"):
    st.download_button(
        "下載 JSON 備份",
        data=json.dumps(load_data(), ensure_ascii=False, indent=2),
        file_name="hualien_trip_checklist.json",
        mime="application/json",
        use_container_width=True
    )

st.caption(lang["footer"])
