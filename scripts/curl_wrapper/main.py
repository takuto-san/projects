import requests
from urllib.parse import urljoin
from dataclasses import dataclass, field

@dataclass
class Request:
    base_url: str
    method: str
    path: str
    params: dict = field(default_factory=dict)
    json: dict = field(default_factory=dict)

api_requests = [
    Request(base_url="https://api.github.com", method="get", path="/zen"),
    Request(base_url="https://api.github.com", method="get", path="/meta"),
    Request(base_url="https://www.googleapis.com", method="get", path="/books/v1/volumes", params={"q": "python"}),
    Request(base_url="https://www.googleapis.com", method="get", path="/discovery/v1/apis"),
    Request(base_url="https://www.jma.go.jp", method="get", path="/bosai/forecast/data/forecast/130000.json"),
    Request(base_url="https://www.jma.go.jp", method="get", path="/bosai/common/const/area.json"),
    Request(base_url="https://ndlsearch.ndl.go.jp", method="get", path="/api/opensearch", params={"title": "python"}),
    Request(base_url="https://ndlsearch.ndl.go.jp", method="get", path="/api/sru", params={"operation": "searchRetrieve", "query": "title=python"}),
    Request(base_url="https://ci.nii.ac.jp", method="get", path="/books/opensearch/search", params={"q": "python", "format": "json"}),
    Request(base_url="https://ci.nii.ac.jp", method="get", path="/books/opensearch/author", params={"q": "python", "format": "json"})
]

def send_api(req: Request):
    url = urljoin(req.base_url, req.path)
    
    kwargs = {}
    if req.params: kwargs["params"] = req.params
    if req.json: kwargs["json"] = req.json
        
    return requests.request(req.method.upper(), url, **kwargs)

def run(requests_list):
    for req in requests_list:
        try:
            res = send_api(req)
            res.raise_for_status()
            
            print(f"Success ({res.status_code}): [{req.method.upper()}] {req.base_url}{req.path}")
            
        except requests.exceptions.RequestException as e:
            print(f"Failed: {req.base_url}{req.path} - Error: {e}")
            break

if __name__ == "__main__":
    run(api_requests)