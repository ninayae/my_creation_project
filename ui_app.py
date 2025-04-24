import streamlit as st
import yaml
import os
import ast

DATA_DIR = "data"
CATEGORIES = {
    "キャラクター設定": "characters",
    "世界設定": "world",
    "マップデータ": "maps",
    "建物": "buildings",
    "人間関係": "relations",
    "情勢": "situations",
    "物価": "economy",
    "あらすじ": "synopsis",
    "投稿内容": "narou_posts",
    "今後やりたいこと": "future_plans"
}

# ディレクトリ作成
for folder in CATEGORIES.values():
    path = os.path.join(DATA_DIR, folder)
    os.makedirs(path, exist_ok=True)

def load_yaml(category_folder, filename):
    with open(os.path.join(DATA_DIR, category_folder, filename), 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_yaml(category_folder, filename, data):
    with open(os.path.join(DATA_DIR, category_folder, filename), 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

def list_files(category_folder):
    path = os.path.join(DATA_DIR, category_folder)
    return [f for f in os.listdir(path) if f.endswith(".yml") or f.endswith(".yaml")]

def convert_to_dict(input_str):
    try:
        result = ast.literal_eval(input_str)
        if isinstance(result, dict):
            return result
        else:
            raise ValueError("入力は辞書形式でなければなりません。")
    except Exception as e:
        raise ValueError(f"無効な入力です: {e}")

# Streamlit UI
st.set_page_config(page_title="世界観データ管理", layout="wide")
st.title("異世界設定データ管理システム")

# カテゴリ選択
selected_category = st.sidebar.selectbox("カテゴリを選択", list(CATEGORIES.keys()))
category_folder = CATEGORIES[selected_category]

st.header(f"📁 {selected_category}")

files = list_files(category_folder)
selected_file = st.selectbox(f"{selected_category} ファイルを選択", files)

if selected_file:
    data = load_yaml(category_folder, selected_file)
    st.subheader("データ内容")
    st.json(data)

    if st.checkbox("編集モード"):
        text_data = st.text_area("YAML形式で編集", value=yaml.dump(data, allow_unicode=True))
        if st.button("保存"):
            try:
                parsed_data = yaml.safe_load(text_data)
                save_yaml(category_folder, selected_file, parsed_data)
                st.success("保存しました！")
            except Exception as e:
                st.error(f"保存中にエラーが発生しました: {str(e)}")

# 新規ファイル作成
new_file_name = st.sidebar.text_input("ファイル名（例：new_file）")

if new_file_name:
    # 拡張子がなければ自動的に付ける
    if not new_file_name.endswith(('.yml', '.yaml')):
        new_file_name += '.yml'
    
    # ファイル名が既に存在していなければ作成
    if new_file_name not in files:
        if st.sidebar.button("作成"):
            empty_data = {}
            save_yaml(category_folder, new_file_name, empty_data)
            st.sidebar.success(f"{new_file_name} を作成しました！")
    else:
        st.sidebar.warning(f"そのファイル名「{new_file_name}」はすでに存在します。")
if st.checkbox("専用フォームで編集"):

   if selected_category == "キャラクター設定":
    name = st.text_input("名前", value=data.get("name", ""))
    species = st.text_input("種族", value=data.get("species", ""))
    age = st.text_input("年齢", value=data.get("age", ""))

    st.markdown("---")
    st.subheader("身体的特徴（辞書形式）")
    physical_data = data.get("physical_attributes", {})
    new_physical_data = {}

    for i, (k, v) in enumerate(physical_data.items()):
        col1, col2 = st.columns([1, 2])
        key = col1.text_input(f"特徴キー {i+1}", value=k, key=f"phys_key_{i}")
        value = col2.text_input(f"特徴値 {i+1}", value=v, key=f"phys_val_{i}")
        if key:
            new_physical_data[key] = value

    col1, col2 = st.columns([1, 2])
    add_key = col1.text_input("追加する特徴キー", key="add_phys_key")
    add_value = col2.text_input("追加する特徴値", key="add_phys_val")
    if st.button("身体的特徴を追加"):
        if add_key:
            new_physical_data[add_key] = add_value
            st.experimental_rerun()

    st.markdown("---")
    st.subheader("性格（辞書形式）")
    personality_data = data.get("personality", {})
    new_personality_data = {}

    for i, (k, v) in enumerate(personality_data.items()):
        col1, col2 = st.columns([1, 2])
        key = col1.text_input(f"性格キー {i+1}", value=k, key=f"pers_key_{i}")
        value = col2.text_input(f"性格値 {i+1}", value=v, key=f"pers_val_{i}")
        if key:
            new_personality_data[key] = value

    col1, col2 = st.columns([1, 2])
    add_key_p = col1.text_input("追加する性格キー", key="add_pers_key")
    add_value_p = col2.text_input("追加する性格値", key="add_pers_val")
    if st.button("性格を追加"):
        if add_key_p:
            new_personality_data[add_key_p] = add_value_p
            st.experimental_rerun()

    st.markdown("---")
    if st.button("保存（フォーム）"):
        try:
            new_data = {
                "name": name,
                "species": species,
                "age": age,
                "physical_attributes": new_physical_data,
                "personality": new_personality_data
            }
            save_yaml(category_folder, selected_file, new_data)
            st.success("保存しました！")
        except Exception as e:
            st.error(f"エラー: {e}")


    elif selected_category == "あらすじ":
        title = st.text_input("タイトル", value=data.get("title", ""))
        summary = st.text_area("あらすじ内容", value=data.get("content", ""))
        if st.button("保存（フォーム）"):
            new_data = {"title": title, "content": summary}
            save_yaml(category_folder, selected_file, new_data)
            st.success("保存しました！")

    elif selected_category == "今後やりたいこと":
        ideas = st.text_area("やりたいこと（箇条書きOK）", value="\n".join(data.get("plans", [])))
        if st.button("保存（フォーム）"):
            new_data = {"plans": ideas.strip().splitlines()}
            save_yaml(category_folder, selected_file, new_data)
            st.success("保存しました！")

    elif selected_category == "投稿内容":
        episode_title = st.text_input("エピソードタイトル", value=data.get("episode_title", ""))
        posted_date = st.text_input("投稿日（例：2025-04-23）", value=data.get("posted_date", ""))
        content = st.text_area("投稿内容", value=data.get("content", ""))
        if st.button("保存（フォーム）"):
            new_data = {
                "episode_title": episode_title,
                "posted_date": posted_date,
                "content": content
            }
            save_yaml(category_folder, selected_file, new_data)
            st.success("保存しました！")

    # 必要なら他のカテゴリ（マップ、世界設定など）もここに追加

