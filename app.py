from flask import Flask, render_template, request, jsonify
import random
import urllib.parse
from data import SPOTS, ALL_REGIONS, ALL_CATEGORIES, REGION_ORDER, CATEGORY_EMOJI, SEASON_EMOJI

app = Flask(__name__)


def filter_spots(region, categories, season):
    """クエリパラメータに基づいてスポットを絞り込む"""
    pool = SPOTS

    if region and region != "全国":
        pool = [s for s in pool if s["region"] == region]

    if categories:
        cat_list = [c.strip() for c in categories.split(",") if c.strip()]
        if cat_list:
            pool = [s for s in pool if any(c in s["category"] for c in cat_list)]

    if season:
        pool = [s for s in pool if season in s["seasons"]]

    return pool


@app.route("/")
def index():
    return render_template(
        "index.html",
        regions=ALL_REGIONS,
        categories=ALL_CATEGORIES,
        category_emoji=CATEGORY_EMOJI,
        season_emoji=SEASON_EMOJI,
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/api/random")
def api_random():
    """ランダムに1件のスポットをJSONで返す"""
    region = request.args.get("region", "全国")
    categories = request.args.get("category", "")
    season = request.args.get("season", "")

    pool = filter_spots(region, categories, season)

    if not pool:
        return jsonify({"error": "条件に合うスポットが見つかりません。"}), 404

    spot = random.choice(pool)
    # GoogleマップURLとじゃらんURLをサーバー側で生成
    query = urllib.parse.quote(f"{spot['name']} {spot['pref']}")
    pref_name = spot["pref"].split()[0]  # 都道府県名のみ抽出
    jalan_base = "https://px.a8.net/svt/ejp?a8mat=4B1PLQ+1SCD6+14CS+67JUA&a8ejpredirect="
    jalan_search = f"https://www.jalan.net/yad/?CenS=1&keyword={pref_name}"
    jalan_url = jalan_base + urllib.parse.quote(jalan_search, safe="")

    return jsonify({
        **spot,
        "map_url": f"https://www.google.com/maps/search/?api=1&query={query}",
        "jalan_url": jalan_url,
    })


@app.route("/api/spots")
def api_spots():
    """フィルター済みの全スポットをJSONで返す（一覧用）"""
    region = request.args.get("region", "全国")
    categories = request.args.get("category", "")
    season = request.args.get("season", "")

    pool = filter_spots(region, categories, season)

    if not pool:
        return jsonify({"error": "条件に合うスポットが見つかりません。"}), 404

    # 地方ごとにグループ化
    if region and region != "全国":
        grouped = {region: pool}
    else:
        grouped = {}
        for r in REGION_ORDER:
            spots_in_r = [s for s in pool if s["region"] == r]
            if spots_in_r:
                grouped[r] = spots_in_r

    # 各スポットにじゃらんURLとGoogleマップURLを付加
    result = {}
    for region_name, spots in grouped.items():
        result[region_name] = []
        for spot in spots:
            query = urllib.parse.quote(f"{spot['name']} {spot['pref']}")
            pref_name = spot["pref"].split()[0]
            jalan_base = "https://px.a8.net/svt/ejp?a8mat=4B1PLQ+1SCD6+14CS+67JUA&a8ejpredirect="
            jalan_search = f"https://www.jalan.net/yad/?CenS=1&keyword={pref_name}"
            jalan_url = jalan_base + urllib.parse.quote(jalan_search, safe="")
            result[region_name].append({
                **spot,
                "map_url": f"https://www.google.com/maps/search/?api=1&query={query}",
                "jalan_url": jalan_url,
            })

    return jsonify({"regions": result, "total": len(pool)})


if __name__ == "__main__":
    app.run(debug=True)
