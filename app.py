import streamlit as st
import random
import urllib.parse

# ─────────────────────────────────────────────
#  データ定義
# ─────────────────────────────────────────────
SPOTS = [
    # ── 北海道 ──────────────────────────────
    {
        "name": "函館山・五稜郭",
        "pref": "北海道 函館市",
        "region": "北海道",
        "category": ["歴史・文化", "夜景"],
        "seasons": ["夏", "秋"],
        "desc": (
            "幕末に築造された星型の西洋式城郭・五稜郭と、日本三大夜景に数えられる"
            "函館山の夜景が有名。ペリー来航ゆかりの地でもあり、元町の異国情緒ある"
            "街並みも楽しめます。"
        ),
        "highlights": ["星型要塞", "夜景スポット", "元町洋館街", "函館朝市"],
        "links": [
            {"label": "じゃらん 函館", "url": "https://www.jalan.net/kankou/spt_01202ag2130000009/"},
            {"label": "函館市観光情報", "url": "https://www.hakodatejin.com/"},
        ],
    },
    {
        "name": "富良野・美瑛",
        "pref": "北海道 富良野市・上川郡",
        "region": "北海道",
        "category": ["自然・絶景", "アウトドア"],
        "seasons": ["夏"],
        "desc": (
            "7〜8月はラベンダーが一面に広がる丘が圧巻。パッチワークの丘と呼ばれる"
            "美瑛の農村風景も北海道らしい広大なスケールで、サイクリングやドライブが楽しめます。"
        ),
        "highlights": ["ラベンダー畑", "パッチワークの丘", "ファーム富田", "青い池（美瑛）"],
        "links": [
            {"label": "じゃらん 富良野", "url": "https://www.jalan.net/kankou/spt_010300/"},
            {"label": "北海道観光公式", "url": "https://www.visit-hokkaido.jp/"},
        ],
    },
    {
        "name": "知床五湖・羅臼",
        "pref": "北海道 斜里郡・目梨郡",
        "region": "北海道",
        "category": ["自然・絶景", "アウトドア", "世界遺産"],
        "seasons": ["夏", "秋"],
        "desc": (
            "ユネスコ世界自然遺産に登録された知床半島。五湖を巡る高架木道からは"
            "ヒグマに出会えることも。羅臼では流氷クルーズやホエールウォッチングが人気です。"
        ),
        "highlights": ["知床五湖高架木道", "ヒグマ観察", "流氷クルーズ", "ホエールウォッチング", "カムイワッカ湯の滝"],
        "links": [
            {"label": "知床観光公式", "url": "https://www.shiretoko.asia/"},
            {"label": "じゃらん 知床", "url": "https://www.jalan.net/kankou/spt_010420/"},
        ],
    },
    {
        "name": "小樽・余市",
        "pref": "北海道 小樽市・余市郡",
        "region": "北海道",
        "category": ["歴史・文化", "グルメ"],
        "seasons": ["春", "夏", "冬"],
        "desc": (
            "石造り倉庫が立ち並ぶ小樽運河は北海道屈指のフォトスポット。"
            "寿司・海鮮丼も絶品で、余市ではニッカウヰスキーの蒸溜所見学が楽しめます。"
        ),
        "highlights": ["小樽運河", "寿司・海鮮丼", "ニッカウヰスキー余市蒸溜所", "堺町通り"],
        "links": [
            {"label": "小樽観光協会", "url": "https://otaru.gr.jp/"},
            {"label": "余市観光", "url": "https://yoichi-kankou.jp/"},
        ],
    },
    {
        "name": "登別温泉・洞爺湖",
        "pref": "北海道 登別市・虻田郡",
        "region": "北海道",
        "category": ["温泉・癒し", "自然・絶景"],
        "seasons": ["春", "夏", "秋", "冬"],
        "desc": (
            "日本有数の湯量を誇る登別温泉は9種類の泉質が湧く「温泉のデパート」。"
            "地獄谷の迫力は圧倒的で、近隣の洞爺湖は支笏洞爺国立公園内の美しいカルデラ湖です。"
        ),
        "highlights": ["地獄谷", "9種の泉質", "洞爺湖サイロ展望台", "有珠山ロープウェイ"],
        "links": [
            {"label": "登別温泉観光", "url": "https://www.noboribetsu-spa.jp/"},
            {"label": "洞爺湖観光", "url": "https://www.laketoya.com/"},
        ],
    },
    # ── 東北 ──────────────────────────────
    {
        "name": "弘前城・弘前公園",
        "pref": "青森県 弘前市",
        "region": "東北",
        "category": ["歴史・文化", "自然・絶景"],
        "seasons": ["春"],
        "desc": (
            "日本屈指の桜の名所。天守が現存する数少ない城のひとつで、春には約2600本の"
            "ソメイヨシノが濠を覆うほど咲き誇る「花筏」が絶景です。りんご農園巡りも人気。"
        ),
        "highlights": ["現存天守", "花筏（桜×濠）", "津軽三味線", "りんご街道"],
        "links": [
            {"label": "弘前市観光情報", "url": "https://www.hirosaki-kanko.or.jp/"},
        ],
    },
    {
        "name": "奥入瀬渓流・十和田湖",
        "pref": "青森県 十和田市",
        "region": "東北",
        "category": ["自然・絶景", "アウトドア"],
        "seasons": ["春", "夏", "秋"],
        "desc": (
            "14kmにわたって続く渓流沿いの遊歩道は新緑・紅葉ともに絶景。"
            "水量豊富な滝が連続し、十和田湖の神秘的な青さとセットで楽しむ自然旅の定番です。"
        ),
        "highlights": ["銚子大滝", "渓流沿い遊歩道", "十和田湖遊覧船", "紅葉"],
        "links": [
            {"label": "奥入瀬渓流観光", "url": "https://www.oirase-keikoku.com/"},
            {"label": "十和田観光", "url": "https://www.towada.travel/ja"},
        ],
    },
    {
        "name": "猊鼻渓・厳美渓",
        "pref": "岩手県 一関市",
        "region": "東北",
        "category": ["自然・絶景", "アウトドア"],
        "seasons": ["春", "秋"],
        "desc": (
            "国指定名勝の猊鼻渓は、約2kmの砂鉄川沿いを平底舟でゆったり下る舟下りが名物。"
            "高さ100mを超える石灰岩の断崖が続き、四季折々の絶景が楽しめます。"
        ),
        "highlights": ["舟下り", "石灰岩断崖", "こびき唄", "厳美渓の空飛ぶだんご"],
        "links": [
            {"label": "岩手観光ガイド", "url": "https://iwatetabi.jp/"},
            {"label": "猊鼻渓観光", "url": "http://www.geibikei.co.jp/"},
        ],
    },
    {
        "name": "平泉・中尊寺金色堂",
        "pref": "岩手県 西磐井郡",
        "region": "東北",
        "category": ["歴史・文化", "世界遺産"],
        "seasons": ["春", "秋"],
        "desc": (
            "奥州藤原氏が栄華を誇った平安時代の遺跡群がユネスコ世界文化遺産に登録。"
            "金色堂は黄金に輝く傑作で、芭蕉も旅した毛越寺の浄土庭園も静寂の美があります。"
        ),
        "highlights": ["中尊寺金色堂", "毛越寺浄土庭園", "芭蕉句碑", "わんこそば"],
        "links": [
            {"label": "平泉観光公式", "url": "https://hiraizumi.or.jp/"},
        ],
    },
    {
        "name": "仙台・松島",
        "pref": "宮城県 仙台市・宮城郡",
        "region": "東北",
        "category": ["自然・絶景", "グルメ"],
        "seasons": ["春", "秋", "冬"],
        "desc": (
            "日本三景のひとつ、松島は大小約260の島が点在する多島美の絶景地。"
            "遊覧船から眺める景色は格別で、名物の牡蠣や穴子丼も楽しみ。仙台では牛タンが必食です。"
        ),
        "highlights": ["日本三景", "遊覧船", "牡蠣・穴子丼", "瑞巌寺", "仙台牛タン"],
        "links": [
            {"label": "松島観光協会", "url": "https://www.matsushima-kanko.com/"},
            {"label": "仙台観光情報", "url": "https://www.sentabi.jp/"},
        ],
    },
    {
        "name": "角館・武家屋敷",
        "pref": "秋田県 仙北市",
        "region": "東北",
        "category": ["歴史・文化", "自然・絶景"],
        "seasons": ["春"],
        "desc": (
            "「みちのくの小京都」と呼ばれる城下町。武家屋敷の黒板塀とシダレザクラが同居する景色は"
            "全国屈指の桜スポット。秋の紅葉も美しく、比内地鶏きりたんぽも名物です。"
        ),
        "highlights": ["武家屋敷", "シダレザクラ", "きりたんぽ鍋", "比内地鶏"],
        "links": [
            {"label": "角館観光情報", "url": "https://www.kakunodate-kanko.jp/"},
        ],
    },
    {
        "name": "山寺（立石寺）",
        "pref": "山形県 山形市",
        "region": "東北",
        "category": ["歴史・文化", "自然・絶景"],
        "seasons": ["春", "夏", "秋"],
        "desc": (
            "松尾芭蕉「閑さや 岩にしみ入る 蝉の声」で有名な霊場。1015段の石段を登ると、"
            "奇岩と杉林の向こうに山形盆地が広がる絶景が待っています。"
        ),
        "highlights": ["1015段の石段", "奇岩絶景", "芭蕉の句碑", "山形芋煮"],
        "links": [
            {"label": "山寺観光", "url": "https://www.yamaderakankou.com/"},
        ],
    },
    {
        "name": "会津若松・鶴ヶ城",
        "pref": "福島県 会津若松市",
        "region": "東北",
        "category": ["歴史・文化"],
        "seasons": ["春", "秋"],
        "desc": (
            "戊辰戦争・白虎隊の悲話で知られる会津。鶴ヶ城から望む磐梯山の眺望と春の桜が名高く、"
            "七日町通りの大正浪漫な町並みや喜多方ラーメンも人気です。"
        ),
        "highlights": ["鶴ヶ城", "白虎隊記念館", "七日町通り", "喜多方ラーメン"],
        "links": [
            {"label": "会津若松観光", "url": "https://www.aizukanko.com/"},
        ],
    },
    # ── 関東 ──────────────────────────────
    {
        "name": "日光東照宮・中禅寺湖",
        "pref": "栃木県 日光市",
        "region": "関東",
        "category": ["歴史・文化", "世界遺産", "自然・絶景"],
        "seasons": ["春", "秋"],
        "desc": (
            "徳川家康を祀る絢爛豪華な社殿群は世界遺産。奥日光の中禅寺湖と男体山、"
            "華厳の滝、竜頭の滝の紅葉は特に名高く、湯元温泉も人気の滞在スポットです。"
        ),
        "highlights": ["世界遺産", "陽明門", "華厳の滝", "中禅寺湖紅葉", "湯元温泉"],
        "links": [
            {"label": "日光観光協会", "url": "https://www.nikko-kankou.org/"},
            {"label": "世界遺産日光", "url": "https://www.nikko-toshogu.or.jp/"},
        ],
    },
    {
        "name": "那須高原・塩原温泉",
        "pref": "栃木県 那須郡",
        "region": "関東",
        "category": ["自然・絶景", "温泉・癒し", "アウトドア"],
        "seasons": ["春", "夏", "秋"],
        "desc": (
            "関東からのアクセスが良い高原リゾート。那須岳登山やサイクリング、ハイキングが楽しめ、"
            "塩原温泉は渓谷沿いに温泉宿が並ぶ癒やしの地です。"
        ),
        "highlights": ["那須岳登山", "那須高原の牧場", "塩原温泉渓谷", "りんどう湖"],
        "links": [
            {"label": "那須観光", "url": "https://www.nasu-kankou.com/"},
            {"label": "塩原温泉", "url": "https://www.nasu-shiobara.jp/onsen/"},
        ],
    },
    {
        "name": "秩父・三峯神社",
        "pref": "埼玉県 秩父市",
        "region": "関東",
        "category": ["歴史・文化", "自然・絶景"],
        "seasons": ["春", "秋", "冬"],
        "desc": (
            "関東随一のパワースポットとして名高い三峯神社は標高1100mに鎮座する神秘的な空間。"
            "秩父夜祭（12月）は国重要無形民俗文化財で、SL列車やわらじかつ丼も名物です。"
        ),
        "highlights": ["三峯神社", "秩父夜祭", "SL列車", "わらじかつ丼", "芝桜"],
        "links": [
            {"label": "秩父観光なび", "url": "https://www.chichibu.co.jp/"},
            {"label": "三峯神社", "url": "https://www.mitsuminejinja.or.jp/"},
        ],
    },
    {
        "name": "鎌倉・江ノ島",
        "pref": "神奈川県 鎌倉市・藤沢市",
        "region": "関東",
        "category": ["歴史・文化", "自然・絶景", "グルメ"],
        "seasons": ["春", "夏", "秋"],
        "desc": (
            "鎌倉幕府の中心地として栄えた古都で、高徳院の大仏や鶴岡八幡宮が有名。"
            "江ノ電に乗り江ノ島の海鮮や夕景を楽しむコースは定番で、寺院のあじさいも有名です。"
        ),
        "highlights": ["鎌倉大仏", "江ノ電", "江ノ島", "あじさい寺", "鶴岡八幡宮"],
        "links": [
            {"label": "鎌倉観光公式", "url": "https://www.kamakura-info.jp/"},
            {"label": "江ノ島公式", "url": "https://www.enoshima-navi.jp/"},
        ],
    },
    {
        "name": "箱根・芦ノ湖",
        "pref": "神奈川県 足柄下郡",
        "region": "関東",
        "category": ["自然・絶景", "温泉・癒し", "アウトドア"],
        "seasons": ["春", "秋", "冬"],
        "desc": (
            "富士山を望む芦ノ湖の湖畔と多彩な温泉が魅力の関東屈指のリゾート地。"
            "ロープウェイ・登山鉄道・船と乗り物も豊富で、大涌谷の黒たまごも名物です。"
        ),
        "highlights": ["芦ノ湖から富士山", "大涌谷", "箱根登山鉄道", "温泉旅館", "黒たまご"],
        "links": [
            {"label": "箱根ナビ", "url": "https://www.hakonenavi.jp/"},
        ],
    },
    # ── 中部 ──────────────────────────────
    {
        "name": "上高地・乗鞍",
        "pref": "長野県 松本市",
        "region": "中部",
        "category": ["自然・絶景", "アウトドア"],
        "seasons": ["春", "夏", "秋"],
        "desc": (
            "標高1500mのマイカー規制区域に広がる奥山の楽園。河童橋から望む穂高連峰と"
            "澄んだ梓川の流れが絶景。大正池の早朝の霧幻景も幻想的で、ハイキングの聖地です。"
        ),
        "highlights": ["河童橋", "穂高連峰", "大正池", "高山植物", "乗鞍岳"],
        "links": [
            {"label": "上高地公式", "url": "https://www.kamikochi.or.jp/"},
        ],
    },
    {
        "name": "軽井沢・浅間山",
        "pref": "長野県 北佐久郡",
        "region": "中部",
        "category": ["自然・絶景", "アウトドア", "グルメ"],
        "seasons": ["春", "夏", "秋"],
        "desc": (
            "明治から続く高原リゾート。旧軽井沢銀座の食べ歩き、サイクリング、星空観察が楽しめ、"
            "浅間山を望む白糸の滝やプリンスショッピングプラザも人気スポットです。"
        ),
        "highlights": ["旧軽井沢銀座", "白糸の滝", "サイクリング", "星空観察", "浅間山"],
        "links": [
            {"label": "軽井沢観光", "url": "https://karuizawa-kankokyokai.jp/"},
        ],
    },
    {
        "name": "飛騨高山・白川郷",
        "pref": "岐阜県 高山市・大野郡",
        "region": "中部",
        "category": ["歴史・文化", "世界遺産", "グルメ"],
        "seasons": ["春", "夏", "秋", "冬"],
        "desc": (
            "「飛騨の小京都」高山の三町古い町並みと、ユネスコ世界遺産の合掌造り集落・白川郷は"
            "車で約1時間。冬の雪の白川郷は別格の美しさで、飛騨牛や朴葉味噌も絶品です。"
        ),
        "highlights": ["白川郷（世界遺産）", "高山古い町並み", "飛騨牛", "朴葉味噌", "陣屋朝市"],
        "links": [
            {"label": "高山市観光", "url": "https://www.hida.jp/"},
            {"label": "白川郷観光", "url": "https://shirakawa-go.gr.jp/"},
        ],
    },
    {
        "name": "伊勢神宮・鳥羽・志摩",
        "pref": "三重県 伊勢市",
        "region": "中部",
        "category": ["歴史・文化", "グルメ", "自然・絶景"],
        "seasons": ["春", "秋"],
        "desc": (
            "日本人の心のふるさと・伊勢神宮（内宮・外宮）は年間800万人超が訪れる聖地。"
            "おはらい町での食べ歩き、鳥羽水族館、志摩のカキや伊勢海老も魅力です。"
        ),
        "highlights": ["伊勢神宮内宮", "おはらい町", "赤福", "伊勢海老・牡蠣", "鳥羽水族館"],
        "links": [
            {"label": "伊勢市観光", "url": "https://www.kanko-ise.jp/"},
        ],
    },
    {
        "name": "金沢・兼六園",
        "pref": "石川県 金沢市",
        "region": "中部",
        "category": ["歴史・文化", "グルメ", "自然・絶景"],
        "seasons": ["春", "秋", "冬"],
        "desc": (
            "日本三名園のひとつ兼六園と、近江町市場の海鮮が有名な「小京都」。"
            "ひがし茶屋街の石畳、21世紀美術館、加賀料理と見どころが豊富です。"
        ),
        "highlights": ["兼六園", "ひがし茶屋街", "近江町市場", "21世紀美術館", "加賀料理"],
        "links": [
            {"label": "金沢観光公式", "url": "https://www.kanazawa-tourism.com/"},
        ],
    },
    {
        "name": "富士山・富士五湖",
        "pref": "山梨県・静岡県",
        "region": "中部",
        "category": ["自然・絶景", "アウトドア", "世界遺産"],
        "seasons": ["夏", "秋"],
        "desc": (
            "日本最高峰・富士山は世界文化遺産。夏の登山シーズンは山頂からのご来光が圧巻。"
            "河口湖・山中湖などの富士五湖エリアはリゾート・キャンプの拠点としても人気です。"
        ),
        "highlights": ["富士山登山（夏）", "ご来光", "河口湖", "忍野八海", "富士スバルライン"],
        "links": [
            {"label": "富士山観光", "url": "https://www.fujisan-climb.jp/"},
            {"label": "富士五湖観光", "url": "https://fujigoko.tv/"},
        ],
    },
    {
        "name": "熱海・伊豆",
        "pref": "静岡県 熱海市・伊豆半島",
        "region": "中部",
        "category": ["温泉・癒し", "自然・絶景", "グルメ"],
        "seasons": ["春", "夏", "冬"],
        "desc": (
            "関東から最も近い温泉リゾートとして復権した熱海と、豊かな海と山の自然が広がる伊豆半島。"
            "河津桜（2月）、城ヶ崎海岸のつり橋、西伊豆の夕日と金目鯛が魅力です。"
        ),
        "highlights": ["熱海温泉", "河津桜（2月）", "城ヶ崎海岸", "西伊豆夕日", "金目鯛"],
        "links": [
            {"label": "熱海観光協会", "url": "https://www.ataminews.gr.jp/"},
            {"label": "伊豆観光", "url": "https://www.izukanko.or.jp/"},
        ],
    },
    # ── 近畿 ──────────────────────────────
    {
        "name": "京都・嵐山・嵯峨野",
        "pref": "京都府 京都市右京区",
        "region": "近畿",
        "category": ["歴史・文化", "自然・絶景"],
        "seasons": ["春", "秋"],
        "desc": (
            "渡月橋と嵐山の山並み、竹林の小径、天龍寺の曹源池庭園が一帯に凝縮した京都屈指の景勝地。"
            "トロッコ列車で保津川渓谷を下る体験も人気で、桜・紅葉は特に混雑します。"
        ),
        "highlights": ["竹林の小径", "渡月橋", "天龍寺庭園", "トロッコ列車", "湯豆腐"],
        "links": [
            {"label": "嵐山観光", "url": "https://www.arashiyama-kyoto.com/"},
            {"label": "京都観光Navi", "url": "https://kyoto.travel/ja"},
        ],
    },
    {
        "name": "京都・東山・祇園",
        "pref": "京都府 京都市東山区",
        "region": "近畿",
        "category": ["歴史・文化", "グルメ"],
        "seasons": ["春", "秋"],
        "desc": (
            "清水寺・八坂神社・二年坂・産寧坂が連なる京都観光の王道エリア。"
            "石畳の路地に舞妓・芸妓文化が息づく祇園の夜散策も格別です。京料理や抹茶スイーツも充実。"
        ),
        "highlights": ["清水寺舞台", "産寧坂・二年坂", "八坂神社", "祇園白川", "京料理"],
        "links": [
            {"label": "京都観光Navi", "url": "https://kyoto.travel/ja"},
        ],
    },
    {
        "name": "奈良・東大寺・春日大社",
        "pref": "奈良県 奈良市",
        "region": "近畿",
        "category": ["歴史・文化", "世界遺産"],
        "seasons": ["春", "秋"],
        "desc": (
            "世界遺産に登録された古都奈良のシンボル、高さ15mの奈良の大仏（東大寺）と"
            "約1200頭の野生の鹿が共存する奈良公園は別格の体験。柿の葉寿司も名物。"
        ),
        "highlights": ["奈良の大仏", "奈良公園の鹿", "春日大社", "興福寺", "柿の葉寿司"],
        "links": [
            {"label": "奈良観光公式", "url": "https://yamatoji.nara-kankou.or.jp/"},
            {"label": "東大寺公式", "url": "https://www.todaiji.or.jp/"},
        ],
    },
    {
        "name": "大阪・道頓堀・天王寺",
        "pref": "大阪府 大阪市",
        "region": "近畿",
        "category": ["グルメ", "歴史・文化"],
        "seasons": ["春", "秋"],
        "desc": (
            "「食い倒れの街」大阪のグルメと活気を体感できる道頓堀・なんば周辺。"
            "たこ焼き・串かつを食べ歩き、通天閣・大阪城・USJも定番です。"
        ),
        "highlights": ["道頓堀グルメ", "たこ焼き・串かつ", "大阪城", "通天閣", "USJ"],
        "links": [
            {"label": "大阪観光公式", "url": "https://osaka-info.jp/"},
        ],
    },
    {
        "name": "神戸・北野・有馬温泉",
        "pref": "兵庫県 神戸市",
        "region": "近畿",
        "category": ["歴史・文化", "温泉・癒し", "グルメ"],
        "seasons": ["春", "秋"],
        "desc": (
            "異国情緒漂う異人館街と、日本最古の温泉地のひとつ有馬温泉が同じ神戸市内に。"
            "神戸牛・スイーツ・南京町グルメに加え、夜景スポットの摩耶山掬星台も人気です。"
        ),
        "highlights": ["北野異人館", "有馬温泉（金湯・銀湯）", "神戸牛", "南京町", "摩耶山夜景"],
        "links": [
            {"label": "神戸観光公式", "url": "https://www.feel-kobe.jp/"},
            {"label": "有馬温泉観光", "url": "https://www.arima-onsen.com/"},
        ],
    },
    {
        "name": "姫路城・書写山圓教寺",
        "pref": "兵庫県 姫路市",
        "region": "近畿",
        "category": ["歴史・文化", "世界遺産"],
        "seasons": ["春"],
        "desc": (
            "「白鷺城」の美称を持つ日本最大の木造城郭で、ユネスコ世界遺産かつ国宝。"
            "桜との組み合わせは格別で、ラストサムライのロケ地・書写山も近くにあります。"
        ),
        "highlights": ["白鷺城（世界遺産）", "現存天守", "春の桜", "書写山圓教寺", "姫路おでん"],
        "links": [
            {"label": "姫路城公式", "url": "https://www.city.himeji.lg.jp/castle/"},
        ],
    },
    {
        "name": "熊野古道・那智の滝",
        "pref": "和歌山県 東牟婁郡",
        "region": "近畿",
        "category": ["歴史・文化", "世界遺産", "アウトドア"],
        "seasons": ["春", "秋"],
        "desc": (
            "世界遺産「紀伊山地の霊場と参詣道」を構成する熊野古道。苔むす石畳の参道と"
            "日本一の落差・那智の滝（133m）は神秘的で、熊野三山巡りが人気です。"
        ),
        "highlights": ["熊野古道石畳", "那智の滝（133m）", "熊野三山巡り", "温泉"],
        "links": [
            {"label": "和歌山観光", "url": "https://www.wakayama-kanko.or.jp/"},
            {"label": "熊野古道", "url": "https://www.tb-kumano.jp/kumano-kodo/"},
        ],
    },
    # ── 中国 ──────────────────────────────
    {
        "name": "広島・宮島・厳島神社",
        "pref": "広島県 広島市・廿日市市",
        "region": "中国",
        "category": ["歴史・文化", "世界遺産", "グルメ"],
        "seasons": ["春", "秋"],
        "desc": (
            "世界遺産の厳島神社の海上大鳥居は日本屈指の絶景。平和記念公園・原爆ドームとセットで"
            "訪問する歴史旅が定番。もみじ饅頭と広島お好み焼きは必食です。"
        ),
        "highlights": ["海上大鳥居（世界遺産）", "原爆ドーム", "平和記念公園", "もみじ饅頭", "広島お好み焼き"],
        "links": [
            {"label": "宮島観光協会", "url": "https://www.miyajima.or.jp/"},
            {"label": "広島観光", "url": "https://www.hiroshima-kankou.com/"},
        ],
    },
    {
        "name": "出雲大社・足立美術館",
        "pref": "島根県 出雲市・安来市",
        "region": "中国",
        "category": ["歴史・文化", "自然・絶景"],
        "seasons": ["春", "秋"],
        "desc": (
            "縁結びの神様として名高い出雲大社と、日本一の庭園と呼ばれる足立美術館が同じ島根県に。"
            "10〜11月の神在月の神事は神秘的で、出雲そばも名物です。"
        ),
        "highlights": ["出雲大社", "縁結び", "足立美術館の庭園", "神在月", "出雲そば"],
        "links": [
            {"label": "出雲観光ガイド", "url": "https://www.izumo-kankou.gr.jp/"},
            {"label": "足立美術館", "url": "https://www.adachi-museum.or.jp/"},
        ],
    },
    {
        "name": "倉敷美観地区",
        "pref": "岡山県 倉敷市",
        "region": "中国",
        "category": ["歴史・文化", "グルメ"],
        "seasons": ["春", "秋"],
        "desc": (
            "白壁の土蔵と柳並木が続く倉敷川沿いの美観地区は江戸時代の商都の面影を残す国の重要伝統的建造物群。"
            "大原美術館は日本初の西洋美術館で、デニムの聖地・児島も近くにあります。"
        ),
        "highlights": ["倉敷美観地区", "大原美術館", "倉敷川のんびり舟", "デニム・ジーンズ"],
        "links": [
            {"label": "倉敷観光", "url": "https://www.kurashiki-tabi.jp/"},
        ],
    },
    # ── 四国 ──────────────────────────────
    {
        "name": "道後温泉・松山城",
        "pref": "愛媛県 松山市",
        "region": "四国",
        "category": ["温泉・癒し", "歴史・文化"],
        "seasons": ["春", "秋"],
        "desc": (
            "日本最古の温泉のひとつとされる道後温泉本館は2024年保存修理完了。"
            "夏目漱石「坊っちゃん」の舞台としても知られ、松山城天守と鯛めしが名物です。"
        ),
        "highlights": ["道後温泉本館", "夏目漱石ゆかりの地", "松山城", "鯛めし", "蛇口みかんジュース"],
        "links": [
            {"label": "松山観光", "url": "https://www.matsuyama-sightseeing.com/"},
            {"label": "道後温泉公式", "url": "https://dogo.jp/"},
        ],
    },
    {
        "name": "高知・桂浜・四万十川",
        "pref": "高知県 高知市・四万十市",
        "region": "四国",
        "category": ["自然・絶景", "歴史・文化", "グルメ"],
        "seasons": ["春", "夏", "秋"],
        "desc": (
            "坂本龍馬ゆかりの地・桂浜は太平洋を望む豪快な海岸線。「最後の清流」四万十川では"
            "沈下橋や川の幸を楽しめます。カツオのたたきとひろめ市場は必体験。"
        ),
        "highlights": ["桂浜", "坂本龍馬記念館", "四万十川・沈下橋", "カツオのたたき", "ひろめ市場"],
        "links": [
            {"label": "高知観光", "url": "https://www.attaka.or.jp/"},
            {"label": "四万十観光", "url": "https://shimanto-kanko.com/"},
        ],
    },
    {
        "name": "大歩危・祖谷のかずら橋",
        "pref": "徳島県 三好市",
        "region": "四国",
        "category": ["自然・絶景", "アウトドア"],
        "seasons": ["春", "夏", "秋"],
        "desc": (
            "吉野川上流の大歩危峡の渓谷美と、シラクチカズラで編まれた「かずら橋」はスリル満点。"
            "秘境・祖谷温泉や平家落人伝説が息づく集落も魅力の四国山地の深部です。"
        ),
        "highlights": ["大歩危峡ライン下り", "かずら橋スリル体験", "祖谷温泉", "平家落人集落"],
        "links": [
            {"label": "徳島観光", "url": "https://www.awanavi.jp/"},
        ],
    },
    {
        "name": "こんぴらさん・栗林公園",
        "pref": "香川県 仲多度郡・高松市",
        "region": "四国",
        "category": ["歴史・文化", "自然・絶景", "グルメ"],
        "seasons": ["春", "秋"],
        "desc": (
            "海の神様として名高い金刀比羅宮（こんぴらさん）は785段の石段で参拝する讃岐の名社。"
            "高松の栗林公園は特別名勝の大名庭園で、讃岐うどんはもちろん全国から食通が集まります。"
        ),
        "highlights": ["785段の石段", "金刀比羅宮", "栗林公園（特別名勝）", "讃岐うどん"],
        "links": [
            {"label": "香川観光", "url": "https://www.my-kagawa.jp/"},
            {"label": "こんぴらさん公式", "url": "https://www.konpira.or.jp/"},
        ],
    },
    # ── 九州 ──────────────────────────────
    {
        "name": "博多・太宰府・柳川",
        "pref": "福岡県 福岡市・太宰府市",
        "region": "九州",
        "category": ["歴史・文化", "グルメ"],
        "seasons": ["春", "秋"],
        "desc": (
            "九州の玄関口・博多は屋台グルメの聖地。学問の神様・太宰府天満宮は梅の名所で"
            "梅が枝餅が名物。水郷柳川の船下りも周辺の定番観光です。"
        ),
        "highlights": ["博多屋台", "博多ラーメン・もつ鍋", "太宰府天満宮", "梅が枝餅", "柳川船下り"],
        "links": [
            {"label": "福岡観光公式", "url": "https://yokanavi.com/"},
            {"label": "太宰府観光協会", "url": "https://www.dazaifu.org/"},
        ],
    },
    {
        "name": "長崎・グラバー園・軍艦島",
        "pref": "長崎県 長崎市",
        "region": "九州",
        "category": ["歴史・文化", "世界遺産", "夜景"],
        "seasons": ["春", "秋"],
        "desc": (
            "日本三大夜景の稲佐山、世界遺産の軍艦島クルーズ、グラバー園の洋館群が揃う港町。"
            "出島など鎖国時代の痕跡も多く、ちゃんぽん・皿うどん・カステラも名物です。"
        ),
        "highlights": ["軍艦島クルーズ", "稲佐山夜景", "グラバー園", "出島", "ちゃんぽん・カステラ"],
        "links": [
            {"label": "長崎観光公式", "url": "https://www.nagasaki-tabinet.com/"},
            {"label": "軍艦島クルーズ", "url": "https://www.gunkan-jima.net/"},
        ],
    },
    {
        "name": "阿蘇・くじゅう連山",
        "pref": "熊本県 阿蘇市",
        "region": "九州",
        "category": ["自然・絶景", "アウトドア"],
        "seasons": ["春", "夏", "秋"],
        "desc": (
            "世界最大級のカルデラを持つ阿蘇山は、今も活動する草千里ヶ浜と中岳火口が迫力満点。"
            "くじゅう連山の高原トレッキング、地獄温泉、馬刺し・あか牛も大人気です。"
        ),
        "highlights": ["草千里ヶ浜", "中岳火口展望", "くじゅう高原", "馬刺し・あか牛", "地獄温泉"],
        "links": [
            {"label": "阿蘇観光ガイド", "url": "https://www.asocity-kanko.jp/"},
        ],
    },
    {
        "name": "黒川温泉・湯布院",
        "pref": "熊本県・大分県",
        "region": "九州",
        "category": ["温泉・癒し", "自然・絶景"],
        "seasons": ["春", "秋", "冬"],
        "desc": (
            "湯めぐり手形で複数の湯に入れる黒川温泉は「温泉文化」で有名な秘湯系温泉地。"
            "由布岳を望む湯布院は由布川渓谷・金鱗湖の朝霧が幻想的で、カフェや雑貨店も充実します。"
        ),
        "highlights": ["湯めぐり手形", "黒川温泉の露天風呂", "金鱗湖の朝霧", "由布岳登山"],
        "links": [
            {"label": "黒川温泉観光", "url": "https://www.kurokawaonsen.or.jp/"},
            {"label": "湯布院観光", "url": "https://www.yufuin.gr.jp/"},
        ],
    },
    {
        "name": "屋久島・縄文杉",
        "pref": "鹿児島県 熊毛郡",
        "region": "九州",
        "category": ["自然・絶景", "アウトドア", "世界遺産"],
        "seasons": ["春", "夏"],
        "desc": (
            "樹齢2000〜7000年とも言われる縄文杉を目指す約22kmのトレッキングコースは世界遺産の洗礼。"
            "白谷雲水峡はもののけ姫の原風景とされ、島内は30分に1度雨が降る神秘的な気候です。"
        ),
        "highlights": ["縄文杉（世界遺産）", "白谷雲水峡", "ヤクザル・ヤクシカ", "苔の森"],
        "links": [
            {"label": "屋久島観光協会", "url": "https://www.yakushima.or.jp/"},
        ],
    },
    # ── 沖縄 ──────────────────────────────
    {
        "name": "首里城・美ら海水族館",
        "pref": "沖縄県 那覇市・本部町",
        "region": "沖縄",
        "category": ["歴史・文化", "自然・絶景"],
        "seasons": ["冬", "春"],
        "desc": (
            "琉球王国の遺産・首里城（復元工事中）と、ジンベイザメで有名な美ら海水族館が沖縄旅の定番。"
            "コバルトブルーの海でシュノーケリングや離島巡りも充実しています。"
        ),
        "highlights": ["首里城", "美ら海水族館（ジンベイザメ）", "エメラルドの海", "沖縄そば", "国際通り"],
        "links": [
            {"label": "沖縄観光公式", "url": "https://www.okinawastory.jp/"},
            {"label": "美ら海水族館", "url": "https://churaumi.okinawa/"},
        ],
    },
    {
        "name": "竹富島・西表島",
        "pref": "沖縄県 八重山郡",
        "region": "沖縄",
        "category": ["自然・絶景", "アウトドア"],
        "seasons": ["冬", "春", "夏"],
        "desc": (
            "石垣島からフェリーで行ける八重山の離島。竹富島は赤瓦・石畳の伝統集落と水牛車が有名で、"
            "西表島はマングローブ林と国立公園の大自然が待つ。星砂の浜のロマンも格別です。"
        ),
        "highlights": ["水牛車", "赤瓦の集落", "西表マングローブ", "由布島", "星砂の浜"],
        "links": [
            {"label": "八重山観光", "url": "https://www.yaeyama.or.jp/"},
        ],
    },
    {
        "name": "宮古島・久高島",
        "pref": "沖縄県 宮古島市",
        "region": "沖縄",
        "category": ["自然・絶景", "アウトドア"],
        "seasons": ["春", "夏"],
        "desc": (
            "透明度抜群の宮古ブルーとイムギャーマリンガーデンは日本屈指のシュノーケリングスポット。"
            "与那覇前浜ビーチは東洋一とも称され、久高島は琉球神話の聖地として神聖な雰囲気が漂います。"
        ),
        "highlights": ["宮古ブルーの海", "与那覇前浜ビーチ", "シュノーケリング・ダイビング", "久高島"],
        "links": [
            {"label": "宮古島観光", "url": "https://miyako-guide.net/"},
        ],
    },
]

