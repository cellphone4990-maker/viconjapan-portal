import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit.components.v1 as components
import matplotlib.font_manager as fm
import os

# GitHubに置いたフォントファイルを直接読み込む
font_path = "NotoSansJP.ttf"

if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = fm.FontProperties(fname=font_path).get_name()

plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="トラクター・作業機 総合適合判定システム", layout="wide")

# ==============================================
# 0. プリセットデータ定義 & セッション状態の初期化
# ==============================================

if "preset_tractors" not in st.session_state:
    st.session_state.preset_tractors = {
        "1": {"name": "トラクター1", "weight": 1500, "front_weight": 150, "wheelbase": 1600, "f_dist": 600, "r_pin": 500, "height": 2000, "f_area": 200, "r_area": 400, "allow_pressure": 0.80},
        "トラクター2": {"name": "トラクター2", "weight": 2500, "front_weight": 300, "wheelbase": 2000, "f_dist": 800, "r_pin": 600, "height": 2200, "f_area": 300, "r_area": 600, "allow_pressure": 1.00},
        "トラクター3": {"name": "トラクター3", "weight": 4200, "front_weight": 500, "wheelbase": 2400, "f_dist": 950, "r_pin": 750, "height": 2500, "f_area": 450, "r_area": 900, "allow_pressure": 1.20}
    }

if "preset_implements" not in st.session_state:
    st.session_state.preset_implements = {
        "作業機1": {"name": "作業機1", "dry_weight": 300, "total_weight": 350, "cog_dist": 400, "width": 1400, "length": 1200, "height": 1000},
        "作業機2": {"name": "作業機2", "dry_weight": 600, "total_weight": 700, "cog_dist": 600, "width": 1800, "length": 1500, "height": 1200},
        "作業機3": {"name": "作業機3", "dry_weight": 1200, "total_weight": 1400, "cog_dist": 900, "width": 2300, "length": 2000, "height": 1500}
    }

if "preset_trucks" not in st.session_state:
    st.session_state.preset_trucks = {
        "トラック1": {"name": "トラック1", "capacity": 3000, "length": 4300, "width": 1900},
        "トラック2": {"name": "トラック2", "capacity": 5000, "length": 5300, "width": 2100},
        "トラック3": {"name": "トラック3", "capacity": 8000, "length": 6200, "width": 2300}
    }

# ==============================================
# ヘッダー領域
# ==============================================
col_title, col_print = st.columns([3, 1])
with col_title:
    st.title("🚜 トラクター・作業機 総合適合判定システム")

with col_print:
    st.write("")
    components.html(
        """
        <button onclick="window.parent.print()" style="
            width: 100%;
            padding: 10px;
            background-color: #1E293B;
            color: #FFFFFF;
            border: 1px solid #475569;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
        ">🖨️ 画面を印刷 / PDF保存</button>
        """,
        height=50
    )

st.divider()

# ==============================================
# 1. ドロップダウン（選択）領域
# ==============================================
col_sel1, col_sel2, col_sel3 = st.columns(3)

with col_sel1:
    selected_tr_key = st.selectbox("トラクター選択", list(st.session_state.preset_tractors.keys()))
    tr_data = st.session_state.preset_tractors[selected_tr_key]

with col_sel2:
    selected_imp_key = st.selectbox("作業機選択", list(st.session_state.preset_implements.keys()))
    imp_data = st.session_state.preset_implements[selected_imp_key]

with col_sel3:
    selected_tr_truck_key = st.selectbox("トラック選択", list(st.session_state.preset_trucks.keys()))
    truck_data = st.session_state.preset_trucks[selected_tr_truck_key]

# 保存ボタン群
col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    if st.button("トラクター設定を保存", use_container_width=True):
        st.success(f"「{selected_tr_key}」の設定を保存しました")

with col_btn2:
    if st.button("作業機設定を保存", use_container_width=True):
        st.success(f"「{selected_imp_key}」の設定を保存しました")

with col_btn3:
    if st.button("トラック設定を保存", use_container_width=True):
        st.success(f"「{selected_tr_truck_key}」の設定を保存しました")

st.divider()

# ==============================================
# 2. メイン表示・数値設定・グラフ表示領域
# ==============================================
col_left, col_right = st.columns([1.2, 1])

# --- 右側：各種数値入力フォーム ---
with col_right:
    col_r1, col_r2 = st.columns(2)
    
    with col_r1:
        st.caption("【トラクター寸法・重量】")
        t_weight = st.number_input("本体重量 (kg)", value=tr_data["weight"], step=50)
        t_front_w = st.number_input("フロントウェイト重量 (kg)", value=tr_data["front_weight"], step=10)
        t_wheelbase = st.number_input("ホイールベース (mm)", value=tr_data["wheelbase"], step=50)
        t_f_dist = st.number_input("前輪～ウェイト重心 (mm)", value=tr_data["f_dist"], step=50)
        t_r_pin = st.number_input("後輪～ヒッチピン (mm)", value=tr_data["r_pin"], step=50)
        t_height = st.number_input("全高 (mm)", value=tr_data["height"], step=50)

    with col_r2:
        st.caption("【作業機寸法・重量】")
        i_dry_w = st.number_input("作業機乾燥重量 (kg)", value=imp_data["dry_weight"], step=10)
        i_total_w = st.number_input("作業機総重量 (kg)", value=imp_data["total_weight"], step=10)
        i_cog_dist = st.number_input("ピン～作業機重心 (mm)", value=imp_data["cog_dist"], step=50)
        i_width = st.number_input("全幅 (mm)", value=imp_data["width"], step=50)
        i_length = st.number_input("全長 (mm)", value=imp_data["length"], step=50)
        i_height = st.number_input("全高 (mm)", value=imp_data["height"], step=50)

    st.divider()
    
    st.caption("【タイヤ接地圧設定】")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        f_area = st.number_input("前輪1本の接地面積 (cm²)", value=tr_data["f_area"], step=10)
        r_area = st.number_input("後輪1本の接地面積 (cm²)", value=tr_data["r_area"], step=10)
    with col_p2:
        allow_pressure = st.number_input("許容接地圧 (kg/cm²)", value=tr_data["allow_pressure"], step=0.05, format="%.2f")

    st.divider()

    st.caption("【トラック積載設定】")
    truck_cap = st.number_input("トラック最大積載量 (kg)", value=truck_data["capacity"], step=100)
    truck_len = st.number_input("荷台長 (mm)", value=truck_data["length"], step=100)
    truck_wid = st.number_input("荷台幅 (mm)", value=truck_data["width"], step=50)

