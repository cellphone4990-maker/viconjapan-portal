import os
import urllib.request
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import streamlit.components.v1 as components

# ==========================================
# 日本語フォントの自動ダウンロード＆設定
# ==========================================
FONT_URL = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/Japanese/NotoSansCJKjp-Regular.otf"
FONT_NAME = "NotoSansCJKjp-Regular.otf"

if not os.path.exists(FONT_NAME):
    # User-Agentを指定してHTTP 403 Forbiddenなどのエラーを回避
    req = urllib.request.Request(
        FONT_URL, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req) as response, open(FONT_NAME, 'wb') as out_file:
        out_file.write(response.read())

fm.fontManager.addfont(FONT_NAME)
plt.rcParams['font.family'] = 'Noto Sans CJK JP'

st.set_page_config(page_title="トラクター・作業機 総合適合判定システム", layout="wide")

# ==========================================
# 0. プリセットデータ定義 & セッション状態の初期化
# ==========================================

if "preset_tractors" not in st.session_state:
    st.session_state.preset_tractors = {
        "NH T2.800": {
            "name": "NH T2.800", "weight": 3450, "front_weight": 0, "wheelbase": 2250, 
            "f_dist": 800, "r_pin": 1000, "height": 2615, 
            "width": 1930, "f_area": 775, "r_area": 1150
        },
        "NH T4.75": {
            "name": "NH T4.75", "weight": 3030, "front_weight": 0, "wheelbase": 2130, 
            "f_dist": 800, "r_pin": 1000, "height": 2480, 
            "width": 1920, "f_area": 775, "r_area": 1150
        },
        "NH T5.110": {
            "name": "NH T5.110", "weight": 3970, "front_weight": 0, "wheelbase": 2540, 
            "f_dist": 900, "r_pin": 1000, "height": 2500, 
            "width": 2160, "f_area": 1000, "r_area": 1500
        }
    }

if "preset_implements" not in st.session_state:
    st.session_state.preset_implements = {
        "Gaspardo SR1000-12ST": {
            "name": "Gaspardo SR1000-12ST", "dry_weight": 650, "total_weight": 1650, 
            "pin_dist": 700, "add_len": 1520, "width": 2370, "height": 2470
        },
        "Vicon iXter A10 HOSA12": {
            "name": "Vicon iXter A10 HOSA12", "dry_weight": 889, "total_weight": 1889, 
            "pin_dist": 700, "add_len": 1360, "width": 2350, "height": 2560
        },
        "Vicon iXter B10 HC18": {
            "name": "Vicon iXter B10 HC18", "dry_weight": 1383, "total_weight": 2383, 
            "pin_dist": 800, "add_len": 1450, "width": 2500, "height": 3300
        }
    }

if "preset_trucks" not in st.session_state:
    st.session_state.preset_trucks = {
        "トラック1": {"name": "トラック1", "payload": 2000, "bed_h": 750, "bed_l": 3100, "bed_w": 1600},
        "トラック2": {"name": "トラック2", "payload": 3500, "bed_h": 850, "bed_l": 4300, "bed_w": 1900},
        "トラック3": {"name": "トラック3", "payload": 7000, "bed_h": 950, "bed_l": 6000, "bed_w": 2350}
    }

# 初回起動時のフォーム数値初期化
if "first_init" not in st.session_state:
    st.session_state.first_init = True
    
    t_init = st.session_state.preset_tractors["NH T2.800"]
    i_init = st.session_state.preset_implements["Gaspardo SR1000-12ST"]
    k_init = st.session_state.preset_trucks["トラック1"]
    
    st.session_state.v_t_name = t_init["name"]
    st.session_state.v_tractor_weight = t_init["weight"]
    st.session_state.v_front_weight = t_init["front_weight"]
    st.session_state.v_wheelbase = t_init["wheelbase"]
    st.session_state.v_front_to_weight = t_init["f_dist"]
    st.session_state.v_rear_to_pin = t_init["r_pin"]
    st.session_state.v_t_body_height = t_init["height"]
    st.session_state.v_t_body_width = t_init.get("width", 1930)
    st.session_state.v_f_area = t_init.get("f_area", 775)
    st.session_state.v_r_area = t_init.get("r_area", 1150)
    
    st.session_state.v_i_name = i_init["name"]
    st.session_state.v_implement_dry_weight = i_init["dry_weight"]
    st.session_state.v_implement_total_weight = i_init["total_weight"]
    st.session_state.v_pin_to_implement = i_init["pin_dist"]
    st.session_state.v_implement_len = i_init["add_len"]
    st.session_state.v_max_width = i_init["width"]
    st.session_state.v_implement_height = i_init.get("height", 2470)
    
    st.session_state.v_k_name = k_init["name"]
    st.session_state.v_max_payload = k_init["payload"]
    st.session_state.v_bed_height = k_init["bed_h"]
    st.session_state.v_bed_length = k_init["bed_l"]
    st.session_state.v_bed_width = k_init["bed_w"]