# ─────────────────────────────────────────────
#  定数
# ─────────────────────────────────────────────
ALL_REGIONS = ["全国", "北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州", "沖縄"]

ALL_CATEGORIES = sorted({cat for spot in SPOTS for cat in spot["category"]})

SEASON_EMOJI = {"春": "🌸", "夏": "☀️", "秋": "🍁", "冬": "❄️"}
CATEGORY_EMOJI = {
    "歴史・文化": "🏯",
    "自然・絶景": "🏔️",
    "アウトドア": "🥾",
    "グルメ": "🍜",
    "温泉・癒し": "♨️",
    "世界遺産": "🌏",
    "夜景": "🌃",
}

# ─────────────────────────────────────────────
#  ページ設定
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="旅行プラン ルーレット 🎲",
    page_icon="🗾",
    layout="centered",
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap');

    h1 { font-family: 'Noto Serif JP', serif !important; }

    .spot-card {
        background: #f8f7f4;
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        border: 1px solid #e0ddd6;
        margin-top: 1rem;
    }
    .spot-name {
        font-family: 'Noto Serif JP', serif;
        font-size: 1.7rem;
        font-weight: 700;
        margin-bottom: 0.1rem;
    }
    .spot-pref {
        color: #888;
        font-size: 0.9rem;
        margin-bottom: 0.8rem;
    }
    .tag {
        display: inline-block;
        background: #ede9e1;
        border-radius: 999px;
        padding: 3px 12px;
        font-size: 0.78rem;
        margin-right: 5px;
        margin-bottom: 5px;
        color: #555;
    }
    .highlight-tag {
        display: inline-block;
        background: #fff;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 4px 12px;
        font-size: 0.82rem;
        margin-right: 6px;
        margin-bottom: 6px;
        color: #444;
    }
    .season-good { color: #2e7d32; font-weight: 600; }
    .season-off  { color: #bbb; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  セッション初期化
# ─────────────────────────────────────────────
if "spot" not in st.session_state:
    st.session_state.spot = None

# ─────────────────────────────────────────────
#  UI
# ─────────────────────────────────────────────
st.title("🗾 旅行プラン ルーレット")
st.caption("全国47都道府県からランダムに観光地を提案します")

st.divider()

col1, col2 = st.columns(2)
with col1:
    region = st.selectbox("🗺️ 地方で絞り込む", ALL_REGIONS)
with col2:
    selected_cats = st.multiselect(
        "🏷️ カテゴリで絞り込む",
        ALL_CATEGORIES,
        format_func=lambda c: f"{CATEGORY_EMOJI.get(c, '')} {c}",
    )

# フィルタリング
pool = SPOTS
if region != "全国":
    pool = [s for s in pool if s["region"] == region]
if selected_cats:
    pool = [s for s in pool if any(c in s["category"] for c in selected_cats)]

st.caption(f"対象スポット数: **{len(pool)}** 件")

if len(pool) == 0:
    st.warning("条件に合うスポットが見つかりません。フィルターを変更してください。")
else:
    if st.button("🎲 おすすめを探す", type="primary", use_container_width=True):
        st.session_state.spot = random.choice(pool)

    if st.session_state.spot is not None:
        # フィルター変更でプールに含まれない場合はリセット
        spot = st.session_state.spot
        if spot not in pool:
            st.session_state.spot = random.choice(pool)
            spot = st.session_state.spot

        st.divider()

        # カード表示
        cat_tags = "".join(
            f'<span class="tag">{CATEGORY_EMOJI.get(c,"")} {c}</span>'
            for c in spot["category"]
        )
        season_html = " &nbsp; ".join(
            f'<span class="season-good">{SEASON_EMOJI[s]} {s}</span>'
            if s in spot["seasons"]
            else f'<span class="season-off">{SEASON_EMOJI[s]} {s}</span>'
            for s in ["春", "夏", "秋", "冬"]
        )
        highlight_tags = "".join(
            f'<span class="highlight-tag">{h}</span>' for h in spot["highlights"]
        )
        link_md = " ｜ ".join(
            f'[{lk["label"]}]({lk["url"]})' for lk in spot["links"]
        )

        st.markdown(
            f"""
            <div class="spot-card">
                <div class="spot-name">{spot['name']}</div>
                <div class="spot-pref">📍 {spot['pref']}</div>
                {cat_tags}
                <hr style="border:none;border-top:1px solid #e0ddd6;margin:0.8rem 0;">
                <p style="font-size:0.88rem;margin-bottom:0.5rem;">{season_html}</p>
                <p style="line-height:1.9;font-size:0.95rem;">{spot['desc']}</p>
                <p style="margin-top:0.6rem;">{highlight_tags}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"🔗 **関連リンク**: {link_md}")

        # Google マップリンク
        query = urllib.parse.quote(f"{spot['name']} {spot['pref']}")
        st.markdown(
            f"[🗺️ Google マップで見る](https://www.google.com/maps/search/?api=1&query={query})"
        )

# ─────────────────────────────────────────────
#  フッター
# ─────────────────────────────────────────────
st.divider()
st.caption("Powered by Streamlit  ·  データは観光情報として参考用です")

