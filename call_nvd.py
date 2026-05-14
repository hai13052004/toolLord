import requests

def check_vuln(banner):
    try:
        keyword = banner.replace("SSH-2.0-", "")\
                        .replace("_for_Windows", "")\
                        .replace("_", " ")
        # print(f"DEBUG keyword: {keyword}")
        url= f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}"
        response = requests.get(url, timeout=5)
        data =  response.json()

        if data["totalResults"]==0:
            return "không tìm thấy CVE"
        
        cve = data["vulnerabilities"][0]["cve"]
        cve_id = cve["id"]
        description = cve["descriptions"][0]["value"]
        return f"{cve_id}: {description[:100]}..."
    except requests.Timeout:
        return "API timeout"
    except Exception as e:
        #return f"N/A"
        return f"Loi: {e}"
# print(check_vuln("OpenSSH 9.5"))    
#print(check_vuln("SSH-2.0-OpenSSH_for_Windows_9.5"))