# 個別の読み込み関数
def load_tractor_preset():
    slot = st.session_state.sel_t_slot
    if slot in st.session_state.preset_tractors:
        t_data = st.session_state.preset_tractors[slot]
        st.session_state.v_t_name = t_data["name"]
        st.session_state.v_tractor_weight = t_data["weight"]
        st.session_state.v_front_weight = t_data["front_weight"]
        st.session_state.v_wheelbase = t_data["wheelbase"]
        st.session_state.v_front_to_weight = t_data["f_dist"]
        st.session_state.v_rear_to_pin = t_data["r_pin"]
        st.session_state.v_t_body_height = t_data["height"]
        st.session_state.v_t_body_width = t_data.get("width", 1900)
        st.session_state.v_f_area = t_data.get("f_area", 775)
        st.session_state.v_r_area = t_data.get("r_area", 1150)

def load_implement_preset():
    slot = st.session_state.sel_i_slot
    if slot in st.session_state.preset_implements:
        i_data = st.session_state.preset_implements[slot]
        st.session_state.v_i_name = i_data["name"]
        st.session_state.v_implement_dry_weight = i_data.get("dry_weight", 650)
        st.session_state.v_implement_total_weight = i_data.get("total_weight", 1650)
        st.session_state.v_pin_to_implement = i_data["pin_dist"]
        st.session_state.v_implement_len = i_data["add_len"]
        st.session_state.v_max_width = i_data["width"]
        st.session_state.v_implement_height = i_data.get("height", 2470)

def load_truck_preset():
    slot = st.session_state.sel_k_slot
    if slot in st.session_state.preset_trucks:
        k_data = st.session_state.preset_trucks[slot]
        st.session_state.v_k_name = k_data["name"]
        st.session_state.v_max_payload = k_data["payload"]
        st.session_state.v_bed_height = k_data["bed_h"]
        st.session_state.v_bed_length = k_data["bed_l"]
        st.session_state.v_bed_width = k_data["bed_w"]

# 個別の保存関数
def save_tractor_preset():
    slot = st.session_state.sel_t_slot
    if slot in st.session_state.preset_tractors:
        st.session_state.preset_tractors[slot] = {
            "name": slot,
            "weight": st.session_state.v_tractor_weight,
            "front_weight": st.session_state.v_front_weight,
            "wheelbase": st.session_state.v_wheelbase,
            "f_dist": st.session_state.v_front_to_weight,
            "r_pin": st.session_state.v_rear_to_pin,
            "height": st.session_state.v_t_body_height,
            "width": st.session_state.v_t_body_width,
            "f_area": st.session_state.v_f_area,
            "r_area": st.session_state.v_r_area
        }
        st.toast(f"✅ {slot} の設定を保存しました")

def save_implement_preset():
    slot = st.session_state.sel_i_slot
    if slot in st.session_state.preset_implements:
        st.session_state.preset_implements[slot] = {
            "name": slot,
            "dry_weight": st.session_state.v_implement_dry_weight,
            "total_weight": st.session_state.v_implement_total_weight,
            "pin_dist": st.session_state.v_pin_to_implement,
            "add_len": st.session_state.v_implement_len,
            "width": st.session_state.v_max_width,
            "height": st.session_state.v_implement_height
        }
        st.toast(f"✅ {slot} の設定を保存しました")

def save_truck_preset():
    slot = st.session_state.sel_k_slot
    if slot in st.session_state.preset_trucks:
        st.session_state.preset_trucks[slot] = {
            "name": slot,
            "payload": st.session_state.v_max_payload,
            "bed_h": st.session_state.v_bed_height,
            "bed_l": st.session_state.v_bed_length,
            "bed_w": st.session_state.v_bed_width
        }
        st.toast(f"✅ {slot} の設定を保存しました")

# ==========================================
# 共通計算ロジック
# ==========================================
tractor_weight = st.session_state.v_tractor_weight
front_weight = st.session_state.v_front_weight
wheelbase = st.session_state.v_wheelbase
front_to_weight = st.session_state.v_front_to_weight
rear_to_pin = st.session_state.v_rear_to_pin

