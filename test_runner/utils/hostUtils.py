from urllib.parse import urlparse


def parse_host(ip,api):
    if not isinstance(ip,list):
        return api
    if not api:
        return api
    try:
        parts=urlparse(api["request"]["url"])
    except:
        parts = urlparse(api["request"]["base_url"])
    host=parts.netloc
    if host:
        for content in ip:
            content=content.strip()
            if not content.startswith("#"):
                # ip1=re.findall(r'\b(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b',content)
                # print(ip1)
                # if [ip1]:
                if 'headers' in api["request"].keys():
                    api["request"]["headers"]["Host"]=host
                else:
                    api["request"].setdefault("headers",{"Host":host})
                try:
                    api["request"]["url"]=api["request"]["url"].replace(host,content)
                except KeyError:
                    api["request"]["base_url"]=api["request"]["base_url"].replace(host,content)
    else:
        for content in ip:
            try:
                api["request"]["url"] = content+api["request"]["url"]
            except KeyError:
                api["request"]["base_url"] = content+api["request"]["url"]
    return api

# if __name__ == "__main__":
#     a = parse_host(None, None)
#     print(a)