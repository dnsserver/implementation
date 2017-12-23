# -*- coding: utf-8 -*-
import requests
from requests.auth import _basic_auth_str

client = {
    "client_id": "7c2c0771-131e-4ebc-9914-95e48dfc9df2",
    "client_secret": "AOCNCIAlLOeHam-vrECOfO2tnmkgSuTxSzyP2sqdttmEDBaD-JddRbDFe-7-IVjULiZqLc8J-APeWs0w8vi6sIc"
}


def register_client(url):
    data = "grant_type=client_credentials&scope=openid"
    print(data)
    auth = _basic_auth_str(client['client_id'], client['client_secret'])
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": auth
    }
    print(headers)
    r = requests.post(url, data=data, headers=headers)
    r.raise_for_status()
    return r.text


print(register_client("http://localhost:8085/openid-connect-server-webapp/token"))


"""
curl -i -u "71748421-b1d0-49f9-bd7c-a11997d43e8c:ANmFDjZ0J4-f1yUPlG-yo2HUlrVf8yoce_e6kHEyQ53GKLRRikv3ivR-3Z9Hk52_suxE3c5AzpVL6iwdBlta__s" -d "grant_type=client_credentials&scope=openid" -H "Content-Type: application/x-www-form-urlencoded" http://localhost:8085/openid-connect-server-webapp/token

{
  "client_id": "71748421-b1d0-49f9-bd7c-a11997d43e8c",
  "client_secret": "ANmFDjZ0J4-f1yUPlG-yo2HUlrVf8yoce_e6kHEyQ53GKLRRikv3ivR-3Z9Hk52_suxE3c5AzpVL6iwdBlta__s",
  "redirect_uris": [],
  "client_name": "test_client",
  "client_uri": null,
  "logo_uri": null,
  "contacts": [
    "admin@example.com"
  ],
  "tos_uri": null,
  "token_endpoint_auth_method": "client_secret_post",
  "scope": "address phone email profile",
  "grant_types": [
    "client_credentials"
  ],
  "response_types": [],
  "policy_uri": null,
  "jwks_uri": null,
  "jwks": null,
  "jwksType": "URI",
  "sector_identifier_uri": null,
  "request_object_signing_alg": null,
  "userinfo_signed_response_alg": null,
  "userinfo_encrypted_response_alg": null,
  "userinfo_encrypted_response_enc": null,
  "id_token_signed_response_alg": null,
  "id_token_encrypted_response_alg": null,
  "id_token_encrypted_response_enc": null,
  "default_max_age": 60000,
  "require_auth_time": true,
  "default_acr_values": [],
  "initiate_login_uri": null,
  "post_logout_redirect_uris": [],
  "claims_redirect_uris": [],
  "request_uris": [],
  "software_statement": null,
  "software_id": null,
  "software_version": null,
  "code_challenge_method": null,
  "registration_access_token": "eyJraWQiOiJyc2ExIiwiYWxnIjoiUlMyNTYifQ.eyJhdWQiOiI3MTc0ODQyMS1iMWQwLTQ5ZjktYmQ3Yy1hMTE5OTdkNDNlOGMiLCJpc3MiOiJodHRwOlwvXC9sb2NhbGhvc3Q6ODA4NVwvb3BlbmlkLWNvbm5lY3Qtc2VydmVyLXdlYmFwcFwvIiwiaWF0IjoxNTEzOTgwMTgwLCJqdGkiOiJhZDg4MWQ1ZS05ZWQ0LTQ2NzktYTUwZi05ODVjYmJjOGVkYjQifQ.O8KA_DQ03eq4Atf9uvUC_J2fFWIdFnc58seKDQ0COnDZYolsSO3RdEzC99idUD0Q3meNN_NgM0bbkWhtv94uPKVpnb8L2L-tcnFoqLsVzzwPNMbR-4gYuPQbkuPG_5HFlyAjEyklYYr5wqBgIgfz9OhNYro8f-zbZrYOMKqIwI_3qisfvcnwgdl7PghIygVnEBSNxnGhg2qK9M6z6rtneYamPyBYc5HPVnDq3U470TBtovDi-ZP_1euru5PeSr6PvXbP96lQQ7wq6be9lhmoVVnEaV8MjGoOidQ56PlYNINRxgJym2nFxWslfK-K0YoeOYYpkbXZF0F_Fk0Yv6uhjg",
  "registration_client_uri": "http://localhost:8085/openid-connect-server-webapp/register/71748421-b1d0-49f9-bd7c-a11997d43e8c",
  "softwareId": null,
  "softwareVersion": null,
  "token_endpoint_auth_signing_alg": null,
  "client_secret_expires_at": 0,
  "client_id_issued_at": 1513980180
}
"""