implement_dry_weight = st.session_state.v_implement_dry_weight
implement_total_weight = st.session_state.v_implement_total_weight

pin_to_implement = st.session_state.v_pin_to_implement
implement_len = st.session_state.v_implement_len
t_body_height = st.session_state.v_t_body_height
t_body_width = st.session_state.v_t_body_width
max_width = st.session_state.v_max_width
implement_height = st.session_state.v_implement_height

wb_m = wheelbase / 1000.0
f_w_dist_m = front_to_weight / 1000.0
r_imp_dist_m = (rear_to_pin + pin_to_implement) / 1000.0

t_front = tractor_weight * 0.4
t_rear = tractor_weight * 0.6

if wb_m > 0:
    f_front = front_weight * (1.0 + f_w_dist_m / wb_m)
    f_rear = - front_weight * (f_w_dist_m / wb_m)
    i_rear = implement_total_weight * (1.0 + r_imp_dist_m / wb_m)
    i_front = - implement_total_weight * (r_imp_dist_m / wb_m)
else:
    f_front, f_rear, i_front, i_rear = 0, 0, 0, 0

front_load = t_front + f_front + i_front
rear_load = t_rear + f_rear + i_rear

total_weight = tractor_weight + implement_total_weight + front_weight
total_dry_weight = tractor_weight + implement_dry_weight + front_weight
t_total_length = front_to_weight + wheelbase + rear_to_pin

# 接地圧判定
front_tire_area = st.session_state.v_f_area
rear_tire_area = st.session_state.v_r_area
allowable_pressure = st.session_state.get("v_allowable_pressure", 0.8)

front_pressure = (front_load / 2) / front_tire_area if front_tire_area > 0 else 0
rear_pressure = (rear_load / 2) / rear_tire_area if rear_tire_area > 0 else 0
max_pressure = max(front_pressure, rear_pressure)
pressure_ok = max_pressure <= allowable_pressure

# トラック積載判定
bed_height = st.session_state.v_bed_height
bed_length = st.session_state.v_bed_length
bed_width = st.session_state.v_bed_width
max_payload = st.session_state.v_max_payload

overall_length = t_total_length + implement_len
overall_width = max(t_body_width, max_width)
overall_height = max(t_body_height, implement_height)
total_height_on_truck = bed_height + overall_height

weight_ok = total_dry_weight <= max_payload
width_ok = overall_width <= bed_width and overall_width <= 2500
height_ok = total_height_on_truck <= 3800
length_ok = overall_length <= bed_length
overhang_ratio = (overall_length - bed_length) / bed_length if overall_length > bed_length else 0
length_warning = overhang_ratio > 0 and overhang_ratio <= 0.1

# ==========================================
# タイトル ＆ 印刷ダイアログ呼出エリア
# ==========================================
t_col1, t_col2 = st.columns([3, 1])

with t_col1:
    st.title("🚜 トラクター・作業機 総合適合判定システム")

with t_col2:
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    if st.button("🖨️ 画面を印刷 / PDF保存", use_container_width=True):
        components.html("<script>window.parent.print();</script>", height=0, width=0)

st.markdown("---")

# ==========================================
# 選択肢エリア
# ==========================================
p_col1, p_col2, p_col3 = st.columns(3)

with p_col1:
    t_options = list(st.session_state.preset_tractors.keys())
    st.selectbox("トラクター選択", options=t_options, index=0, key="sel_t_slot", on_change=load_tractor_preset)
    st.button("トラクター設定を保存", key="btn_save_t", on_click=save_tractor_preset, use_container_width=True)

with p_col2:
    i_options = list(st.session_state.preset_implements.keys())
    st.selectbox("作業機選択", options=i_options, index=0, key="sel_i_slot", on_change=load_implement_preset)
    st.button("作業機設定を保存", key="btn_save_i", on_click=save_implement_preset, use_container_width=True)

with p_col3:
    k_options = list(st.session_state.preset_trucks.keys())
    st.selectbox("トラック選択", options=k_options, index=0, key="sel_k_slot", on_change=load_truck_preset)
    st.button("トラック設定を保存", key="btn_save_k", on_click=save_truck_preset, use_container_width=True)

st.markdown("---")

# ==========================================
# セクション 1: 車体重量バランス＆各部寸法
# ==========================================
col_left, col_right = st.columns([1.4, 1])

