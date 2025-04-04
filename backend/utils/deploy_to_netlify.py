import requests
import time
import uuid

def upload_zip_to_netlify(zip_path, netlify_token):
    headers = {
        "Authorization": f"Bearer {netlify_token}",
    }

    # Step 1: Create site with unique name
    site_name = f"puzzle-site-{uuid.uuid4().hex[:8]}"
    create_payload = { "name": site_name }

    print(f"🚀 Creating site: {site_name}")
    site_resp = requests.post("https://api.netlify.com/api/v1/sites", headers=headers, json=create_payload)
    if site_resp.status_code not in (200, 201):
        raise Exception(f"❌ Failed to create Netlify site: {site_resp.status_code} - {site_resp.text}")

    site_info = site_resp.json()
    site_id = site_info["id"]
    site_url = site_info.get("ssl_url") or site_info.get("url")

    print(f"✅ Site created: {site_url} (id: {site_id})")

    # Step 2: Optional wait + poll for provisioning
    print("⏳ Waiting for site to finish provisioning...")
    time.sleep(2)
    for _ in range(100):
        status_resp = requests.get(f"https://api.netlify.com/api/v1/sites/{site_id}", headers=headers)
        if status_resp.status_code == 200:
            state = status_resp.json().get("state")
            print(f"🔍 Site state: {state}")
            if state == "current":
                print("✅ Site is ready for deploy.")
                break
        time.sleep(1)
    else:
        print("⚠️ Timed out waiting — deploying anyway...")

    # Step 3: Upload ZIP
    print("📦 Deploying ZIP...")
    with open(zip_path, "rb") as f:
        zip_bytes = f.read()

    files = {
        "file": ("site.zip", zip_bytes, "application/zip"),
    }

    deploy_url = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys"
    deploy_resp = requests.post(deploy_url, headers=headers, files=files)
    if deploy_resp.status_code not in (200, 201):
        raise Exception(f"❌ Failed to deploy ZIP: {deploy_resp.status_code} - {deploy_resp.text}")

    deploy_data = deploy_resp.json()
    deploy_id = deploy_data["id"]
    deploy_status_url = f"https://api.netlify.com/api/v1/deploys/{deploy_id}"

    # Step 4: Poll until deploy is ready
    print(f"🔁 Polling deploy {deploy_id} until it's ready...")
    for _ in range(120):
        d_status = requests.get(deploy_status_url, headers=headers)
        if d_status.status_code == 200:
            d_state = d_status.json().get("state")
            print(f"🔍 Deploy state: {d_state}")
            if d_state == "ready":
                print("✅ Deploy is ready.")
                break
        time.sleep(1)
    else:
        raise Exception("❌ Deploy never became ready.")

    # Step 5: Lock the deploy
    print(f"🔒 Locking deploy {deploy_id}...")
    lock_url = f"https://api.netlify.com/api/v1/deploys/{deploy_id}/lock"
    lock_resp = requests.post(lock_url, headers=headers)
    if lock_resp.status_code not in (200, 204):
        raise Exception(f"❌ Failed to lock deploy: {lock_resp.status_code} - {lock_resp.text}")
    print("✅ Deploy locked successfully!")

    return site_url
