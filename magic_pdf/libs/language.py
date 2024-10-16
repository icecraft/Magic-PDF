import pycld2 as cld2
import regex
import unicodedata


RE_BAD_CHARS = regex.compile(r"\p{Cc}|\p{Cs}")


def remove_bad_chars(text):
    return RE_BAD_CHARS.sub("", text)


def detect_lang(text: str) -> str:
    if len(text) == 0:
        return ""

    try:
        _, _, details = cld2.detect(text)
    except:
        # cld2 doesn't like control characters
        # https://github.com/mikemccand/chromium-compact-language-detector/issues/22#issuecomment-435904616
        html_no_ctrl_chars = ''.join([l for l in text if unicodedata.category(l)[0] not in ['C',]])
        _, _, details = cld2.detect(html_no_ctrl_chars)
    lang = ""
    try:
        lang = details[0][1].lower()
    except:
        lang = ""
    return lang


if __name__ == '__main__':
    print(detect_lang("This is a test."))
    print(detect_lang("<html>This is a test</html>"))
    print(detect_lang("这个是中文测试。"))
    print(detect_lang("<html>这个是中文测试。</html>"))