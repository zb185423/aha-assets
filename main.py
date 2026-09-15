import json
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

# ドメイン（定数定義）
BASE_URL = "https://zb185423.github.io/aha-assets"
JSON_PATH = "questions.json"

# JST (UTC+9) のタイムゾーン定義
JST = timezone(timedelta(hours=9))


def get_current_jst_time():
    """現在時刻をISO 8601形式（JST: +09:00）で取得"""
    return datetime.now(JST).isoformat(timespec="seconds")


def load_existing_questions():
    """既存のquestions.jsonが存在していれば読み込み、idをキーにした辞書で返す"""
    if not os.path.exists(JSON_PATH):
        return {}

    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            questions_list = (
                data.get("questions", []) if isinstance(data, dict) else data
            )
            return {q["id"]: q for q in questions_list if "id" in q}
    except Exception as e:
        print(
            f"Warning: 既存の {JSON_PATH} の読み込みに失敗しました ({e})。新規作成します。"
        )
        return {}


def generate_questions_json(root_dir="assets"):
    existing_map = load_existing_questions()
    now_str = get_current_jst_time()

    questions = []

    for root, dirs, files in os.walk(root_dir):
        jpg_files = [f for f in files if f.endswith(".jpg")]
        if not jpg_files:
            continue

        rel_path = os.path.relpath(root, root_dir)
        path_parts = Path(rel_path).parts
        question_id = "_".join(path_parts)

        bef_file = next((f for f in jpg_files if "bef" in f), None)
        aft_file = next((f for f in jpg_files if "aft" in f), None)
        ans_file = next((f for f in jpg_files if "ans" in f), None)

        if not (bef_file and aft_file and ans_file):
            print(f"Warning: {root} に必要な画像が揃っていません。スキップします。")
            continue

        url_prefix = f"{BASE_URL}/{root_dir}/{'/'.join(path_parts)}"
        is_premium = path_parts[0] == "premium"

        # 既存データがあれば元の updated_at を引き継ぐ
        if question_id in existing_map:
            updated_at = existing_map[question_id].get("updated_at", now_str)
        else:
            updated_at = now_str

        question_data = {
            "id": question_id,
            "title": "",
            "base_url": f"{url_prefix}/{bef_file}",
            "changed_url": f"{url_prefix}/{aft_file}",
            "answer_url": f"{url_prefix}/{ans_file}",
            "difficulty": 1,
            "is_premium": is_premium,
            "updated_at": updated_at,
        }

        if is_premium and len(path_parts) >= 2:
            question_data["premium_id"] = str(path_parts[1])

        questions.append(question_data)

    questions.sort(key=lambda x: x["id"])

    output_data = {"updated_at": now_str, "questions": questions}

    return output_data


if __name__ == "__main__":
    result = generate_questions_json()

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Successfully updated {JSON_PATH} ({len(result['questions'])} items)")
