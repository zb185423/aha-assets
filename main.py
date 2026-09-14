# python3 main.py
import json
import os
from pathlib import Path

# ドメイン（定数定義）
BASE_URL = "https://your-storage.com"


def generate_questions_json(root_dir="assets"):
    questions = []

    # assetsディレクトリ以下を再帰的に走査
    for root, dirs, files in os.walk(root_dir):
        # 画像ファイルが含まれるディレクトリのみ処理対象とする
        jpg_files = [f for f in files if f.endswith(".jpg")]
        if not jpg_files:
            continue

        # ディレクトリパスの取得 (例: assets/premium/001/001 -> parts: ('premium', '001', '001'))
        rel_path = os.path.relpath(root, root_dir)
        path_parts = Path(rel_path).parts
        question_id = "_".join(path_parts)

        # ディレクトリ内の画像ファイルから bef / aft / ans を特定
        bef_file = next((f for f in jpg_files if "bef" in f), None)
        aft_file = next((f for f in jpg_files if "aft" in f), None)
        ans_file = next((f for f in jpg_files if "ans" in f), None)

        if not (bef_file and aft_file and ans_file):
            print(f"Warning: {root} に必要な画像が揃っていません。スキップします。")
            continue

        # 公開用の相対パス構造を構築
        url_prefix = f"{BASE_URL}/{root_dir}/{'/'.join(path_parts)}"

        # free / premium の判定と premium_id の取得
        is_premium = path_parts[0] == "premium"

        # 問題データの基本構造
        question_data = {
            "id": question_id,
            "title": "",
            "base_url": f"{url_prefix}/{bef_file}",
            "changed_url": f"{url_prefix}/{aft_file}",
            "answer_url": f"{url_prefix}/{ans_file}",
            "difficulty": 1,
            "is_premium": is_premium,
        }

        # premium配下の場合、premium直下のフォルダ名（パックIDなど）を付与
        if is_premium and len(path_parts) >= 2:
            question_data["premium_id"] = str(path_parts[1])

        questions.append(question_data)

    # ID順にソート
    questions.sort(key=lambda x: x["id"])
    return questions


if __name__ == "__main__":
    result = generate_questions_json()

    # JSONファイルへの書き出し
    output_path = "questions.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {output_path} ({len(result)} items)")