# --- 計算ロジック ---
# 前後軸重の計算
# 軸力モーメント計算: 
# (前輪軸中心を原点 0 としたモーメント計算)
total_weight = t_weight + t_front_w + i_total_w
rear_axle_load = ( (t_weight * (t_wheelbase / 2)) + (i_total_w * (t_wheelbase + t_r_pin + i_cog_dist)) - (t_front_w * t_f_dist) ) / t_wheelbase
front_axle_load = total_weight - rear_axle_load

# 接地圧計算 (1輪あたりの重量 / 接地面積)
f_pressure = (front_axle_load / 2) / f_area if f_area > 0 else 0
r_pressure = (rear_axle_load / 2) / r_area if r_area > 0 else 0
max_actual_pressure = max(f_pressure, r_pressure)

# 適合判定
is_pressure_ok = max_actual_pressure <= allow_pressure
is_truck_weight_ok = total_weight <= truck_cap
is_truck_size_ok = (i_width <= truck_wid) and ((t_wheelbase + t_f_dist + t_r_pin + i_length) <= truck_len)

# --- 左側：イラスト・描画・判定カード領域 ---
with col_left:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_aspect('equal')
    ax.axis('off')

    # 背景・車両描画（簡易イメージ）
    # 車体描画
    ax.add_patch(patches.Rectangle((0.2, 0.3), 0.5, 0.3, facecolor='#1E88E5', edgecolor='black', linewidth=2))
    # 作業機描画
    ax.add_patch(patches.Rectangle((0.7, 0.35), 0.2, 0.25, facecolor='#FF8F00', edgecolor='black', linewidth=2))
    # ウェイト描画
    ax.add_patch(patches.Rectangle((0.1, 0.35), 0.1, 0.15, facecolor='#757575', edgecolor='black', linewidth=2))
    # 前輪・後輪
    ax.add_patch(patches.Circle((0.3, 0.25), 0.12, facecolor='#212121', edgecolor='black', linewidth=2))
    ax.add_patch(patches.Circle((0.65, 0.28), 0.16, facecolor='#212121', edgecolor='black', linewidth=2))

    # 接地圧テキスト表示
    f_p_text = f"{f_pressure:.2f}"
    r_p_text = f"{r_pressure:.2f}"
    
    # 前輪接地圧ボックス
    ax.text(0.3, 0.7, f"前輪接地圧\n{f_p_text} kg/cm²", fontsize=11, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#E53935' if f_pressure > allow_pressure else '#43A047', alpha=0.8, edgecolor='none'), color='white', weight='bold')
    # 後輪接地圧ボックス
    ax.text(0.65, 0.7, f"後輪接地圧\n{r_p_text} kg/cm²", fontsize=11, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#E53935' if r_pressure > allow_pressure else '#43A047', alpha=0.8, edgecolor='none'), color='white', weight='bold')

    # 中央総合判定ボックス
    status_text = "判定：適合" if is_pressure_ok else "判定：不適合"
    ax.text(0.48, 0.45, f"{status_text}\n最大 {max_actual_pressure:.2f} kg/cm²", fontsize=13, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#FFCDD2' if not is_pressure_ok else '#C8E6C9', edgecolor='#E53935' if not is_pressure_ok else '#2E7D32', linewidth=2),
            color='#B71C1C' if not is_pressure_ok else '#1B5E20', weight='bold')

    # 車両合計重量タグ
    ax.text(0.05, 0.9, f"車両合計重量: {total_weight:.0f} kg", fontsize=12, bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#B0BEC5', alpha=0.9))

    ax.set_xlim(-0.05, 1.0)
    ax.set_ylim(0.0, 1.0)
    
    st.pyplot(fig)

    # 総合適合判定サマリーカード
    st.subheader("📋 適合判定結果")
    c1, c2, c3 = st.columns(3)
    with c1:
        if is_pressure_ok:
            st.success("接地圧判定: OK")
        else:
            st.error("接地圧判定: NG (超過)")

    with c2:
        if is_truck_weight_ok:
            st.success("トラック重量判定: OK")
        else:
            st.error("トラック重量判定: NG (過積載)")

    with c3:
        if is_truck_size_ok:
            st.success("トラック寸法判定: OK")
        else:
            st.warning("トラック寸法判定: 注意")