# ── 左列：イラスト ──
with col_left:
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    fig1.patch.set_facecolor('#ffffff')
    ax1.set_facecolor('#f8f9fa')
    ax1.set_aspect('equal')
    
    ax1.axhline(0.2, color='#333333', lw=2.5, zorder=1)
    
    ax1.text(0.6, 1.8, f"車両合計重量: {total_weight:.0f} kg", fontsize=10, fontweight='bold', color='#333333',
             bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec="#cccccc", lw=1))
    
    ax1.add_patch(patches.FancyBboxPatch((0.77, 0.6), 0.3, 0.35, 
                                         boxstyle="round,pad=0,rounding_size=0.05",
                                         color='#6c757d', ec='black', lw=1.2, zorder=3))
    
    ax1.add_patch(patches.Rectangle((1.1, 0.6), 0.9, 0.6, color='#007bff', ec='black', lw=1.2))
    ax1.add_patch(patches.Rectangle((2.0, 0.6), 0.8, 1.1, color='#007bff', ec='black', lw=1.2, alpha=0.9))
    
    ax1.add_patch(patches.FancyBboxPatch((3.1, 0.6), 0.6, 0.9, 
                                         boxstyle="round,pad=0,rounding_size=0.05",
                                         color='#fd7e14', ec='black', lw=1.2, zorder=3))
    
    ax1.plot(3.1, 0.75, marker='o', markersize=6, color='red', zorder=5)
    
    ax1.add_patch(patches.Circle((1.3, 0.5), 0.3, color='black', ec='black', zorder=2))
    ax1.add_patch(patches.Circle((1.3, 0.5), 0.18, color='white', zorder=3))
    ax1.add_patch(patches.Circle((2.6, 0.65), 0.45, color='black', ec='black', zorder=2))
    ax1.add_patch(patches.Circle((2.6, 0.65), 0.28, color='white', zorder=3))
    
    f_color = '#007bff' if front_load > 0 else '#dc3545'
    ax1.text(1.3, 0.5, f"{front_load:.0f}\nkg", ha='center', va='center', fontsize=7.5, fontweight='bold', color=f_color, zorder=4)
    ax1.text(2.6, 0.65, f"{rear_load:.0f}\nkg", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#dc3545', zorder=4)
    
    guide_lines = [
        (0.92, -0.05, 0.6),
        (1.3,  -0.05, 0.5),
        (2.6,  -0.05, 0.65),
        (3.1,  -0.05, 0.75),
        (3.4,  -0.05, 0.6)
    ]
    for x, y_start, y_end in guide_lines:
        ax1.plot([x, x], [y_start, y_end], color='#888888', ls='--', lw=0.9, zorder=1)

    ax1.annotate('', xy=(1.3, -0.05), xytext=(2.6, -0.05), arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.0))
    ax1.text(1.95, -0.22, f"{wheelbase}mm", ha='center', fontsize=8, fontweight='bold')
    
    ax1.annotate('', xy=(0.92, -0.05), xytext=(1.3, -0.05), arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.0))
    ax1.text(1.11, -0.22, f"{front_to_weight}mm", ha='center', fontsize=8, fontweight='bold')
    
    ax1.annotate('', xy=(2.6, -0.05), xytext=(3.1, -0.05), arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.0))
    ax1.text(2.85, -0.22, f"{rear_to_pin}mm", ha='center', fontsize=8, fontweight='bold')
    
    ax1.annotate('', xy=(3.1, -0.05), xytext=(3.4, -0.05), arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.0))
    ax1.text(3.25, -0.22, f"{pin_to_implement}mm", ha='center', fontsize=8, fontweight='bold')
    
    ax1.set_xlim(0.5, 4.1)
    ax1.set_ylim(-0.35, 1.95)
    ax1.axis('off')
    
    st.pyplot(fig1)

# ── 右列：入力フォーム ──
with col_right:
    col_t_in, col_i_in = st.columns(2)
    
    with col_t_in:
        st.caption("【トラクター寸法・重量】")
        st.number_input("本体重量 (kg)", step=100, key="v_tractor_weight")
        st.number_input("フロントウェイト重量 (kg)", step=50, key="v_front_weight")
        st.number_input("ホイールベース (mm)", step=50, key="v_wheelbase")
        st.number_input("フロント軸〜ウェイト先端 (mm)", step=50, key="v_front_to_weight")
        st.number_input("リア軸〜作業機ピン (mm)", step=50, key="v_rear_to_pin")
        st.number_input("トラクター全高 (mm)", step=50, key="v_t_body_height")
        st.number_input("トラクター全幅 (mm)", step=50, key="v_t_body_width")

    with col_i_in:
        st.caption("【作業機寸法・重量】")
        st.number_input("作業機乾燥重量 (kg)", step=50, key="v_implement_dry_weight")
        st.number_input("作業機総重量 (kg)", step=50, key="v_implement_total_weight")
        st.number_input("ピン〜作業機重心 (mm)", step=50, key="v_pin_to_implement")
        st.number_input("作業機単体長さ (mm)", step=50, key="v_implement_len")
        st.number_input("作業機全幅 (mm)", step=50, key="v_max_width")
        st.number_input("作業機全高 (mm)", step=50, key="v_implement_height")

