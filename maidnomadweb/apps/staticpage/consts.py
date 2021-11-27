STATICPAGES = {
    "top": {
        "template": "staticpage/toppage.html",
        "title": "TopPage",
        "ogp_title": "メイドカフェでノマド会公式ページへようこそ",
        "ogp_type": "website",
        "priority": 1.0,
        "changefreq": "monthly",
    },
    "maidnomad_info": {
        "template": "staticpage/maidnomad_info.html",
        "title": "メイドカフェ店舗様向けノマド会のご紹介",
        "parent": "top",
        "description": (
            # fmt: off
            "メイドカフェ様向けに私達メイドカフェでノマド会の目指していること、"
            "一緒に取り組んでいきたいことを説明する資料を掲載しています。"
        ),
        "changefreq": "monthly",
    },
    "maidcafe_info": {
        "template": "staticpage/maidcafe_info.html",
        "title": "ノマドができるメイドカフェ紹介",
        "parent": "top",
        "description": (
            # fmt: off
            "どのお店に行けば良いのかまったく分からないという方のために、"
            "メイドカフェでノマド会としておすすめのお店を紹介します。"
        ),
        "changefreq": "weekly",
    },
    "organization": {
        "template": "staticpage/organization.html",
        "title": "運営体制",
        "parent": "top",
        "description": (
            # fmt: off
            "メイドカフェでノマド会の運営体制と参加者、"
            "イベントオーガナイザー、メイドさんの役割を説明します。"
        ),
        "changefreq": "yearly",
    },
}
