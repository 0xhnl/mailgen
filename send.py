import argparse
import requests
from datetime import datetime, timezone
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Gophish server details
GOPHISH_HOST = "https://test.com:1231"  # Update with your Gophish host and port
API_KEY = "123123123123123123123"  # Replace with your API key

# Headers for API requests
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def create_campaign(campaign_name, template_name, landing_page_name, url, profile_name, group_name, send_now):
    """
    Create and start a phishing campaign in Gophish.
    :param campaign_name: Name of the campaign
    :param template_name: Name of the email template
    :param landing_page_name: Name of the landing page
    :param url: Campaign URL (redirect URL)
    :param profile_name: Sending profile name
    :param group_name: Target group name
    :param send_now: Boolean indicating whether to send the campaign now
    """
    # Fetch the template ID
    template_id = get_template_id(template_name)
    if not template_id:
        print(f"[-] Template '{template_name}' not found.")
        return

    # Fetch the landing page ID
    landing_page_id = get_landing_page_id(landing_page_name)
    if not landing_page_id:
        print(f"[-] Landing page '{landing_page_name}' not found.")
        return

    # Fetch the sending profile ID
    profile_id = get_profile_id(profile_name)
    if not profile_id:
        print(f"[-] Sending profile '{profile_name}' not found.")
        return

    # Fetch the group ID
    group_id = get_group_id(group_name)
    if not group_id:
        print(f"[-] Group '{group_name}' not found.")
        return

    # Set launch date based on the -now flag
    if send_now:
        launch_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"[+] Launching campaign immediately at: {launch_date}")
    else:
        launch_date = "2023-10-01T00:00:00Z"  # Default future date
        print(f"[+] Launching campaign at: {launch_date}")

    # Prepare the campaign payload
    data = {
        "name": campaign_name,
        "template": {"name": template_name, "id": template_id},
        "page": {"name": landing_page_name, "id": landing_page_id},
        "url": url,
        "smtp": {"name": profile_name, "id": profile_id},
        "launch_date": launch_date,
        "groups": [{"name": group_name, "id": group_id}]
    }

    # Send POST request to create the campaign
    response = requests.post(f"{GOPHISH_HOST}/api/campaigns/", headers=HEADERS, json=data, verify=False)
    if response.status_code == 201:
        print(f"[+] Successfully created campaign: {campaign_name}")
    else:
        print(f"[-] Failed to create campaign: {campaign_name}")
        print(f"    Response: {response.text}")

def get_template_id(template_name):
    """
    Get the ID of an email template by name.
    :param template_name: Name of the template
    :return: Template ID or None if not found
    """
    response = requests.get(f"{GOPHISH_HOST}/api/templates/", headers=HEADERS, verify=False)
    if response.status_code == 200:
        templates = response.json()
        for template in templates:
            if template["name"] == template_name:
                return template["id"]
    return None

def get_landing_page_id(landing_page_name):
    """
    Get the ID of a landing page by name.
    :param landing_page_name: Name of the landing page
    :return: Landing page ID or None if not found
    """
    response = requests.get(f"{GOPHISH_HOST}/api/pages/", headers=HEADERS, verify=False)
    if response.status_code == 200:
        pages = response.json()
        for page in pages:
            if page["name"] == landing_page_name:
                return page["id"]
    return None

def get_profile_id(profile_name):
    """
    Get the ID of a sending profile by name.
    :param profile_name: Name of the sending profile
    :return: Profile ID or None if not found
    """
    response = requests.get(f"{GOPHISH_HOST}/api/smtp/", headers=HEADERS, verify=False)
    if response.status_code == 200:
        profiles = response.json()
        for profile in profiles:
            if profile["name"] == profile_name:
                return profile["id"]
    return None

def get_group_id(group_name):
    """
    Get the ID of a group by name.
    :param group_name: Name of the group
    :return: Group ID or None if not found
    """
    response = requests.get(f"{GOPHISH_HOST}/api/groups/", headers=HEADERS, verify=False)
    if response.status_code == 200:
        groups = response.json()
        for group in groups:
            if group["name"] == group_name:
                return group["id"]
    return None

def main():
    parser = argparse.ArgumentParser(description="Create and start a phishing campaign in Gophish.")
    parser.add_argument("-l", "--landing-page", required=True, help="Name of the landing page")
    parser.add_argument("-t", "--template", required=True, help="Name of the email template")
    parser.add_argument("-u", "--url", required=True, help="Campaign URL (redirect URL)")
    parser.add_argument("-p", "--profile", required=True, help="Sending profile name")
    parser.add_argument("-g", "--group", required=True, help="Target group name")
    parser.add_argument("-c", "--campaign", required=True, help="Campaign name")
    parser.add_argument("-now", action="store_true", help="Send the campaign immediately")

    args = parser.parse_args()

    create_campaign(
        campaign_name=args.campaign,
        template_name=args.template,
        landing_page_name=args.landing_page,
        url=args.url,
        profile_name=args.profile,
        group_name=args.group,
        send_now=args.now
    )

if __name__ == "__main__":
    main()