st.markdown("---")

# ==========================================
# セクション 2: 接地圧判定
# ==========================================
col3_left, col3_right = st.columns([1.4, 1])

with col3_right:
    st.caption("【タイヤ接地圧設定】")
    st.number_input("前輪1本の接地面積 (cm²)", step=10, key="v_f_area")
    st.number_input("後輪1本の接地面積 (cm²)", step=10, key="v_r_area")
    st.number_input("許容接地圧 (kg/cm²)", value=0.8, step=0.1, key="v_allowable_pressure")

with col3_left:
    fig3, ax3 = plt.subplots(figsize=(7, 3.2))
    fig3.patch.set_facecolor('#ffffff')
    ax3.set_facecolor('#f8f9fa')
    ax3.set_aspect('equal')
    
    f_color = '#28a745' if front_pressure <= allowable_pressure else '#dc3545'
    r_color = '#28a745' if rear_pressure <= allowable_pressure else '#dc3545'
    
    ax3.add_patch(patches.Rectangle((0.8, 0.3), 2.6, 1.8, color='none', ec='#6c757d', lw=1.5, ls='--'))
    box_style = "round,pad=0,rounding_size=0.1"
    
    ax3.add_patch(patches.FancyBboxPatch((0.5, 1.5), 0.6, 0.6, boxstyle=box_style, color=f_color, alpha=0.85, ec='black', lw=1.5))
    ax3.text(0.8, 1.8, f"前輪\n{front_pressure:.2f}", ha='center', va='center', color='white', fontweight='bold', fontsize=8)
    
    ax3.add_patch(patches.FancyBboxPatch((0.5, 0.3), 0.6, 0.6, boxstyle=box_style, color=f_color, alpha=0.85, ec='black', lw=1.5))
    ax3.text(0.8, 0.6, f"前輪\n{front_pressure:.2f}", ha='center', va='center', color='white', fontweight='bold', fontsize=8)
    
    ax3.add_patch(patches.FancyBboxPatch((3.1, 1.5), 0.6, 0.6, boxstyle=box_style, color=r_color, alpha=0.85, ec='black', lw=1.5))
    ax3.text(3.4, 1.8, f"後輪\n{rear_pressure:.2f}", ha='center', va='center', color='white', fontweight='bold', fontsize=8)
    
    ax3.add_patch(patches.FancyBboxPatch((3.1, 0.3), 0.6, 0.6, boxstyle=box_style, color=r_color, alpha=0.85, ec='black', lw=1.5))
    ax3.text(3.4, 0.6, f"後輪\n{rear_pressure:.2f}", ha='center', va='center', color='white', fontweight='bold', fontsize=8)
    
    if pressure_ok:
        status_text = f"判定: 適合\n（基準 {allowable_pressure:.2f} kg/cm² 以下）"
        status_bg, status_color = "#d4edda", "#155724"
    else:
        status_text = f"判定: 警告\n（基準 {allowable_pressure:.2f} kg/cm² 超過）"
        status_bg, status_color = "#f8d7da", "#721c24"
    
    ax3.text(2.1, 1.2, status_text, 
             ha='center', va='center', fontsize=9, fontweight='bold', color=status_color, linespacing=1.3,
             bbox=dict(boxstyle="round,pad=0.4", fc=status_bg, ec=status_color, lw=1))
    
    ax3.set_xlim(0, 4.2)
    ax3.set_ylim(-0.1, 2.5)
    ax3.axis('off')
    
    st.pyplot(fig3)

st.markdown("---")

# ==========================================
# セクション 3: トラック積載判定
# ==========================================
col2_left, col2_right = st.columns([1.4, 1])

