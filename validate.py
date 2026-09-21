from datetime import datetime
import json
import re
from urllib.parse import urlparse


TITLE_LANGS = ("ja", "en", "zh-Hans")


def validate_item(item: dict, index: int) -> list[str]:
    errors = []

    # 1. 必須フィールドおよび型チェック
    required_keys = {
        "id": str,
        "base_url": str,
        "changed_url": str,
        "answer_url": str,
        "difficulty": int,
        "change_points_number": int,
        "is_premium": bool,
        "size": list,
        "regions": list,
        "updated_at": str,
    }

    for key, expected_type in required_keys.items():
        if key not in item:
            errors.append(f"キー '{key}' が存在しません。")
        elif not isinstance(item[key], expected_type):
            errors.append(
                f"'{key}' の型が不正です (期待: {expected_type.__name__}, 実際: {type(item[key]).__name__})"
            )

    # title は言語コードをキーにしたオブジェクト（ja / en / zh-Hans）
    if "title" not in item:
        errors.append("キー 'title' が存在しません。")
    elif not isinstance(item["title"], dict):
        errors.append(
            f"'title' の型が不正です (期待: dict, 実際: {type(item['title']).__name__})"
        )
    else:
        for lang in TITLE_LANGS:
            value = item["title"].get(lang)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"'title.{lang}' が空、または文字列ではありません。")

    if errors:
        return errors  # 構造自体が崩れている場合は基本チェックのみ返す

    # 2. URLフォーマットチェック
    for url_key in ["base_url", "changed_url", "answer_url"]:
        parsed = urlparse(item[url_key])
        if not (parsed.scheme in ("http", "https") and parsed.netloc):
            errors.append(f"'{url_key}' のURL形式が不正です: {item[url_key]}")

    # 3. size の検証 [width, height]
    size = item["size"]
    if len(size) != 2 or not isinstance(size[0], int) or not isinstance(size[1], int):
        errors.append(
            f"'size' は2つの整数の配列 [width, height] である必要があります: {size}"
        )
        width, height = 0, 0
    else:
        width, height = size[0], size[1]

    # 4. is_premium と premium_id の整合性
    if item["is_premium"]:
        if "premium_id" not in item or not isinstance(item["premium_id"], str):
            errors.append(
                "'is_premium' が true の場合、文字列の 'premium_id' が必須です。"
            )

    # 5. change_points_number と regions の件数一致
    regions = item["regions"]
    if len(regions) != item["change_points_number"]:
        errors.append(
            f"'change_points_number' ({item['change_points_number']}) と 'regions' の要素数 ({len(regions)}) が不一致です。"
        )

    # 6. regions 内の座標検証
    for r_idx, region in enumerate(regions):
        if not isinstance(region, dict):
            errors.append(f"'regions[{r_idx}]' がオブジェクトではありません。")
            continue

        for coord in ["x0", "y0", "x1", "y1"]:
            if coord not in region or not isinstance(region[coord], int):
                errors.append(f"'regions[{r_idx}].{coord}' が整数ではありません。")

        x0, y0 = region.get("x0", 0), region.get("y0", 0)
        x1, y1 = region.get("x1", 0), region.get("y1", 0)

        if x0 >= x1:
            errors.append(
                f"'regions[{r_idx}]' で x0 ({x0}) >= x1 ({x1}) となっています。"
            )
        if y0 >= y1:
            errors.append(
                f"'regions[{r_idx}]' で y0 ({y0}) >= y1 ({y1}) となっています。"
            )

        if width > 0 and height > 0:
            if not (0 <= x0 < width and 0 < x1 <= width):
                errors.append(
                    f"'regions[{r_idx}]' のX座標範囲が画像サイズ (幅: {width}) を超えています。"
                )
            if not (0 <= y0 < height and 0 < y1 <= height):
                errors.append(
                    f"'regions[{r_idx}]' のY座標範囲が画像サイズ (高さ: {height}) を超えています。"
                )

    # 7. ISO 8601 日時フォーマット検証
    try:
        datetime.fromisoformat(item["updated_at"])
    except ValueError:
        errors.append(
            f"'updated_at' が正しいISO 8601形式ではありません: {item['updated_at']}"
        )

    return errors


def validate_json_data(json_data: list) -> bool:
    if not isinstance(json_data, list):
        print("エラー: ルート要素がリストではありません。")
        return False

    all_valid = True
    for idx, item in enumerate(json_data):
        item_id = item.get("id", f"INDEX_{idx}")
        errors = validate_item(item, idx)
        if errors:
            all_valid = False
            print(f"❌ [ID: {item_id}] 検証エラー:")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"✅ [ID: {item_id}] 正常")

    return all_valid


# 実行例（ファイル読み込み時の場合）
if __name__ == "__main__":
    file_path = "questions.json"

    # ファイルから検証を行う場合
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        is_success = validate_json_data(data)
        if is_success:
            print("\nすべてのデータ検証が成功しました！")
        else:
            print("\n一部のデータに不整合があります。")
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
