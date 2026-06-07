import json
import html

def reddit_json_to_txt(raw_json, out_path):
    """
    Takes a raw Reddit .json string (single line) and writes extracted text to out_path.
    """
    data = json.loads(raw_json)

    post = data[0]["data"]["children"][0]["data"]
    title = post.get("title", "")
    body = html.unescape(post.get("selftext", ""))
    texts = [f"TITLE: {title}", f"POST: {body}"]

    def walk(children):
        for child in children:
            if child["kind"] != "t1":  # t1 = comment
                continue
            c = child["data"]
            comment_body = html.unescape(c.get("body", ""))
            if comment_body and comment_body not in ("[deleted]", "[removed]"):
                texts.append(f"COMMENT: {comment_body}")
            replies = c.get("replies")
            if replies and isinstance(replies, dict):
                walk(replies["data"]["children"])

    walk(data[1]["data"]["children"])
    text = "\n\n".join(texts)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✓ Saved {len(text)} chars to {out_path}")
    return text


# Read from terminal — JSON on one line
raw = input("Paste the raw Reddit JSON (single line): ")
out_path = input("Output filename (e.g. data/raw/reddit_acc_general.txt): ")
reddit_json_to_txt(raw, out_path)