with col2_right:
    st.caption("【トラック積載設定】")
    st.number_input("積載車両合計重量 (乾燥重量ベース) (kg)", value=int(total_dry_weight), disabled=True)
    
    bed_height = st.number_input("トラック荷台高さ (mm)", step=50, key="v_bed_height")
    bed_length = st.number_input("トラック荷台長 (mm)", step=100, key="v_bed_length")
    bed_width = st.number_input("トラック荷台幅 (mm)", step=50, key="v_bed_width")
    max_payload = st.number_input("トラック最大積載量 (kg)", step=100, key="v_max_payload")

with col2_left:
    fig2_side, ax2s = plt.subplots(figsize=(7, 3))
    fig2_side.patch.set_facecolor('#ffffff')
    ax2s.set_facecolor('#f8f9fa')
    ax2s.set_aspect('equal')
    
    bed_h_m = bed_height / 1000
    bed_l_m = bed_length / 1000
    mach_l_m = overall_length / 1000
    mach_h_m = overall_height / 1000
    
    ax2s.axhline(0.0, color='#333333', lw=2)
    ax2s.add_patch(patches.Rectangle((0.2, 0.3), 0.8, 2.4, color='#495057', ec='black', lw=1.5))
    ax2s.add_patch(patches.FancyBboxPatch((0.28, 1.6), 0.45, 0.8, boxstyle="round,pad=0,rounding_size=0.08", color='#e0f7fa', ec='black', lw=1.2, zorder=3))
    ax2s.add_patch(patches.Rectangle((1.0, 0.3), bed_l_m, bed_h_m, color='#adb5bd', ec='black', lw=1.5, hatch='//'))
    
    r_rear1 = 1.0 + bed_l_m - 0.85
    r_rear2 = 1.0 + bed_l_m - 0.25
    ax2s.add_patch(patches.Circle((0.6, 0.3), 0.3, color='black', zorder=2))
    ax2s.add_patch(patches.Circle((0.6, 0.3), 0.15, color='white', zorder=3))
    ax2s.add_patch(patches.Circle((r_rear1, 0.3), 0.3, color='black', zorder=2))
    ax2s.add_patch(patches.Circle((r_rear1, 0.3), 0.15, color='white', zorder=3))
    ax2s.add_patch(patches.Circle((r_rear2, 0.3), 0.3, color='black', zorder=2))
    ax2s.add_patch(patches.Circle((r_rear2, 0.3), 0.15, color='white', zorder=3))

    h_color = '#28a745' if height_ok else '#dc3545'
    ax2s.add_patch(patches.Rectangle((1.0, 0.3 + bed_h_m), mach_l_m, mach_h_m, color=h_color, alpha=0.7, ec='black', lw=1.5))
    ax2s.text(1.0 + mach_l_m/2, 0.3 + bed_h_m + mach_h_m/2, f"積載物\n({total_dry_weight:.0f}kg / 全高:{total_height_on_truck}mm)", 
              ha='center', va='center', color='white', fontweight='bold', fontsize=9)

    ax2s.axhline(3.8, color='#dc3545', lw=2, ls='--')
    ax2s.text(0.2, 3.9, "法規制限: 3.8m", color='#dc3545', fontweight='bold', fontsize=8)

    ax2s.set_xlim(0, max(1.2 + bed_l_m, 1.2 + mach_l_m) + 0.5)
    ax2s.set_ylim(-0.2, 4.5)
    ax2s.axis('off')
    st.pyplot(fig2_side)

    fig2_top, ax2t = plt.subplots(figsize=(7, 2.2))
    fig2_top.patch.set_facecolor('#ffffff')
    ax2t.set_facecolor('#f8f9fa')
    ax2t.set_aspect('equal')
    
    bed_w_m = bed_width / 1000
    mach_w_m = overall_width / 1000
    
    ax2t.add_patch(patches.Rectangle((0.2, 0.2), 0.7, bed_w_m, color='#495057', ec='black', lw=1.5))
    ax2t.add_patch(patches.Rectangle((0.9, 0.2), bed_l_m, bed_w_m, color='#e9ecef', ec='black', lw=1.5, hatch='...'))
    
    w_color = '#28a745' if (length_ok or length_warning) and width_ok else '#dc3545'
    ax2t.add_patch(patches.Rectangle((0.9, 0.2 + (bed_w_m - mach_w_m)/2), mach_l_m, mach_w_m, color=w_color, alpha=0.7, ec='black', lw=1.5))
    
    ax2t.set_xlim(0, max(0.9 + bed_l_m, 0.9 + mach_l_m) + 0.5)
    ax2t.set_ylim(0, max(bed_w_m, mach_w_m) + 0.6)
    ax2t.axis('off')
    st.pyplot(fig2_top)
