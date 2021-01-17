import sys, os
import datetime
import subprocess
import urllib.parse

# __pycache__を生成させない
sys.dont_write_bytecode = True

# 実行ディレクトリ名
PJTPATH = os.path.dirname(os.path.abspath(__file__))

POST_TEMP = """---
title: "{0}"
upload_date: {1}
date: {1}
category: "{2}"
tags: {3}
permalink: "{4}"
---
"""


# URLで使えない文字
cant_use_chars = [
    "\\",
    "'",
    "|",
    "`",
    "^",
    '"',
    "<",
    ">",
    ")",
    "(",
    "}",
    "{",
    "]",
    "[",
    ";",
    "/",
    "?",
    ":",
    "@",
    "&",
    "=",
    "+",
    "$",
    ",",
    "%",
    "#",
    ".",
]


# コマンドライン引数を取得
def get_args():
    import argparse
    from argparse import RawTextHelpFormatter

    ap = argparse.ArgumentParser(
        prog="templatecreator.py",
        usage="create post template.",
        description="""example:
        $ python templatecreator.py "i love python <3" -c language -t python "Rapsberry Pi"
    """,
        add_help=True,
        formatter_class=RawTextHelpFormatter,
    )
    # タイトル
    ap.add_argument("title", help="post's title.")
    # カテゴリ
    ap.add_argument(
        "-c",
        "--category",
        help='post\'s category (like group). default: "other"',
        default="Other",
    )
    # タグ
    ap.add_argument(
        "-t",
        "--tags",
        help="post's tags. defalut: ['other']",
        default=["other"],
        nargs="*",
    )
    args = ap.parse_args()

    return args.title, args.category.lower(), [tag.lower() for tag in args.tags]


class TemplateCreator:
    def __init__(self, *args):
        title, category, tags = args
        tag4path: str = self._get_norm_str(tags[0])
        cate4path: str = self._get_norm_str(category)
        out_dir: str = os.path.join(
            PJTPATH, "_posts", cate4path, tag4path,
        )
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        date: datetime = self._get_now()
        link, self.path = self._get_link_and_path(cate4path, tag4path, out_dir, date)
        self.content = POST_TEMP.format(
            title, f"{date:%Y-%m-%d %H:%M:%S %z}", category, str(tags), link,
        )

    # テンプレート出力
    def create(self):
        with open(self.path, "wb") as f:
            f.write(self.content.encode("utf-8"))

    # jekyllに準拠したフォーマットの日付を取得(yyyy-mm-dd HH-MM-SS +/-hhmm)
    def _get_now(self) -> datetime:
        # 0: year, 1: month, 2: day, 3: hour, 4: minutes, 5: seconds
        now_date: datetime = datetime.datetime(
            *datetime.datetime.today().timetuple()[:6]
        )
        utc_date: datetime = datetime.datetime(*now_date.utcnow().timetuple()[:6])
        tz: timezone = datetime.timezone(now_date - utc_date)
        return now_date.astimezone(tz)

    # permalinkとファイルパスを取得
    def _get_link_and_path(self, c: str, t: str, od: str, date: datetime) -> (str, str):
        date4path = f"{date:%Y-%m-%d}"
        lisd_dir = [f for f in os.listdir(od) if os.path.isfile(os.path.join(od, f))]
        num = 0
        for i in range(2 * 100):
            if not f"{date4path}-{t}_{num}.md" in lisd_dir:
                return (
                    "/".join(["/articles", c, t, f"{date:%Y/%m/%d}", f"{t}_{num}",]),
                    os.path.join(od, f"{date4path}-{t}_{num}.md"),
                )
            else:
                num += 1

    # 文字列の正規化(使用できない文字は16進数文字に置き換える)
    def _get_norm_str(self, s: str):
        if s.isascii() and len([c for c in cant_use_chars if c in s]) == 0:
            return s

        # 置き換え対象となる文字列と置き換える文字列
        before_after = {
            c: c.encode().hex() for c in s if not c.isascii() or c in cant_use_chars
        }

        for before, after in before_after.items():
            s = s.replace(before, after)
        return s


if __name__ == "__main__":
    args = ()
    if len(sys.argv) > 1:
        args = get_args()
    else:
        title = input("title : ")
        while title == "":
            title = input("title! : ")

        category = input("category : ").lower()
        if category == "":
            category = "other"

        tags = [tag.strip().lower() for tag in input('tags (split ",") : ').split(",")]
        if tags[0] == "":
            tags = ["other"]
        args = (title, category, tags)

    TemplateCreator(*args).create()

